# QuizBot

## Descripción
QuizBot es un bot de Telegram para ayudar a estudiantes con preguntas y respuestas interactivas.

## Instalación
1. Clona el repositorio: `git clone https://github.com/tu-usuario/QuizBot.git`
2. Instala dependencias: `pip install -r requirements.txt`
3. Crea un archivo `.env` con `TELEGRAM_TOKEN` y `DEEPSEEK_API_KEY`.
4. Ejecuta el bot: `python main.py`

## Dependencias
- pyTelegramBotAPI
- requests
- python-dotenv

## Uso
- `/start`: Inicia el bot.
- `/exam`: Realiza un examen.
- `/generate_question <tema>`: Genera una pregunta con IA.

## Contribución
1. Haz un fork del repositorio.
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`.
3. Envía un pull request.