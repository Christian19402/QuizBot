import telebot
from config.config import TOKEN
from handlers.commands import start_menu, show_asignaturas, show_preguntas, show_progress
from handlers.questions import handle_topic_selection, handle_answer_selection
from handlers.groups import handle_group_question, import_questions, share_questions
from handlers.exams import start_exam, handle_exam_subject
from handlers.ai_integration import generate_question
from database import Database
from core.models.user import User

# Inicialización del bot
bot = telebot.TeleBot(TOKEN)

# Inicialización de la base de datos
db = Database()

# Manejadores de comandos
@bot.message_handler(commands=['start'])
def start(message):
    try:
        user = User(chat_id=message.chat.id)
        db.add_user(user)
        start_menu(bot, message)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al iniciar: {e}")

@bot.message_handler(func=lambda message: message.text == 'Asignaturas')
def asignaturas(message):
    try:
        show_asignaturas(bot, message)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al mostrar asignaturas: {e}")

@bot.message_handler(func=lambda message: message.text == 'Preguntas')
def preguntas(message):
    try:
        show_preguntas(bot, message)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al mostrar preguntas: {e}")

# Manejadores de preguntas y respuestas
@bot.callback_query_handler(func=lambda call: call.data.startswith("tema_"))
def tema_selection(call):
    handle_topic_selection(bot, call)

@bot.callback_query_handler(func=lambda call: call.data.startswith("respuesta_"))
def answer_selection(call):
    handle_answer_selection(bot, call)

# Manejador para preguntas creadas en grupos
@bot.message_handler(func=lambda message: message.chat.type in ["group", "supergroup"])
def group_message_handler(message):
    handle_group_question(bot, message)

# Manejador para importar preguntas desde grupos
@bot.message_handler(commands=['import_questions'])
def import_questions_handler(message):
    try:
        import_questions(bot, message)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al importar preguntas: {e}")

# Manejador de preguntas compartidas
@bot.message_handler(commands=['share_questions'])
def share_questions_handler(message):
    try:
        share_questions(bot, message)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al compartir preguntas: {e}")

# Manejador de exámenes
@bot.message_handler(commands=['exam'])
def exam_handler(message):
    try:
        start_exam(bot, message)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al iniciar examen: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith("exam_subject_"))
def exam_subject_selection(call):
    handle_exam_subject(bot, call)

# Manejador del progreso del estudiante
@bot.message_handler(func=lambda message: message.text == 'Ver progreso')
def progress_handler(message):
    try:
        show_progress(bot, message)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al mostrar progreso: {e}")

# Manejador de generación de preguntas con IA
@bot.message_handler(commands=['generate_question'])
def generate_question_handler(message):
    try:
        generate_question(bot, message)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al generar pregunta: {e}")

# Iniciar el bot
if __name__ == "__main__":
    bot.polling()