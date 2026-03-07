import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from services.bitacora import Bitacora


class Correo:
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_user: str,
        smtp_password: str,
        email_from: str,
        bitacora: Bitacora,
    ) -> None:
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.email_from = email_from
        self.bitacora = bitacora

    def enviar(self, destinatario: str, nombre: str) -> bool:
        asunto = "Recordatorio de pago pendiente"
        cuerpo = f"""
Hola {nombre},

Le recordamos que actualmente registra un pago pendiente en nuestro sistema.
Le recomendamos realizar su gestión a la brevedad para evitar inconvenientes.

Este mensaje fue enviado automáticamente por nuestro sistema de notificaciones.

Saludos cordiales,
Departamento de Atención al Cliente
"""

        mensaje = MIMEMultipart()
        mensaje["From"] = self.email_from
        mensaje["To"] = destinatario
        mensaje["Subject"] = asunto
        mensaje.attach(MIMEText(cuerpo, "plain", "utf-8"))

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as servidor:
                servidor.starttls()
                servidor.login(self.smtp_user, self.smtp_password)
                servidor.sendmail(
                    self.email_from,
                    destinatario,
                    mensaje.as_string()
                )

            self.bitacora.escribir(
                f"Correo enviado correctamente a {nombre} <{destinatario}>"
            )
            return True

        except Exception as e:
            self.bitacora.escribir(
                f"Error al enviar correo a {nombre} <{destinatario}>: {e}"
            )
            return False
        
    def enviar_quebrado(self, destinatario: str, nombre: str) -> bool:
        asunto = "No mas prestamos!!"
        cuerpo = f"""
Hola {nombre},

usted esta quebrado, ya no le daremos mas dinero >:v

Este mensaje fue enviado automáticamente por nuestro sistema de notificaciones.

Saludos cordiales,
Departamento de Atención al Cliente
"""

        mensaje = MIMEMultipart()
        mensaje["From"] = self.email_from
        mensaje["To"] = destinatario
        mensaje["Subject"] = asunto
        mensaje.attach(MIMEText(cuerpo, "plain", "utf-8"))

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as servidor:
                servidor.starttls()
                servidor.login(self.smtp_user, self.smtp_password)
                servidor.sendmail(
                    self.email_from,
                    destinatario,
                    mensaje.as_string()
                )

            self.bitacora.escribir(
                f"Correo enviado correctamente a {nombre} <{destinatario}>, quebrado"
            )
            return True

        except Exception as e:
            self.bitacora.escribir(
                f"Error al enviar correo a {nombre} <{destinatario}>: {e}"
            )
            return False