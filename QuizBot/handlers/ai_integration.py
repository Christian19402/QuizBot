import requests
import json
from config.config import DEEPSEEK_API_KEY

def generate_question(bot, message):
    try:
        topic = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else "general"
        url = "https://api.deepseek.com/v1/generate"  # Verifica la URL correcta
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": f"Genera una pregunta sobre {topic}",
            "max_tokens": 50,
            "temperature": 0.7
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        generated_text = response.json().get("choices", [{}])[0].get("text", "").strip()
        if generated_text:
            bot.send_message(message.chat.id, generated_text)
        else:
            bot.send_message(message.chat.id, "No se pudo generar una pregunta.")
    except requests.exceptions.RequestException as e:
        bot.send_message(message.chat.id, f"Error al generar pregunta: {e}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error inesperado: {e}")