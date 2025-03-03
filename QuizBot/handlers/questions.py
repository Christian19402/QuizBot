from telebot import types
from database import Database
from core.models.progress import Progress

def handle_topic_selection(bot, call):
    try:
        topic_info = call.data.split("_")
        topic_number = topic_info[1]
        subject = topic_info[2]
        db = Database()
        questions = db.get_questions_by_topic(subject, f"Tema {topic_number}")
        if questions:
            first_question = questions[0]
            markup = types.InlineKeyboardMarkup()
            for option in first_question[4].split(","):
                markup.add(types.InlineKeyboardButton(text=option, callback_data=f"respuesta_{topic_number}_{subject}_{option}"))
            if first_question[7]:  # Si hay una URL de imagen
                bot.send_photo(call.message.chat.id, first_question[7], caption=first_question[3], reply_markup=markup)
            else:
                bot.send_message(call.message.chat.id, first_question[3], reply_markup=markup)
        else:
            bot.send_message(call.message.chat.id, f"No se encontraron preguntas válidas para {subject}, Tema {topic_number}.")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Error al cargar preguntas: {e}")

def handle_answer_selection(bot, call):
    try:
        answer_info = call.data.split("_")
        topic_number = answer_info[1]
        subject = answer_info[2]
        selected_answer = answer_info[3]
        db = Database()
        questions = db.get_questions_by_topic(subject, f"Tema {topic_number}")
        if questions:
            current_question = questions[0]
            correct_answer = current_question[5]
            explanation = current_question[6]
            user_id = call.from_user.id
            progress = Progress(user_id=user_id, subject_id=int(subject), topic=f"Tema {topic_number}",
                                correct_answers=1 if selected_answer == correct_answer else 0, total_questions=1)
            db.update_progress(progress)
            if selected_answer == correct_answer:
                bot.send_message(call.message.chat.id, "¡Correcto!")
            else:
                bot.send_message(call.message.chat.id, f"Incorrecto. La respuesta correcta es: {correct_answer}. {explanation}")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Error al procesar respuesta: {e}")