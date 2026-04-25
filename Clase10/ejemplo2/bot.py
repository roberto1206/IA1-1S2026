# https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Error al enviar el mensaje")
    else:
        print("Mensaje enviado correctamente")

send_message("Todos tienen 0 xD")