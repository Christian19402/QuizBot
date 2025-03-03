import unittest
from handlers.commands import start_menu

class TestHandlers(unittest.TestCase):
    def setUp(self):
        self.bot = MockBot()
        self.message = MockMessage(12345)

    def test_start_menu(self):
        start_menu(self.bot, self.message)
        self.assertTrue(self.bot.sent_message)
        self.assertIn("Hola!", self.bot.last_message)

class MockBot:
    def __init__(self):
        self.sent_message = False
        self.last_message = ""

    def send_message(self, chat_id, text, reply_markup=None):
        self.sent_message = True
        self.last_message = text

class MockMessage:
    def __init__(self, chat_id):
        self.chat = MockChat(chat_id)

class MockChat:
    def __init__(self, id):
        self.id = id

if __name__ == "__main__":
    unittest.main()