# model.py
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
    Consulta 2 (CORREGIDA): Cuenta cuántos participantes fueron notificados
    en las ÚLTIMAS 24 HORAS exactas (ventana continua).
    """
    query = """
    SELECT COUNT(idLog_perticipanteNotificado) AS total_24h
    FROM Log_perticipantesNotificados
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
    Consulta 1: Obtiene un LOTE de participantes no notificados,
    usando un límite dinámico.
    """
    if limit_amount <= 0:
        return [] # No pidas nada a la BD si el límite es 0
        
    query = """
    SELECT 
        p.idPerticipante, 
        p.nombresCompleto, 
        p.correo, 
        e.nombre AS nombre_evento
    FROM 
        Perticipantes p
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
    query = "UPDATE Perticipantes SET estadoNotificado = 'si' WHERE idPerticipante = %s"
    
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
        
def get_notification_log(search_term=None, limit_amount=200):
    """
    Consulta 3 (Actualizada): Obtiene el Log de notificaciones,
    con filtrado de búsqueda opcional.
    """
    params = []
    
    # Construcción dinámica de la consulta
    query_parts = [
        "SELECT nombre, correo, fecha",
        "FROM Log_perticipantesNotificados"
    ]
    
    # Si hay un término de búsqueda, añadimos un WHERE
    if search_term and search_term.strip():
        query_parts.append("WHERE nombre LIKE %s")
        params.append(f"%{search_term.strip()}%") # % para búsqueda parcial
        
    query_parts.append("ORDER BY fecha DESC")
    
    # Añadimos el límite
    query_parts.append("LIMIT %s")
    params.append(limit_amount)

    # Unimos todo
    final_query = " ".join(query_parts)
    
    conn = get_db_connection()
    if not conn:
        return []
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(final_query, tuple(params))
        logs = cursor.fetchall()
        return logs
    except mysql.connector.Error as err:
        print(f"Error al obtener log de notificaciones: {err}")
        return []
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
        INSERT INTO Perticipantes (nombresCompleto, correo, estadoNotificado, fk_idEvento) 
        VALUES (%s, %s, 'no', %s)
        """
        cursor.execute(query_part, (nombres, correo, id_evento))
        
        # 2. Obtener el ID del participante que acabamos de crear
        id_nuevo_participante = cursor.lastrowid
        
        # 3. Si se proporcionó id_facultad, insertarlo
        if id_facultad:
            query_fac = "INSERT INTO ParticipanteFacultad (fk_idFacultad, fk_idParticipante) VALUES (%s, %s)"
            cursor.execute(query_fac, (id_facultad, id_nuevo_participante))
            
        # 4. Si se proporcionó id_escuela, insertarlo
        if id_escuela:
            query_esc = "INSERT INTO ParticipanteEscuela (fk_idEscuela, fk_idParticipante) VALUES (%s, %s)"
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
    Obtiene todas las escuelas para los menús desplegables.
    """
    query = "SELECT idEscuela, nombreEscuela FROM Escuelas ORDER BY nombreEscuela ASC"
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error al obtener escuelas: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_participant_report(search_term=None, filter_facultad=None, filter_escuela=None):
    """
    Genera un reporte completo de participantes con todos los filtros.
    """
    params = []
    
    # Esta consulta es compleja:
    # 1. Obtiene el participante (p) y su evento (e).
    # 2. (pe, es, f_esc) Obtiene la escuela (es) y la facultad (f_esc) a la que pertenece esa escuela.
    # 3. (pf, f_part) Obtiene la facultad (f_part) si está asignada directamente al participante.
    # 4. COALESCE da prioridad a la facultad de la escuela, si no, usa la facultad directa.
    
    query = """
    SELECT 
        p.nombresCompleto, 
        p.correo, 
        p.estadoNotificado, 
        e.nombre AS nombre_evento,
        COALESCE(f_esc.nombreFacultad, f_part.nombreFacultad) AS nombre_facultad,
        es.nombreEscuela AS nombre_escuela
    FROM Perticipantes p
    JOIN Eventos e ON p.fk_idEvento = e.idEvento
    LEFT JOIN ParticipanteEscuela pe ON p.idPerticipante = pe.fk_idParticipante
    LEFT JOIN Escuelas es ON pe.fk_idEscuela = es.idEscuela
    LEFT JOIN Facultades f_esc ON es.fk_idFacultad = f_esc.idFacultad
    LEFT JOIN ParticipanteFacultad pf ON p.idPerticipante = pf.fk_idParticipante
    LEFT JOIN Facultades f_part ON pf.fk_idFacultad = f_part.idFacultad
    """
    
    where_clauses = []
    
    if search_term and search_term.strip():
        where_clauses.append("p.nombresCompleto LIKE %s")
        params.append(f"%{search_term.strip()}%")
        
    if filter_facultad and filter_facultad.strip():
        # Filtra por CUALQUIERA de las dos rutas de facultad
        where_clauses.append("(f_esc.idFacultad = %s OR f_part.idFacultad = %s)")
        params.append(filter_facultad)
        params.append(filter_facultad)
        
    if filter_escuela and filter_escuela.strip():
        where_clauses.append("es.idEscuela = %s")
        params.append(filter_escuela)
        
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
        
    query += " ORDER BY p.nombresCompleto ASC LIMIT 500" # Límite para la vista web
    
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