# 📄 email_sender.py

import smtplib
from email.message import EmailMessage

# --- 1. CONFIGURACIÓN ---
# V Reemplaza con tus datos reales V

GMAIL_USER = "yjru23@gmail.com"
GMAIL_APP_PASSWORD = "dzpq ynxu ujti bjmf" # <-- ¡Usa la Contraseña de Aplicación de 16 letras!

# V Configuración del Mensaje V
DIRECCION_RECOJO = "Av. Siempre Viva 123, Oficina 404, Incubadora de Empresas"
EMAIL_REMITENTE_REAL = "incubadora@universidad.edu.pe" # El correo de la incubadora


# --- 2. FUNCIÓN DE ENVÍO ---

def enviar_correo(destinatario_email, destinatario_nombre, nombre_evento):
    """
    Construye y envía un correo individual usando el servidor SMTP de Gmail.
    """
    
    # --- Asunto y Cuerpo del Mensaje ---
    asunto = f"¡Tu certificado del evento '{nombre_evento}' está listo!"
    
    # Usamos f-strings para personalizar el mensaje
    cuerpo = f"""
    Hola {destinatario_nombre},

    ¡Buenas noticias!

    Te informamos que tu certificado de participación por el evento "{nombre_evento}" 
    ya se encuentra impreso y listo para ser recogido.

    Puedes acercarte a la siguiente dirección:
    {DIRECCION_RECOJO}

    Horario de atención: Lunes a Viernes de 9:00 a.m. a 5:00 p.m.

    ¡Te esperamos!

    Saludos,
    El equipo de la Incubadora de Empresas.
    """

    # --- Creación del objeto Email ---
    msg = EmailMessage()
    msg['Subject'] = asunto
    msg['From'] = GMAIL_USER
    msg['To'] = destinatario_email
    
    # El truco: El correo se envía desde GMAIL_USER, 
    # pero si responden, le llegará al correo institucional.
    msg['Reply-To'] = EMAIL_REMITENTE_REAL
    
    msg.set_content(cuerpo)

    # --- Envío por SMTP de Gmail ---
    try:
        # Nos conectamos de forma segura al servidor de Gmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD) # Usa tus credenciales
            smtp.send_message(msg)
        
        print(f"Correo enviado exitosamente a {destinatario_email}")
        return True
    except Exception as e:
        print(f"Error al enviar correo a {destinatario_email}: {e}")
        return False