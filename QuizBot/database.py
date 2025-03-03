import sqlite3
from core.models.user import User
from core.models.subject import Subject
from core.models.question import Question
from core.models.progress import Progress

class Database:
    def __init__(self, db_name="quizbot.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                chat_id INTEGER UNIQUE
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                subject_id INTEGER,
                topic TEXT,
                question TEXT,
                options TEXT,
                correct_answer TEXT,
                explanation TEXT,
                image_url TEXT,
                FOREIGN KEY (subject_id) REFERENCES subjects (id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                subject_id INTEGER,
                topic TEXT,
                correct_answers INTEGER,
                total_questions INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (subject_id) REFERENCES subjects (id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS group_questions (
                id INTEGER PRIMARY KEY,
                chat_id INTEGER,
                user_id INTEGER,
                subject_id INTEGER,
                topic TEXT,
                question TEXT,
                options TEXT,
                correct_answer TEXT,
                explanation TEXT,
                FOREIGN KEY (subject_id) REFERENCES subjects (id)
            )
        """)
        self.conn.commit()

    def add_user(self, user: User):
        try:
            self.cursor.execute("INSERT OR IGNORE INTO users (chat_id) VALUES (?)", (user.chat_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Error al añadir usuario: {e}")

    def add_subject(self, subject: Subject):
        try:
            self.cursor.execute("INSERT OR IGNORE INTO subjects (name) VALUES (?)", (subject.name,))
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Error al añadir asignatura: {e}")

    def add_question(self, question: Question):
        try:
            self.cursor.execute("""
                INSERT INTO questions (subject_id, topic, question, options, correct_answer, explanation, image_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (question.subject_id, question.topic, question.question, ",".join(question.options),
                  question.correct_answer, question.explanation, question.image_url))
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Error al añadir pregunta: {e}")

    def get_questions_by_topic(self, subject_id, topic):
        try:
            self.cursor.execute("SELECT * FROM questions WHERE subject_id = ? AND topic = ?", (subject_id, topic))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Error al obtener preguntas: {e}")

    def update_progress(self, progress: Progress):
        try:
            self.cursor.execute("""
                INSERT OR REPLACE INTO progress (user_id, subject_id, topic, correct_answers, total_questions)
                VALUES (?, ?, ?, ?, ?)
            """, (progress.user_id, progress.subject_id, progress.topic, progress.correct_answers, progress.total_questions))
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Error al actualizar progreso: {e}")

    def add_group_question(self, question: Question, chat_id: int, user_id: int):
        try:
            self.cursor.execute("""
                INSERT INTO group_questions (chat_id, user_id, subject_id, topic, question, options, correct_answer, explanation)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (chat_id, user_id, question.subject_id, question.topic, question.question, ",".join(question.options),
                  question.correct_answer, question.explanation))
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Error al añadir pregunta de grupo: {e}")