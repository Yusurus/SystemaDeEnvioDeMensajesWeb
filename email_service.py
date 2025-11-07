# email_service.py
import smtplib
import ssl
from email.message import EmailMessage
import config
from datetime import datetime

def send_notification_email(participant_data):
    """
    Envía un correo de notificación al participante usando una plantilla HTML.
    """
    try:
        msg = EmailMessage()
        msg['Subject'] = f"Certificado Disponible: {participant_data['nombre_evento']}"
        msg['From'] = f"Incubadora de Empresas <{config.EMAIL_REMITENTE_REAL}>"
        msg['To'] = participant_data['correo']
        msg['Reply-To'] = config.EMAIL_REMITENTE_REAL
        
        # --- 1. Mensaje de Texto Plano (Fallback) ---
        # Este es el respaldo para clientes de correo que no soportan HTML
        plain_text_body = f"""
        Hola {participant_data['nombresCompleto']},

        ¡Felicitaciones! Te notificamos que tu certificado por participar en el evento "{participant_data['nombre_evento']}" ya está listo para ser recogido.

        Detalles de recojo:
        Dirección: {config.DIRECCION_RECOJO}
        Horario: Lunes a Viernes de 9:00 AM a 1:00 PM - 2:00 PM a 4:00 PM

        ¡Gracias por tu participación!

        Atentamente,
        El equipo de la Incubadora.
        """
        msg.set_content(plain_text_body)

        # --- 2. Mensaje HTML (La versión principal) ---
        # Elige una de las dos plantillas de abajo (Opción A u Opción B)
        # y ponla aquí. He puesto la "Opción A" como ejemplo.
        
        html_body = plantilla_opcion_a(
            participant_data['nombresCompleto'],
            participant_data['nombre_evento'],
            config.DIRECCION_RECOJO
        )
        
        # --- 3. Adjuntar el HTML al mensaje ---
        # Esta es la línea clave que "mejora" el correo
        msg.add_alternative(html_body, subtype='html')

        # --- 4. Envío del correo ---
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(config.GMAIL_USER, config.GMAIL_APP_PASSWORD)
            server.send_message(msg)
        
        print(f"Correo HTML enviado exitosamente a {participant_data['correo']}")
        return True
    except Exception as e:
        print(f"Error al enviar correo a {participant_data['correo']}: {e}")
        return False


# --- PLANTILLAS HTML ---
# (Puedes moverlas a su propio archivo .py si quieres)

def plantilla_opcion_a(nombre_completo, nombre_evento, direccion_recojo):
    """
    Plantilla A: Profesional y Limpia.
    Un diseño moderno y minimalista.
    """
    year = datetime.now().year
    # IMPORTANTE: Reemplaza [TU HORARIO DE ATENCIÓN AQUÍ]
    horario_atencion = "[Añade tu horario aquí, ej: Lunes a Viernes de 9:00 AM a 5:00 PM]"
    
    # IMPORTANTE: Reemplaza https://www.instagram.com/tulogoaqui_mx/?hl=en o elimina la línea <img>
    url_logo = "https://i.imgur.com/example.png" # Ejemplo, reemplaza esto

    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f7f6;">
        <div style="width: 90%; max-width: 600px; margin: 20px auto; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; background-color: #ffffff;">
            
            <div style="padding: 20px 30px; background-color: #f9f9f9; border-bottom: 1px solid #ddd; text-align: left;">
                <h2 style="margin: 0; color: #004a99;">Incubadora de Empresas</h2>
            </div>
            
            <div style="padding: 30px; line-height: 1.6; color: #333;">
                <p style="font-size: 18px;">Hola <strong>{nombre_completo}</strong>,</p>
                <h3 style="color: #004a99; font-size: 22px;">¡Felicitaciones! Tu certificado está listo.</h3>
                <p>Nos complace informarte que tu certificado físico por haber participado en el evento:</p>
                
                <p style="font-size: 1.2em; font-weight: bold; text-align: center; margin: 25px 0; padding: 15px; background-color: #f4f7f6; border-radius: 5px;">
                    "{nombre_evento}"
                </p>
                
                <p>Ya se encuentra disponible para ser recogido en nuestras oficinas.</p>

                <div style="background-color: #f4f7f6; padding: 25px; border-radius: 5px; margin-top: 25px; border-left: 5px solid #004a99;">
                    <strong style="font-size: 18px; color: #333;">Detalles de Recojo:</strong>
                    <p style="margin: 15px 0 0 0; font-size: 16px;">
                        <strong>Dirección:</strong><br>
                        {direccion_recojo}
                    </p>
                    <p style="margin: 15px 0 0 0; font-size: 16px;">
                        <strong>Horario de Atención:</strong><br>
                        {horario_atencion}
                    </p>
                </div>

                <p style="margin-top: 30px;">¡Gracias por tu valiosa participación!</p>
                <p>Atentamente,<br>El equipo de la Incubadora</p>
            </div>
            
            <div style="background-color: #f9f9f9; color: #777; padding: 20px 30px; text-align: center; font-size: 12px; border-top: 1px solid #ddd;">
                <p style="margin:0;">&copy; {year} Incubadora de Empresas. Todos los derechos reservados.</p>
            </div>
        </div>
    </body>
    </html>
    """

def plantilla_opcion_b(nombre_completo, nombre_evento, direccion_recojo):
    """
    Plantilla B: Más Gráfica con "Botón"
    Usa un botón falso para un llamado a la acción más fuerte.
    """
    year = datetime.now().year
    # IMPORTANTE: Reemplaza [TU HORARIO DE ATENCIÓN AQUÍ]
    horario_atencion = "[Añade tu horario aquí, ej: Lunes a Viernes de 9:00 AM a 5:00 PM]"

    # Codifica la dirección para un enlace de Google Maps
    url_direccion = direccion_recojo.replace(' ', '+').replace('"', '')

    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f1f1f1;">
        <table width="100%" border="0" cellspacing="0" cellpadding="0">
            <tr>
                <td align="center" style="padding: 20px;">
                    <table width="600" border="0" cellspacing="0" cellpadding="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                        
                        <tr>
                            <td align="center" style="padding: 40px 20px; background-color: #004a99; color: #ffffff;">
                                <h1 style="margin: 0; font-size: 28px;">Certificado Listo para Recojo</h1>
                            </td>
                        </tr>
                        
                        <tr>
                            <td style="padding: 40px 30px; color: #333; line-height: 1.7;">
                                <p style="font-size: 18px;">Hola <strong>{nombre_completo}</strong>,</p>
                                <p>¡Excelentes noticias! Tu certificado por la participación en el evento <strong>"{nombre_evento}"</strong> ya está impreso y listo para ti.</p>
                                
                                <p style="margin-top: 30px;">Puedes recogerlo en nuestra oficina:</p>
                                
                                <table border="0" cellspacing="0" cellpadding="0" style="margin: 25px auto;">
                                    <tr>
                                        <td align="center" style="background-color: #28a745; border-radius: 5px;">
                                            <a href="https://maps.google.com/?q={url_direccion}" target="_blank" style="color: #ffffff; text-decoration: none; font-size: 16px; font-weight: bold; padding: 14px 25px; display: inline-block;">
                                                Ver Dirección en el Mapa
                                            </a>
                                        </td>
                                    </tr>
                                </table>
                                
                                <p style="text-align: center; font-size: 14px; color: #555;">
                                    <strong>Dirección:</strong> {direccion_recojo}
                                    <br>
                                    <strong>Horario:</strong> {horario_atencion}
                                </p>
                                
                                <p style="margin-top: 30px;">¡Te esperamos!</p>
                                <p>El equipo de la Incubadora</p>
                            </td>
                        </tr>
                        
                        <tr>
                            <td align="center" style="padding: 20px 30px; background-color: #f9f9f9; color: #888; font-size: 12px;">
                                <p style="margin:0;">&copy; {year} Incubadora de Empresas.</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """