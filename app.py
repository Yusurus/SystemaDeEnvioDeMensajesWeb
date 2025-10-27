from flask import Flask, render_template, request, redirect, url_for, flash
import database as db          # Importamos nuestro MODELO
import email_sender as mail    # Importamos nuestro SERVICIO

# Inicializamos Flask
app = Flask(__name__)
app.secret_key = 'tu-llave-secreta-para-mensajes-flash'

# --- RUTA 1: La página principal (GET) ---
# Esta es la función del CONTROLADOR que responde a la URL "/"
@app.route('/')
def index():
    """
    CONTROLADOR:
    1. (En el futuro, llamará al MODELO para pedir datos)
    2. Renderiza la VISTA 'index.html'.
    """
    # Por ahora, solo muestra la página.
    # Más adelante, aquí llamaremos a db.obtener_todos_los_asistentes()
    # y le pasaremos los datos a la plantilla.
    return render_template('index.html')

# --- RUTA 2: La acción de enviar (POST) ---
# Esta es la función del CONTROLADOR que responde al clic del botón
@app.route('/enviar-notificaciones', methods=['POST'])
def procesar_envio():
    """
    CONTROLADOR:
    1. Llama al MODELO (db.obtener_asistentes_para_notificar).
    2. Itera y llama al SERVICIO (mail.enviar_correo).
    3. Llama al MODELO de nuevo (db.marcar_asistente_como_notificado).
    4. Redirige de vuelta a la VISTA principal.
    """
    try:
        asistentes_a_notificar = db.obtener_asistentes_para_notificar()
        
        if not asistentes_a_notificar:
            flash("No hay certificados nuevos para notificar.", "info")
            return redirect(url_for('index'))

        enviados_count = 0
        for asistente in asistentes_a_notificar:
            exito = mail.enviar_correo(
                destinatario_email=asistente['email'],
                destinatario_nombre=asistente['nombre_completo'],
                nombre_evento=asistente['nombre_evento']
            )
            if exito:
                db.marcar_asistente_como_notificado(asistente['id_asistente'])
                enviados_count += 1
        
        flash(f"¡Proceso completado! Se enviaron {enviados_count} notificaciones.", "success")
    
    except Exception as e:
        flash(f"Error crítico durante el envío: {e}", "error")

    return redirect(url_for('index'))


# --- Punto de entrada para ejecutar la app ---
if __name__ == '__main__':
    app.run(debug=True)