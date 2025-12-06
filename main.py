import json
import requests
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class RecruitmentAIFunction:
    def __init__(self):
        self.giga_api_key = os.getenv("YANDEX_API_KEY")
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        logger.info("✅ AI Recruitment Function initialized")
    
    def parse_resume(self, resume_text: str) -> dict:
        """Парсинг резюме - упрощённая версия"""
        logger.info("Parsing resume...")
        return {
            "name": "Максим Иванов",
            "hard_skills": ["Go", "Python", "Kubernetes", "Docker", "PostgreSQL"],
            "experience_years": 7,
            "status": "parsed"
        }
    
    def send_telegram(self, chat_id: str, message: str) -> dict:
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info("✅ Message sent")
                return {"status": "SENT", "message_id": response.json()['result']['message_id']}
            else:
                return {"status": "FAILED", "error": response.text}
        except Exception as e:
            return {"status": "FAILED", "error": str(e)}
