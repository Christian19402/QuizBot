from telebot import types
from database import Database
from core.models.question import Question

def handle_group_question(bot, message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        if message.text.startswith("/add_question"):
            details = message.text.split("\n")
            if len(details) < 6:
                bot.reply_to(message, "Formato incorrecto. Usa /add_question seguido de los detalles.")
                return
            db = Database()
            question = Question(subject_id=1, topic="Tema Importado", question=details[1].strip(),
                                options=details[2].strip().split(","), correct_answer=details[3].strip(),
                                explanation=details[4].strip())
            db.add_group_question(question, chat_id, user_id)
            bot.reply_to(message, "Pregunta añadida al grupo. Usa /import_questions para importarla.")
    except Exception as e:
        bot.reply_to(message, f"Error al añadir pregunta: {e}")

def import_questions(bot, message):
    try:
        user_id = message.from_user.id
        db = Database()
        group_questions = db.cursor.execute("""
            SELECT subject_id, topic, question, options, correct_answer, explanation
            FROM group_questions WHERE user_id = ?
        """, (user_id,)).fetchall()
        if group_questions:
            for q in group_questions:
                question = Question(subject_id=q[0], topic=q[1], question=q[2], options=q[3].split(","),
                                    correct_answer=q[4], explanation=q[5])
                db.add_question(question)
            bot.send_message(message.chat.id, "Preguntas importadas exitosamente.")
        else:
            bot.send_message(message.chat.id, "No hay preguntas para importar.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al importar preguntas: {e}")

def share_questions(bot, message):
    try:
        db = Database()
        user_id = message.from_user.id
        markup = types.InlineKeyboardMarkup()
        subjects = db.cursor.execute("SELECT id, name FROM subjects").fetchall()
        for subject in subjects:
            markup.add(types.InlineKeyboardButton(text=subject[1], callback_data=f"share_subject_{subject[0]}"))
        bot.send_message(message.chat.id, "Selecciona una asignatura para compartir:", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al compartir preguntas: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith("share_subject_"))
def handle_share_subject(bot, call):
    try:
        subject_id = int(call.data.split("_")[2])
        db = Database()
        questions = db.get_questions_by_topic(subject_id, "Tema Importado")
        if questions:
            shared_questions = "\n\n".join([f"Pregunta: {q[3]}\nOpciones: {q[4]}\nRespuesta correcta: {q[5]}" for q in questions])
            bot.send_message(call.message.chat.id, f"Preguntas compartidas:\n{shared_questions}")
        else:
            bot.send_message(call.message.chat.id, "No hay preguntas para compartir.")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Error al compartir preguntas: {e}")