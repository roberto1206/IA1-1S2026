# pip install python-dotenv

import os
from dotenv import load_dotenv

from services.bitacora import Bitacora
from services.correo import Correo
from robots.robot_notificador import RobotNotificador

load_dotenv()


def main() -> None:
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    email_from = os.getenv("EMAIL_FROM", smtp_user)

    archivo_clientes = "clientes.txt"
    archivo_bitacora = "bitacora_envios.txt"

    bitacora = Bitacora(archivo_bitacora)
    correo = Correo(
        smtp_host=smtp_host,
        smtp_port=smtp_port,
        smtp_user=smtp_user,
        smtp_password=smtp_password,
        email_from=email_from,
        bitacora=bitacora,
    )
    robot = RobotNotificador(
        archivo_clientes=archivo_clientes,
        correo=correo,
        bitacora=bitacora,
    )

    robot.procesar()


if __name__ == "__main__":
    main()