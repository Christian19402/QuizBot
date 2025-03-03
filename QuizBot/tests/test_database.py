import unittest
from database import Database
from core.models.user import User

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database("test_quizbot.db")

    def test_add_user(self):
        user = User(chat_id=12345)
        self.db.add_user(user)
        result = self.db.cursor.execute("SELECT chat_id FROM users WHERE chat_id = ?", (12345,)).fetchone()
        self.assertEqual(result[0], 12345)

    def tearDown(self):
        self.db.conn.close()

if __name__ == "__main__":
    unittest.main()