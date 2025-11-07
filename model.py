import mysql.connector
import config

def get_db_connection():
    """
    Crea y devuelve una conexión a la base de datos.
    """
    try:
        conn = mysql.connector.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error en la conexión a la BD: {err}")
        return None

# --- Definición de Consultas ---

def get_24h_rolling_sent_count():
    """
    Cuenta cuántos participantes fueron notificados
    en las ÚLTIMAS 24 HORAS exactas (ventana continua).
    """
    query = """
    SELECT COUNT(idLog_participanteNotificado) AS total_24h
    FROM Log_participantesNotificados
    WHERE fecha > (NOW() - INTERVAL 24 HOUR);
    """
    conn = get_db_connection()
    if not conn:
        return 0
        
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            return result['total_24h']
        return 0
    except mysql.connector.Error as err:
        print(f"Error al contar logs de 24h: {err}")
        return 0
    finally:
        cursor.close()
        conn.close()


def get_unnotified_participants(limit_amount):
    """
    Obtiene un LOTE de participantes no notificados,
    usando un límite dinámico.
    """
    if limit_amount <= 0:
        return [] # No pidas nada a la BD si el límite es 0
        
    query = """
    SELECT 
        p.idParticipante, 
        p.nombresCompleto, 
        p.correo, 
        e.nombre AS nombre_evento
    FROM 
        Participantes p
    JOIN 
        Eventos e ON p.fk_idEvento = e.idEvento
    WHERE 
        p.estadoNotificado = 'no'
    LIMIT %s;
    """
    conn = get_db_connection()
    if not conn:
        return []
    
    cursor = conn.cursor(dictionary=True) 
    try:
        cursor.execute(query, (limit_amount,)) # Pasamos el límite dinámico
        participants = cursor.fetchall()
        return participants
    except mysql.connector.Error as err:
        print(f"Error al obtener participantes: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

def update_participant_status(participant_id):
    """
    Consulta 2: Actualiza el estado de un participante a 'si'.
    Esto debería disparar tu Trigger existente para llenar la tabla Log.
    """
    query = "UPDATE Participantes SET estadoNotificado = 'si' WHERE idParticipante = %s"
    
    conn = get_db_connection()
    if not conn:
        return False
        
    cursor = conn.cursor()
    try:
        cursor.execute(query, (participant_id,))
        conn.commit() # Importante: confirmar la transacción
        return True
    except mysql.connector.Error as err:
        print(f"Error al actualizar estado: {err}")
        conn.rollback() # Revertir si hay error
        return False
    finally:
        cursor.close()
        conn.close()
        
def get_all_events():
    """
    Consulta 4: Obtiene TODOS los eventos para un menú desplegable.
    """
    query = "SELECT idEvento, nombre FROM Eventos ORDER BY nombre ASC"
    conn = get_db_connection()
    if not conn:
        return []
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query)
        events = cursor.fetchall()
        return events
    except mysql.connector.Error as err:
        print(f"Error al obtener todos los eventos: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

def add_new_event(nombre, fecha):
    """
    Consulta 5: Inserta un nuevo evento en la BD.
    """
    query = "INSERT INTO Eventos (nombre, fecha) VALUES (%s, %s)"
    conn = get_db_connection()
    if not conn:
        return False, "Error de conexión a la BD"
        
    cursor = conn.cursor()
    try:
        cursor.execute(query, (nombre, fecha))
        conn.commit()
        return True, "Evento agregado"
    except mysql.connector.Error as err:
        print(f"Error al agregar evento: {err}")
        conn.rollback()
        return False, f"Error de BD: {err}"
    finally:
        cursor.close()
        conn.close()

def add_new_participant(nombres, correo, id_evento, id_facultad=None, id_escuela=None):
    """
    Inserta un participante y, opcionalmente, sus relaciones
    en las nuevas tablas de unión, usando una transacción.
    """
    conn = get_db_connection()
    if not conn:
        return False, "Error de conexión a la BD"
        
    cursor = conn.cursor()
    try:
        # Iniciar transacción
        conn.start_transaction()
        
        # 1. Insertar el participante principal
        query_part = """
        INSERT INTO Participantes (nombresCompleto, correo, estadoNotificado, fk_idEvento) 
        VALUES (%s, %s, 'no', %s)
        """
        cursor.execute(query_part, (nombres, correo, id_evento))
        
        # 2. Obtener el ID del participante que acabamos de crear
        id_nuevo_participante = cursor.lastrowid
        
        # 3. Si se proporcionó id_facultad, insertarlo
        if id_facultad:
            query_fac = "INSERT INTO ParticipantesFacultades (fk_idFacultad, fk_idParticipante) VALUES (%s, %s)"
            cursor.execute(query_fac, (id_facultad, id_nuevo_participante))
            
        # 4. Si se proporcionó id_escuela, insertarlo
        if id_escuela:
            query_esc = "INSERT INTO ParticipantesEscuelas (fk_idEscuela, fk_idParticipante) VALUES (%s, %s)"
            cursor.execute(query_esc, (id_escuela, id_nuevo_participante))

        # 5. Confirmar todos los cambios
        conn.commit()
        return True, "Participante agregado"
        
    except mysql.connector.Error as err:
        print(f"Error al agregar participante: {err}")
        # Si algo falla, revertir TODOS los cambios de esta transacción
        conn.rollback()
        return False, f"Error de BD: {err}"
    finally:
        cursor.close()
        conn.close()
        
def get_all_facultades():
    """
    Obtiene todas las facultades para los menús desplegables.
    """
    query = "SELECT idFacultad, nombreFacultad FROM Facultades ORDER BY nombreFacultad ASC"
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error al obtener facultades: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_all_escuelas():
    """
    Ahora también obtiene el fk_idFacultad
    para usarlo en el JavaScript de los menús dependientes.
    """
    query = "SELECT idEscuela, nombreEscuela, fk_idFacultad FROM Escuelas ORDER BY nombreEscuela ASC"
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query)
        return cursor.fetchall()  # Ahora incluirá fk_idFacultad
    except mysql.connector.Error as err:
        print(f"Error al obtener escuelas: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

# model.py

def get_participant_report(search_term=None, filter_facultad=None, filter_escuela=None, 
                           date_start=None, date_end=None, 
                           noti_date_start=None, noti_date_end=None): # <-- NUEVOS PARÁMETROS
    """
    filtros de rango de fechas para la FECHA DE NOTIFICACIÓN
    (noti_date_start y noti_date_end).
    """
    params = []
    
    query = """
    SELECT 
        p.nombresCompleto, 
        p.correo, 
        p.estadoNotificado, 
        e.nombre AS nombre_evento,
        e.fecha AS fecha_evento,
        COALESCE(f_esc.nombreFacultad, f_part.nombreFacultad) AS nombre_facultad,
        es.nombreEscuela AS nombre_escuela,
        log.fecha_notificacion
    FROM Participantes p
    JOIN Eventos e ON p.fk_idEvento = e.idEvento
    LEFT JOIN ParticipantesEscuelas pe ON p.idParticipante = pe.fk_idParticipante
    LEFT JOIN Escuelas es ON pe.fk_idEscuela = es.idEscuela
    LEFT JOIN Facultades f_esc ON es.fk_idFacultad = f_esc.idFacultad
    LEFT JOIN ParticipantesFacultades pf ON p.idParticipante = pf.fk_idParticipante
    LEFT JOIN Facultades f_part ON pf.fk_idFacultad = f_part.idFacultad
    LEFT JOIN (
        SELECT correo, MAX(fecha) as fecha_notificacion 
        FROM Log_participantesNotificados 
        GROUP BY correo
    ) log ON p.correo = log.correo
    """
    
    where_clauses = []
    
    # Filtro: Nombre
    if search_term and search_term.strip():
        where_clauses.append("p.nombresCompleto LIKE %s")
        params.append(f"%{search_term.strip()}%")
        
    # Filtro: Facultad
    if filter_facultad and filter_facultad.strip():
        where_clauses.append("(f_esc.idFacultad = %s OR f_part.idFacultad = %s)")
        params.append(filter_facultad)
        params.append(filter_facultad)
        
    # Filtro: Escuela
    if filter_escuela and filter_escuela.strip():
        where_clauses.append("es.idEscuela = %s")
        params.append(filter_escuela)
        
    # Filtro: Fecha de EVENTO
    if date_start and date_start.strip():
        where_clauses.append("e.fecha >= %s")
        params.append(date_start)
    if date_end and date_end.strip():
        where_clauses.append("e.fecha <= %s")
        params.append(date_end)
        
    # Nota: Estos filtros solo mostrarán participantes que SÍ han sido notificados
    # y que caen dentro de este rango.
    if noti_date_start and noti_date_start.strip():
        where_clauses.append("log.fecha_notificacion >= %s")
        params.append(noti_date_start)
    if noti_date_end and noti_date_end.strip():
        where_clauses.append("log.fecha_notificacion <= %s")
        params.append(noti_date_end)
        
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
        
    query += " ORDER BY p.nombresCompleto ASC LIMIT 500"
    
    conn = get_db_connection()
    if not conn:
        return []
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error al generar reporte de participantes: {err}")
        return []
    finally:
        cursor.close()
        conn.close()
        
def get_all_facultades_map():
    facultades_map = {}
    
    conn = get_db_connection()
    if not conn:
        print("Error cargando mapa de facultades: No se pudo conectar a la BD.")
        return {}
        
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT idFacultad, nombreFacultad FROM Facultades")
        
        rows = cursor.fetchall() 
        
        for row in rows:
            nombre_limpio = str(row['nombreFacultad']).strip().upper()
            facultades_map[nombre_limpio] = row['idFacultad']
            
        return facultades_map
        
    except mysql.connector.Error as e:
        print(f"Error cargando mapa de facultades: {e}")
        return {}
        
    finally:
        cursor.close()
        conn.close()

def get_all_escuelas_map():
    escuelas_map = {}
    
    conn = get_db_connection()
    if not conn:
        print("Error cargando mapa de escuelas: No se pudo conectar a la BD.")
        return {}

    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT idEscuela, nombreEscuela, fk_idFacultad FROM Escuelas") 
        
        rows = cursor.fetchall()
        
        for row in rows:
            nombre_limpio = str(row['nombreEscuela']).strip().upper()
            escuelas_map[nombre_limpio] = {
                'idEscuela': row['idEscuela'],
                'fk_idFacultad': row['fk_idFacultad']
            }
        
        return escuelas_map
        
    except mysql.connector.Error as e:
        print(f"Error cargando mapa de escuelas: {e}")
        return {}
        
    finally:
        cursor.close()
        conn.close()