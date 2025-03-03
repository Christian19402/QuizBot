from telebot import types
from database import Database
import random

def start_exam(bot, message):
    try:
        db = Database()
        subjects = db.cursor.execute("SELECT id, name FROM subjects").fetchall()
        if subjects:
            markup = types.InlineKeyboardMarkup()
            for subject in subjects:
                markup.add(types.InlineKeyboardButton(text=subject[1], callback_data=f"exam_subject_{subject[0]}"))
            bot.send_message(message.chat.id, "Selecciona una asignatura para el examen:", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "No hay asignaturas disponibles.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al iniciar examen: {e}")

def handle_exam_subject(bot, call):
    try:
        subject_id = int(call.data.split("_")[2])
        db = Database()
        questions = db.cursor.execute("SELECT * FROM questions WHERE subject_id = ?", (subject_id,)).fetchall()
        if questions:
            exam_questions = random.sample(questions, min(10, len(questions)))
            for i, question in enumerate(exam_questions):
                markup = types.InlineKeyboardMarkup()
                for option in question[4].split(","):
                    markup.add(types.InlineKeyboardButton(text=option, callback_data=f"exam_answer_{question[0]}_{option}"))
                bot.send_message(call.message.chat.id, f"Pregunta {i + 1}: {question[3]}", reply_markup=markup)
        else:
            bot.send_message(call.message.chat.id, "No hay preguntas disponibles para esta asignatura.")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Error al cargar examen: {e}")