# 📄 database.py

import mysql.connector

# --- CONFIGURACIÓN DE BD ---
DB_HOST = "mysql-yusurus.alwaysdata.net"
DB_USER = "yusurus_enviar_email"
DB_PASSWORD = "12admin34"
DB_NAME = "yusurus_enviar_email"

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return None

def obtener_asistentes_para_notificar():
    # ... (código de la función) ...
    pass

def marcar_asistente_como_notificado(id_asistente):
    # ... (código de la función) ...
    pass

# --- NUEVA FUNCIÓN QUE NECESITAREMOS ---
def obtener_todos_los_asistentes():
    """
    Obtiene TODOS los asistentes para mostrarlos en una tabla en la web.
    """
    conn = get_db_connection()
    if not conn:
        return []
    
    cursor = conn.cursor(dictionary=True)
    # Un query más completo para ver todo
    query = """
        SELECT 
            a.id_asistente, a.nombre_completo, a.email, e.nombre_evento, 
            a.estado_certificado, a.notificado
        FROM 
            Asistentes a
        JOIN 
            Eventos e ON a.id_evento_fk = e.id_evento
        ORDER BY 
            a.id_asistente DESC;
    """
    cursor.execute(query)
    asistentes = cursor.fetchall()
    cursor.close()
    conn.close()
    return asistentes