# llm_client.py
import os
import json
from typing import Dict, Any
import requests


class LLMClient:
    """Клиент для анализа резюме через ProxyAPI с поддержкой OpenAI API."""
    
    def __init__(self) -> None:
        self.base_url = os.getenv("PROXY_API_BASE_URL", "https://api.proxyapi.ru/openai/v1")
        self.api_key = os.getenv("PROXY_API_KEY")
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        
        if not self.api_key:
            raise RuntimeError("PROXY_API_KEY is not set in environment variables")

    def analyze_resume(self, raw_text: str) -> Dict[str, Any]:
        """
        Анализирует резюме через ProxyAPI и возвращает структурированные данные.
        
        Args:
            raw_text: Текст резюме
            
        Returns:
            Dict с полями: name, email, phone, skills, experience_years, 
                          education_level, languages, score, summary
        """
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        prompt = self._build_prompt(raw_text)
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Ты опытный HR-аналитик. Проанализируй резюме и верни ТОЛЬКО валидный JSON "
                        "по указанной схеме, без какого-либо текста вокруг."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            return json.loads(content)
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"ProxyAPI request failed: {e}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"LLM returned invalid JSON: {e}")

    def _build_prompt(self, raw_text: str) -> str:
        """Построить промпт для анализа резюме."""
        return (
            "Вот текст резюме кандидата:\n\n"
            f"{raw_text}\n\n"
            "Проанализируй резюме и верни JSON строго по этой схеме (без отклонений):\n"
            "{\n"
            '  "name": "string (ФИ или имя кандидата)",\n'
            '  "email": "string или null",\n'
            '  "phone": "string или null",\n'
            '  "skills": ["список технологий/навыков"],\n'
            '  "experience_years": число,\n'
            '  "education_level": "string (Bachelor, Master, etc)",\n'
            '  "languages": ["список языков"],\n'
            '  "score": число от 0 до 100,\n'
            '  "summary": "краткое резюме кандидата (2-3 строки)"\n'
            "}\n\n"
            "ВАЖНО: Верни ТОЛЬКО JSON без комментариев, без markdown, без текста снаружи."
        )
