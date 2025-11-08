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
    # app.py

    @app.route('/')
    def index():
        try:
            # --- Obtener filtros y pestaña activa ---
            search_query = request.args.get('search_name', None)
            filter_facultad = request.args.get('filter_facultad', None)
            filter_escuela = request.args.get('filter_escuela', None)
            date_start = request.args.get('date_start', None)
            date_end = request.args.get('date_end', None)
            noti_date_start = request.args.get('noti_date_start', None)
            noti_date_end = request.args.get('noti_date_end', None)
            
            active_tab = request.args.get('tab', 'notificar')
            
            if any([search_query, filter_facultad, filter_escuela, date_start, date_end, noti_date_start, noti_date_end]):
                active_tab = 'reporte-general'
            
            # --- Pestaña 1: Notificar ---
            status = get_notification_status()
            participants_list = model.get_unnotified_participants(status['available_this_batch'])
            
            # --- Pestaña 2: Reporte (General) ---
            participant_report = model.get_participant_report(
                search_query, filter_facultad, filter_escuela, 
                date_start, date_end, noti_date_start, noti_date_end
            )
            
            # --- Pestaña 3: Vistas (NUEVO) ---
            event_summary_data = model.get_event_summary_view()
            all_participants_data = model.get_all_participants_view()

            # --- Pestaña 4: Administrar ---
            events_list = model.get_all_events()
            facultades_list = model.get_all_facultades()
            escuelas_list = model.get_all_escuelas()
            
            return render_template(
                'index.html', 
                # Tab 1
                participants=participants_list,
                status=status,
                # Tab 2
                report_data=participant_report,
                search_name=search_query or "",
                current_facultad=filter_facultad,
                current_escuela=filter_escuela,
                current_date_start=date_start or "",
                current_date_end=date_end or "",
                current_noti_date_start=noti_date_start or "",
                current_noti_date_end=noti_date_end or "",
                # Tab 3 (NUEVO)
                event_summary=event_summary_data,
                all_participants=all_participants_data,
                # Tab 4
                events_list=events_list,
                facultades_list=facultades_list,
                escuelas_list=escuelas_list,
                # General
                active_tab=active_tab
            )
        except Exception as e:
            flash(f"Error al cargar la página: {e}", 'error')
            # ... (se añaden los nuevos valores por defecto al render de error) ...
            return render_template('index.html', participants=[], status={'count_today': 0, 'daily_limit': config.EMAIL_DAILY_LIMIT, 'remaining_today': 0}, events_list=[], facultades_list=[], escuelas_list=[], report_data=[], search_name="", active_tab="notificar", current_date_start="", current_date_end="", current_noti_date_start="", current_noti_date_end="", event_summary=[], all_participants=[])
    
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

    @app.route('/export/reporte-general') # <-- CAMBIO DE NOMBRE
    def export_reporte_general(): # <-- CAMBIO DE NOMBRE
        """
        Exporta el Reporte General con todos sus filtros.
        """
        try:
            # ... (leer todos los filtros de la URL) ...
            search_query = request.args.get('search_name', '')
            filter_facultad = request.args.get('filter_facultad', None)
            filter_escuela = request.args.get('filter_escuela', None)
            date_start = request.args.get('date_start', None)
            date_end = request.args.get('date_end', None)
            noti_date_start = request.args.get('noti_date_start', None)
            noti_date_end = request.args.get('noti_date_end', None)

            data = model.get_participant_report(
                search_query, filter_facultad, filter_escuela, 
                date_start, date_end, noti_date_start, noti_date_end
            )
            if not data:
                flash("No hay datos para exportar.", "info")
                return redirect(url_for('index', tab='reporte-general'))

            df = pd.DataFrame(data)
            # ... (renombrar columnas) ...
            df.rename(columns={
                'nombresCompleto': 'Nombre Completo', 'correo': 'Correo Electrónico',
                'estadoNotificado': 'Estado', 'nombre_evento': 'Evento',
                'fecha_evento': 'Fecha Evento', 'nombre_facultad': 'Facultad',
                'nombre_escuela': 'Escuela', 'fecha_notificacion': 'Fecha Notificación'
            }, inplace=True)
            # ... (formatear fechas y N/A) ...
            if 'Fecha Evento' in df.columns:
                df['Fecha Evento'] = pd.to_datetime(df['Fecha Evento']).dt.strftime('%Y-%m-%d')
            if 'Fecha Notificación' in df.columns:
                df['Fecha Notificación'] = pd.to_datetime(df['Fecha Notificación']).dt.strftime('%Y-%m-%d %H:%M:%S')
            df['Facultad'] = df['Facultad'].fillna('N/A')
            df['Escuela'] = df['Escuela'].fillna('N/A')
            df['Fecha Notificación'] = df['Fecha Notificación'].fillna('N/A')

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Reporte_General')
            output.seek(0)

            return send_file(
                output,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name='reporte_general_participantes.xlsx'
            )
        except Exception as e:
            flash(f"Error al exportar a Excel: {e}", "warning")
            return redirect(url_for('index', tab='reporte-general'))
        
    @app.route('/export/eventos') # <-- NUEVA RUTA
    def export_excel_eventos():
        """
        Exporta la vista de Resumen de Eventos.
        """
        try:
            data = model.get_event_summary_view()
            if not data:
                flash("No hay datos de eventos para exportar.", "info")
                return redirect(url_for('index', tab='vistas'))

            df = pd.DataFrame(data)
            df.rename(columns={
                'nombre_evento': 'Nombre del Evento',
                'fecha': 'Fecha',
                'numero_participantes': 'Nro. de Participantes'
            }, inplace=True)
            
            df['Fecha'] = pd.to_datetime(df['Fecha']).dt.strftime('%Y-%m-%d')

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Resumen_Eventos')
            output.seek(0)
            
            return send_file(
                output,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name='resumen_eventos.xlsx'
            )
        except Exception as e:
            flash(f"Error al exportar eventos: {e}", "warning")
            return redirect(url_for('index', tab='vistas'))


    @app.route('/export/participantes') # <-- NUEVA RUTA
    def export_excel_participantes():
        """
        Exporta la vista de Todos los Participantes.
        """
        try:
            data = model.get_all_participants_view()
            if not data:
                flash("No hay datos de participantes para exportar.", "info")
                return redirect(url_for('index', tab='vistas'))

            df = pd.DataFrame(data)
            df.rename(columns={
                'nombresCompleto': 'Nombres Completos',
                'correo': 'Correo Electrónico',
                'nombre_evento': 'Evento'
            }, inplace=True)

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Total_Participantes')
            output.seek(0)
            
            return send_file(
                output,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name='total_participantes.xlsx'
            )
        except Exception as e:
            flash(f"Error al exportar participantes: {e}", "warning")
            return redirect(url_for('index', tab='vistas'))
    
    @app.route('/upload-excel', methods=['POST'])
    def upload_excel():
        """
        Lógica de carga de Excel simplificada con DEPURACIÓN y corrección 'nan'.
        """
        print("\n--- [DEBUG] INICIANDO upload_excel ---")
        
        if 'excel_file' not in request.files:
            flash('No se encontró ningún archivo', 'warning')
            print("DEBUG: Error - No se encontró 'excel_file' en request.files")
            return redirect(url_for('index', tab='administrar'))
        
        file = request.files['excel_file']
        evento_id = request.form['evento_id']
        
        if file.filename == '' or not evento_id:
            flash('No se seleccionó archivo o evento de destino', 'warning')
            print(f"DEBUG: Error - Filename vacío o evento_id no provisto (Evento: {evento_id})")
            return redirect(url_for('index', tab='administrar'))
        
        if file:
            try:
                df = pd.read_excel(file)
                print(f"DEBUG: Excel leído. {len(df)} filas encontradas.")
                
                if 'NombresCompletos' not in df.columns or 'CorreoElectronico' not in df.columns:
                    flash("Error: El archivo Excel debe tener las columnas 'NombresCompletos' y 'CorreoElectronico'", 'warning')
                    print("DEBUG: Error - Columnas requeridas no encontradas.")
                    return redirect(url_for('index', tab='administrar'))

                success_count = 0
                fail_count = 0
                
                # --- Cargar mapas ANTES del bucle ---
                print("DEBUG: Cargando mapas de traducción...")
                facultad_map = model.get_all_facultades_map()
                escuela_map = model.get_all_escuelas_map()
                
                print(f"DEBUG: Mapa de Facultades cargado. {len(facultad_map)} items.")
                print(f"DEBUG: Mapa de Escuelas cargado. {len(escuela_map)} items.")
                
                has_facultad_col = 'Facultad' in df.columns
                has_escuela_col = 'Escuela' in df.columns
                print(f"DEBUG: Columna 'Facultad' existe en Excel: {has_facultad_col}")
                print(f"DEBUG: Columna 'Escuela' existe en Excel: {has_escuela_col}")

                for index, row in df.iterrows():
                    print(f"\n--- [DEBUG] Procesando Fila {index + 2} ---")
                    
                    nombres = str(row['NombresCompletos'])
                    correo = str(row['CorreoElectronico'])
                    print(f"DEBUG: Nombre='{nombres}', Correo='{correo}'")
                    
                    facultad_id_final = None
                    escuela_id_final = None
                    valid_row = True
                    
                    facu_id_from_excel = None 
                    facu_id_from_escu_db = None 
                    
                    # --- 1. Procesar la columna 'escuela' (CON FIX 'NAN') ---
                    nombre_escuela_raw = ""
                    if has_escuela_col:
                        nombre_escuela_raw = str(row.get('Escuela', '')).strip()
                    print(f"DEBUG: Leyendo 'Escuela': '{nombre_escuela_raw}'")

                    nombre_busqueda_escuela = nombre_escuela_raw.upper()
                    
                    # ¡CORRECCIÓN! Solo buscar si NO está vacío y NO es 'NAN'
                    if nombre_escuela_raw and nombre_busqueda_escuela != 'NAN':
                        print(f"DEBUG: Buscando escuela en mapa: '{nombre_busqueda_escuela}'")
                        escuela_info = escuela_map.get(nombre_busqueda_escuela)
                        print(f"DEBUG: Resultado búsqueda escuela: {escuela_info}")
                        
                        if escuela_info:
                            escuela_id_final = escuela_info['idEscuela']
                            # Usando la llave de tu log
                            facu_id_from_escu_db = escuela_info.get('fk_idFacultad') 
                            print(f"DEBUG: Escuela encontrada. idEscuela={escuela_id_final}, idFacultad_detectada={facu_id_from_escu_db}")
                        else:
                            print("DEBUG: FALLA (A) - Nombre de escuela no encontrado en la BD.")
                            valid_row = False 
                    
                    # --- 2. Procesar la columna 'facultad' (CON FIX 'NAN') ---
                    nombre_facultad_raw = ""
                    if has_facultad_col:
                        nombre_facultad_raw = str(row.get('Facultad', '')).strip()
                    print(f"DEBUG: Leyendo 'Facultad': '{nombre_facultad_raw}'")

                    nombre_busqueda_facultad = nombre_facultad_raw.upper()
                    
                    # ¡CORRECCIÓN! Solo buscar si NO está vacío y NO es 'NAN'
                    if nombre_facultad_raw and nombre_busqueda_facultad != 'NAN':
                        print(f"DEBUG: Buscando facultad en mapa: '{nombre_busqueda_facultad}'")
                        facu_id_from_excel = facultad_map.get(nombre_busqueda_facultad)
                        print(f"DEBUG: Resultado búsqueda Facultad: {facu_id_from_excel}")
                        
                        if not facu_id_from_excel:
                            print("DEBUG: FALLA (B) - Nombre de Facultad no encontrado en la BD.")
                            valid_row = False

                    # --- 3. Validar y Reconciliar los IDs ---
                    print("DEBUG: Iniciando validación de IDs...")
                    
                    if not valid_row:
                        print(f"DEBUG: FALLA (C) - Fila invalidada por búsqueda fallida (A o B).")
                        fail_count += 1
                        continue # Saltar a la siguiente fila

                    # Error 2: Conflicto
                    if facu_id_from_excel and facu_id_from_escu_db and facu_id_from_excel != facu_id_from_escu_db:
                        print(f"DEBUG: FALLA (D) - Conflicto de IDs. Facultad Excel ({facu_id_from_excel}) != Facultad de Escuela en BD ({facu_id_from_escu_db})")
                        fail_count += 1
                        continue 
                    
                    # Error 3: (Tu requisito)
                    if escuela_id_final and not facu_id_from_escu_db and not facu_id_from_excel:
                        print(f"DEBUG: FALLA (E) - Se proveyó escuela, pero no tiene facultad en BD y no se proveyó facultad en Excel.")
                        fail_count += 1
                        continue 

                    # --- 4. Asignación Final ---
                    facultad_id_final = facu_id_from_excel or facu_id_from_escu_db
                    
                    print(f"DEBUG: IDs Finales Asignados: idFacultad={facultad_id_final}, idEscuela={escuela_id_final}")
                    
                    # --- 5. Insertar en la Base de Datos ---
                    print(f"DEBUG: Llamando a model.add_new_participant(...) con evento_id={evento_id}")
                    
                    # Asumo que tu función devuelve (bool, str) para el log
                    success, message = model.add_new_participant(
                        nombres, correo, evento_id, 
                        facultad_id_final, # Puede ser None
                        escuela_id_final   # Puede ser None
                    )
                    
                    if success:
                        print("DEBUG: Inserción Exitosa.")
                        success_count += 1
                    else:
                        print(f"DEBUG: FALLA (F) - model.add_new_participant retornó Falso. Mensaje: {message}")
                        fail_count += 1
                        
                print(f"\nDEBUG: Proceso finalizado. Success={success_count}, Fail={fail_count}")
                flash(f"Importación completada: {success_count} agregados, {fail_count} fallaron.", 'success' if success_count > 0 else 'warning')
            
            except Exception as e:
                print(f"DEBUG: FALLA (GLOBAL) - Ocurrió una excepción: {e}")
                flash(f"Error al procesar el archivo: {e}", 'warning')
                
        return redirect(url_for('index', tab='administrar'))
    
    
    return app

if __name__ == '__main__':
    app = crear_app()
    app.run(debug=True)