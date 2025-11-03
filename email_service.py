# email_service.py
import smtplib
import ssl
from email.message import EmailMessage
import config

def send_notification_email(participant_data):
    """
    Envía un correo de notificación al participante.
    participant_data debe ser un diccionario de la consulta (modelo).
    """
    try:
        msg = EmailMessage()
        msg['Subject'] = f"Certificado Disponible: {participant_data['nombre_evento']}"
        # Usamos el remitente real que definiste
        msg['From'] = f"Incubadora de Empresas <{config.EMAIL_REMITENTE_REAL}>"
        msg['To'] = participant_data['correo']
        
        # Le dice al cliente de correo a dónde enviar las respuestas.
        msg['Reply-To'] = config.EMAIL_REMITENTE_REAL
        
        # Cuerpo del correo (puedes mejorarlo con HTML si quieres)
        body = f"""
        Hola {participant_data['nombresCompleto']},

        Te notificamos que tu certificado por participar en el evento "{participant_data['nombre_evento']}" ya está listo para ser recogido.

        Puedes acercarte a la siguiente dirección:
        {config.DIRECCION_RECOJO}

        ¡Gracias por tu participación!

        Atentamente,
        El equipo de la Incubadora.
        """
        msg.set_content(body)

        # Envío del correo usando Gmail y SSL
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(config.GMAIL_USER, config.GMAIL_APP_PASSWORD)
            server.send_message(msg)
        
        print(f"Correo enviado exitosamente a {participant_data['correo']}")
        return True
    except Exception as e:
        print(f"Error al enviar correo a {participant_data['correo']}: {e}")
        return False