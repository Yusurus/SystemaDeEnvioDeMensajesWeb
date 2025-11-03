# app.py
from flask import (
    Flask, render_template, redirect, url_for, 
    flash, request, send_file
)
import model
import email_service
import config
import pandas as pd  # <-- NUEVO
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'puedes-poner-cualquier-texto-aleatorio-aqui' 

def crear_app():

    def get_notification_status():
        """Función auxiliar para no repetir código"""
        
        # 1. Contar cuántos se enviaron hoy (Usando la nueva función corregida)
        count_today = model.get_24h_rolling_sent_count() # <--- ÚNICO CAMBIO AQUÍ
        
        # 2. Calcular cuántos quedan para el límite diario
        remaining_today = config.EMAIL_DAILY_LIMIT - count_today
        
        # 3. Calcular cuántos podemos enviar en ESTE LOTE
        available_this_batch = max(0, min(config.EMAIL_BATCH_LIMIT, remaining_today))

        # El resto de la lógica no cambia
        return {
            'count_today': count_today,
            'daily_limit': config.EMAIL_DAILY_LIMIT,
            'remaining_today': remaining_today,
            'available_this_batch': available_this_batch
        }


    @app.route('/')
    def index():
        """
        Controlador para la página principal (GET).
        Ahora carga datos para las TRES pestañas y maneja la búsqueda.
        """
        try:
            # 2. Manejo de la pestaña activa y la búsqueda
            # Si 'search_name' está en la URL, activamos la pestaña de reportes
            search_query = request.args.get('search_name', None)
            active_tab = 'reportes' if search_query is not None else 'notificar'
            
            # Pestaña 1: Notificar
            status = get_notification_status()
            participants_list = model.get_unnotified_participants(status['available_this_batch'])
            
            # Pestaña 2: Reportes (ahora pasa el término de búsqueda)
            notification_log = model.get_notification_log(search_term=search_query) # Usa el límite por defecto
            
            # Pestaña 3: Administrar
            events_list = model.get_all_events()
            
            return render_template(
                'index.html', 
                participants=participants_list,
                status=status,
                logs=notification_log,
                events_list=events_list,
                search_name=search_query or "", # Pasa el término de búsqueda de vuelta
                active_tab=active_tab           # Pasa la pestaña activa
            )
        except Exception as e:
            flash(f"Error al cargar la página: {e}", 'error')
            return render_template('index.html', participants=[], status={'count_today': 0, 'daily_limit': config.EMAIL_DAILY_LIMIT, 'remaining_today': 0}, logs=[], events_list=[], search_name="", active_tab="notificar")

    @app.route('/enviar-notificaciones', methods=['POST'])
    def send_notifications():
        """
        Controlador para la acción de enviar (POST).
        Ahora respeta el límite diario y de lote.
        """
        # 1. Volvemos a calcular el estado (NO confiamos en lo que mostró la página)
        status = get_notification_status()

        if status['available_this_batch'] <= 0:
            if status['remaining_today'] <= 0:
                flash(f"Límite diario de {config.EMAIL_DAILY_LIMIT} correos alcanzado. Intenta mañana.", 'warning')
            else:
                flash('No hay participantes para notificar en este momento.', 'info')
            return redirect(url_for('index'))

        # 2. Obtenemos la lista FRESCA de participantes, respetando el límite
        participants = model.get_unnotified_participants(status['available_this_batch'])
        
        if not participants:
            flash('No hay participantes para notificar.', 'info')
            return redirect(url_for('index'))

        success_count = 0
        fail_count = 0

        # 3. Iteramos sobre la lista (que ya está limitada a 50 o menos)
        for p in participants:
            if email_service.send_notification_email(p):
                if model.update_participant_status(p['idPerticipante']):
                    success_count += 1
                else:
                    fail_count += 1
                    print(f"ERROR GRAVE: Correo enviado a {p['correo']} pero no se pudo actualizar la BD.")
            else:
                fail_count += 1

        # 5. Enviamos un mensaje de retroalimentación al usuario
        if fail_count > 0:
            flash(f"Proceso completado con errores: {success_count} notificados, {fail_count} fallaron.", 'warning')
        else:
            flash(f"¡Éxito! {success_count} participantes notificados correctamente.", 'success')

        return redirect(url_for('index'))

    @app.route('/add-event', methods=['POST'])
    def add_event():
        """
        Controlador para el formulario de agregar evento.
        """
        if request.method == 'POST':
            nombre = request.form['nombre_evento']
            fecha = request.form['fecha_evento']
            
            success, message = model.add_new_event(nombre, fecha)
            
            if success:
                flash(f"¡Éxito! Evento '{nombre}' agregado correctamente.", 'success')
            else:
                flash(f"Error al agregar evento: {message}", 'warning')
                
        # Redirigimos de vuelta a la página principal
        return redirect(url_for('index'))

    @app.route('/add-participant', methods=['POST'])
    def add_participant():
        """
        Controlador para el formulario de agregar participante.
        """
        if request.method == 'POST':
            nombres = request.form['nombres_participante']
            correo = request.form['correo_participante']
            evento_id = request.form['evento_id']
            
            success, message = model.add_new_participant(nombres, correo, evento_id)

            if success:
                flash(f"¡Éxito! Participante '{nombres}' agregado correctamente.", 'success')
            else:
                flash(f"Error al agregar participante: {message}", 'warning')

        return redirect(url_for('index'))

    @app.route('/export/excel')
    def export_excel():
        """
        Genera y descarga un archivo Excel con el log de notificaciones.
        """
        try:
            # Obtenemos el mismo término de búsqueda desde la URL
            search_query = request.args.get('search_name', '')

            # Obtenemos los datos, PERO con un límite muy alto
            data = model.get_notification_log(search_term=search_query, limit_amount=100000)

            if not data:
                flash("No hay datos para exportar.", "info")
                return redirect(url_for('index'))

            # Convertimos la lista de diccionarios a un DataFrame de Pandas
            df = pd.DataFrame(data)
            
            # Renombramos columnas para que se vean bien en Excel
            df.rename(columns={
                'nombre': 'Nombre del Participante',
                'correo': 'Correo Electrónico',
                'fecha': 'Fecha de Notificación'
            }, inplace=True)

            # Formateamos la fecha (opcional, pero recomendado)
            df['Fecha de Notificación'] = pd.to_datetime(df['Fecha de Notificación']).dt.strftime('%Y-%m-%d %H:%M:%S')

            # Creamos un archivo Excel en memoria
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Reporte_Notificaciones')
            
            output.seek(0) # Regresamos al inicio del "archivo" en memoria

            # Enviamos el archivo al usuario para su descarga
            return send_file(
                output,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name='reporte_notificaciones.xlsx'
            )

        except Exception as e:
            flash(f"Error al exportar a Excel: {e}", "warning")
            return redirect(url_for('index'))
        
    @app.route('/upload-excel', methods=['POST'])
    def upload_excel():
        """
        Procesa el archivo Excel subido para agregar participantes en lote.
        """
        if 'excel_file' not in request.files:
            flash('No se encontró ningún archivo', 'warning')
            return redirect(url_for('index'))
        
        file = request.files['excel_file']
        evento_id = request.form['evento_id']
        
        if file.filename == '':
            flash('No se seleccionó ningún archivo', 'warning')
            return redirect(url_for('index'))
        
        if file and evento_id:
            try:
                # Lee el archivo Excel en un DataFrame de Pandas
                df = pd.read_excel(file)
                
                # --- Validación de Columnas ---
                # Aseguramos que las columnas se llamen EXACTAMENTE como queremos
                if 'NombresCompletos' not in df.columns or 'CorreoElectronico' not in df.columns:
                    flash("Error: El archivo Excel debe tener las columnas 'NombresCompletos' y 'CorreoElectronico'", 'warning')
                    return redirect(url_for('index'))

                success_count = 0
                fail_count = 0
                
                # Iteramos sobre cada fila del Excel
                for index, row in df.iterrows():
                    nombres = str(row['NombresCompletos'])
                    correo = str(row['CorreoElectronico'])
                    
                    # Reutilizamos nuestra función de modelo existente
                    success, _ = model.add_new_participant(nombres, correo, evento_id)
                    
                    if success:
                        success_count += 1
                    else:
                        fail_count += 1
                        
                flash(f"Importación completada: {success_count} agregados, {fail_count} fallaron.", 'success')
            
            except Exception as e:
                flash(f"Error al procesar el archivo: {e}", 'warning')
                
        return redirect(url_for('index'))
    return app

if __name__ == '__main__':
    app = crear_app()
    app.run(debug=True)