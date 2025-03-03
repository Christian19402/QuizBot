from telebot import types
from database import Database

def start_menu(bot, message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton("Asignaturas"))
        markup.add(types.KeyboardButton("Preguntas"))
        markup.add(types.KeyboardButton("Ver progreso"))
        bot.send_message(message.chat.id, "Hola! 😊, para usar el bot observa las opciones del menú", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al mostrar menú: {e}")

def show_asignaturas(bot, message):
    try:
        db = Database()
        subjects = db.cursor.execute("SELECT id, name FROM subjects").fetchall()
        if subjects:
            markup = types.InlineKeyboardMarkup()
            for subject in subjects:
                markup.add(types.InlineKeyboardButton(text=subject[1], callback_data=f"tema_{subject[0]}_{subject[1]}"))
            bot.send_message(message.chat.id, 'Selecciona una asignatura:', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "No hay asignaturas disponibles.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al mostrar asignaturas: {e}")

def show_preguntas(bot, message):
    try:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="Añadir pregunta", callback_data="añadir_pregunta"))
        bot.send_message(message.chat.id, 'Selecciona una opción:', reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al mostrar opciones de preguntas: {e}")

def show_progress(bot, message):
    try:
        db = Database()
        user_id = message.from_user.id
        progress = db.cursor.execute("""
            SELECT subject_id, topic, correct_answers, total_questions
            FROM progress WHERE user_id = ?
        """, (user_id,)).fetchall()
        if progress:
            progress_text = "\n".join([f"Tema {p[1]} ({p[0]}): {p[2]}/{p[3]}" for p in progress])
            bot.send_message(message.chat.id, f"Tu progreso:\n{progress_text}")
        else:
            bot.send_message(message.chat.id, "No tienes progreso registrado.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error al mostrar progreso: {e}")