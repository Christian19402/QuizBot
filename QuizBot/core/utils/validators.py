def validate_question_input(question, options, correct_answer, explanation):
    if not question or not options or not correct_answer or not explanation:
        raise ValueError("Todos los campos son obligatorios.")
    if correct_answer not in options:
        raise ValueError("La respuesta correcta debe estar entre las opciones.")