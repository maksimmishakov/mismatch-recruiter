import sys
import os
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(__file__))
load_dotenv()

from main import RecruitmentAIFunction

print("=" * 70)
print("🧪 ЛОКАЛЬНОЕ ТЕСТИРОВАНИЕ AI РЕКРУТИНГА")
print("=" * 70)

print("\n📍 Инициализация функции...")
ai_agent = RecruitmentAIFunction()
print("✅ Функция инициализирована!")

print("\n" + "=" * 70)
print("ТЕСТ 1️⃣ : ПАРСИНГ РЕЗЮМЕ")
print("=" * 70)

test_resume = """
Максим Иванов
Senior Backend Developer
Опыт работы: 7 лет

Компания: Яндекс
Должность: Lead Backend Developer

Технические навыки:
- Go (Golang)
- Python
- Kubernetes
- Docker
- PostgreSQL
"""

print(f"\n📄 Резюме кандидата:\n{test_resume}")
print("\n⏳ Парсирую резюме через Яндекс.Giga...")

parsed_candidate = ai_agent.parse_resume(test_resume)

print("\n📊 Результат парсинга:")
print(json.dumps(parsed_candidate, ensure_ascii=False, indent=2))

print("\n" + "=" * 70)
print("ТЕСТ 2️⃣ : ОТПРАВКА TELEGRAM СООБЩЕНИЯ")
print("=" * 70)

YOUR_TELEGRAM_ID = "873023928"

test_message = """
👋 Привет, Максим!

Видел твой опыт с Go - впечатляет! 🚀

В Lamoda ищем Senior Backend Developer:
💰 120k рублей
🛠️ Go, Python, Kubernetes
📊 Масштабируемые системы

Интересует? Давай обсудим!

https://calendly.com/syromiatski/backend

Максим
"""

print(f"\n💬 Отправляю сообщение...")
print(f"Сообщение:\n{test_message}")

telegram_result = ai_agent.send_telegram(YOUR_TELEGRAM_ID, test_message)

print(f"\n📤 Результат отправки:")
print(json.dumps(telegram_result, ensure_ascii=False, indent=2))

if telegram_result.get('status') == 'SENT':
    print("✅ Сообщение успешно отправлено в Telegram!")
else:
    print("❌ Ошибка при отправке сообщения")

print("\n" + "=" * 70)
print("✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!")
print("=" * 70)
