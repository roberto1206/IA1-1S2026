import os
import requests
from dotenv import load_dotenv

load_dotenv()

class TelegramService:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def send_message(self, message): 
        if not self.token or not self.chat_id:
            print("Telegram token or chat ID not found in environment variables.")
            return False
        
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message
        }

        response = requests.post(url, data=payload)

        if response.status_code != 200:
            print(f"Error sending message to Telegram: {response.status_code}")
            return False
        else:
            print("Message sent to Telegram successfully.")
        return True