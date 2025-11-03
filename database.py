# 📄 database.py

import mysql.connector
import os

# --- CONFIGURACIÓN DE BD ---
DB_HOST = os.getenv("DB_HOST", "mysql-yusurus.alwaysdata.net")
DB_USER = os.getenv("DB_USER", "yusurus_sms")
DB_PASSWORD = os.getenv("DB_PASSWORD", "12admin34")
DB_NAME = os.getenv("DB_NAME", "yusurus_enviar_email")
DB_PORT = int(os.getenv("DB_PORT", "3306"))

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
    """
    Obtiene los asistentes que tienen certificados listos (estado_certificado = 'Listo')
    pero que AÚN NO han sido notificados (notificado = 0).
    """
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                a.id_asistente, a.nombre_completo, a.email, e.nombre_evento, 
                a.estado_certificado, a.notificado
            FROM 
                Asistentes a
            JOIN 
                Eventos e ON a.id_evento_fk = e.id_evento
            WHERE 
                a.estado_certificado = 'listo_para_recoger' 
                AND a.notificado = 0
            ORDER BY 
                a.id_asistente;
        """
        cursor.execute(query)
        asistentes = cursor.fetchall()
        cursor.close()
        conn.close()
        return asistentes
    except mysql.connector.Error as err:
        print(f"Error al obtener asistentes para notificar: {err}")
        if conn:
            conn.close()
        return []

def marcar_asistente_como_notificado(id_asistente):
    """
    Marca a un asistente como notificado (notificado = 1) después de enviarle el correo.
    """
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        query = """
            UPDATE Asistentes 
            SET notificado = 1 
            WHERE id_asistente = %s;
        """
        cursor.execute(query, (id_asistente,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error al marcar asistente {id_asistente} como notificado: {err}")
        if conn:
            conn.rollback()
            conn.close()
        return False

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