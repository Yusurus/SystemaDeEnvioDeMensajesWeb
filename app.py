from flask import Flask, render_template, redirect, url_for, flash, request, send_file
import model
import email_service
import config
import pandas as pd
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
        try:
            # --- Obtener filtros y pestaña activa ---
            search_query = request.args.get('search_name', None)
            filter_facultad = request.args.get('filter_facultad', None)
            filter_escuela = request.args.get('filter_escuela', None)
            
            # Determinar pestaña activa
            active_tab = request.args.get('tab', 'notificar')
            if search_query or filter_facultad or filter_escuela:
                active_tab = 'reporte-general'
            
            # --- Pestaña 1: Notificar ---
            status = get_notification_status()
            participants_list = model.get_unnotified_participants(status['available_this_batch'])
            
            # --- Pestaña 2: Reporte (Log) ---
            log_search_query = request.args.get('log_search_name', None)
            if log_search_query:
                active_tab = 'reporte-log'
            notification_log = model.get_notification_log(search_term=log_search_query)
            
            # --- Pestaña 3: Reporte (General) ---
            participant_report = model.get_participant_report(search_query, filter_facultad, filter_escuela)
            
            # --- Pestaña 4: Administrar (Cargar listas) ---
            events_list = model.get_all_events()
            facultades_list = model.get_all_facultades() # NUEVO
            escuelas_list = model.get_all_escuelas()     # NUEVO
            
            return render_template(
                'index.html', 
                # Tab 1
                participants=participants_list,
                status=status,
                # Tab 2
                logs=notification_log,
                log_search_name=log_search_query or "",
                # Tab 3
                report_data=participant_report,
                search_name=search_query or "",
                current_facultad=filter_facultad,
                current_escuela=filter_escuela,
                # Tab 4
                events_list=events_list,
                facultades_list=facultades_list,
                escuelas_list=escuelas_list,
                # General
                active_tab=active_tab
            )
        except Exception as e:
            flash(f"Error al cargar la página: {e}", 'error')
            return render_template('index.html', participants=[], status={'count_today': 0, 'daily_limit': config.EMAIL_DAILY_LIMIT, 'remaining_today': 0}, logs=[], events_list=[], facultades_list=[], escuelas_list=[], report_data=[], search_name="", log_search_name="", active_tab="notificar")

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
                if model.update_participant_status(p['idParticipante']):
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
        Ahora obtiene los IDs opcionales de facultad y escuela.
        """
        if request.method == 'POST':
            nombres = request.form['nombres_participante']
            correo = request.form['correo_participante']
            evento_id = request.form['evento_id']
            
            # .get() devuelve None si la clave no existe (perfecto para campos opcionales)
            facultad_id = request.form.get('facultad_id')
            escuela_id = request.form.get('escuela_id')
            
            # Convertir a None si está vacío
            if not facultad_id: facultad_id = None
            if not escuela_id: escuela_id = None

            success, message = model.add_new_participant(nombres, correo, evento_id, facultad_id, escuela_id)

            if success:
                flash(f"¡Éxito! Participante '{nombres}' agregado correctamente.", 'success')
            else:
                flash(f"Error al agregar participante: {message}", 'warning')

        return redirect(url_for('index', tab='administrar'))

    @app.route('/export/excel')
    def export_excel():
        """
        Exporta el nuevo "Reporte General" con filtros.
        """
        try:
            search_query = request.args.get('search_name', '')
            filter_facultad = request.args.get('filter_facultad', None)
            filter_escuela = request.args.get('filter_escuela', None)

            # Obtenemos los datos (¡quitando el límite web!)
            data = model.get_participant_report(search_query, filter_facultad, filter_escuela)
            # ^ NOTA: get_participant_report tiene un "LIMIT 500" - deberías quitarlo
            # o hacerlo un parámetro para una exportación completa.
            # Por ahora, funcionará con los 500 primeros.

            if not data:
                flash("No hay datos para exportar.", "info")
                return redirect(url_for('index', tab='reporte-general'))

            df = pd.DataFrame(data)
            
            df.rename(columns={
                'nombresCompleto': 'Nombre Completo',
                'correo': 'Correo Electrónico',
                'estadoNotificado': 'Estado',
                'nombre_evento': 'Evento',
                'nombre_facultad': 'Facultad',
                'nombre_escuela': 'Escuela'
            }, inplace=True)
            
            # Rellenar valores nulos para un reporte más limpio
            df['Facultad'] = df['Facultad'].fillna('N/A')
            df['Escuela'] = df['Escuela'].fillna('N/A')

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Reporte_Participantes')
            output.seek(0)

            return send_file(
                output,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name='reporte_participantes.xlsx'
            )

        except Exception as e:
            flash(f"Error al exportar a Excel: {e}", "warning")
            return redirect(url_for('index', tab='reporte-general'))
    
    @app.route('/upload-excel', methods=['POST'])
    def upload_excel():
        """
        Ahora puede asignar una facultad y/o escuela a
        TODOS los participantes del Excel subido.
        """
        if 'excel_file' not in request.files:
            flash('No se encontró ningún archivo', 'warning')
            return redirect(url_for('index', tab='administrar'))
        
        file = request.files['excel_file']
        evento_id = request.form['evento_id']
        
        # IDs opcionales para todo el lote
        facultad_id = request.form.get('facultad_id')
        escuela_id = request.form.get('escuela_id')
        if not facultad_id: facultad_id = None
        if not escuela_id: escuela_id = None
        
        if file.filename == '' or not evento_id:
            flash('No se seleccionó archivo o evento de destino', 'warning')
            return redirect(url_for('index', tab='administrar'))
        
        if file:
            try:
                df = pd.read_excel(file)
                
                if 'NombresCompletos' not in df.columns or 'CorreoElectronico' not in df.columns:
                    flash("Error: El archivo Excel debe tener las columnas 'NombresCompletos' y 'CorreoElectronico'", 'warning')
                    return redirect(url_for('index', tab='administrar'))

                success_count = 0
                fail_count = 0
                
                for index, row in df.iterrows():
                    nombres = str(row['NombresCompletos'])
                    correo = str(row['CorreoElectronico'])
                    
                    # Reutilizamos nuestra función de modelo actualizada
                    success, _ = model.add_new_participant(
                        nombres, correo, evento_id, facultad_id, escuela_id
                    )
                    
                    if success:
                        success_count += 1
                    else:
                        fail_count += 1
                        
                flash(f"Importación completada: {success_count} agregados, {fail_count} fallaron.", 'success')
            
            except Exception as e:
                flash(f"Error al procesar el archivo: {e}", 'warning')
                
        return redirect(url_for('index', tab='administrar'))
    return app

if __name__ == '__main__':
    app = crear_app()
    app.run(debug=True)