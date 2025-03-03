from Bot.QuizBot.handlers import questions


class Question:
    def __init__(self, subject_id, topic, question, options, correct_answer, explanation):
        self.subject_id = subject_id
        self.topic = topic
        self.question = question
        self.options = options
        self.correct_answer = correct_answer
        self.explanation = explanation
        self.image_url = image_url

    def handle_topic_selection(bot, call):
        topic_info = call.data.split("_")
        topic_number = topic_info[1]
        subject = topic_info[2]    

        db = Database() # type: ignore
        questions = db.get_questions_by_topic(subject, f"Tema {topic_number}")
if questions:
        first_question = questions[0]
        markup = types.InlineKeyboardMarkup() # type: ignore
        for option in first_question[4].split(","):
            markup.add(types.InlineKeyboardButton(text=option, callback_data=f"respuesta_{topic_number}_{subject}_{option}")) # type: ignore
    
if first_question[7]:  # Si hay una URL de imagen
    bot.send_photo(call.message.chat.id, first_question[7], caption=first_question[3], reply_markup=markup) # type: ignore
else:
    bot.send_message(call.message.chat.id, first_question[3], reply_markup=markup) # type: ignore

else: bot.send_message(call.message.chat.id, f"No se encontró preguntas válidas para {subject}, Tema {topic_number}.") # type: ignore