import telebot
import random

token = ""
bot = telebot.TeleBot(token)
users = {}

QUESTIONS = {
    'Какой мусс в исфахане?': ['малиновый', 'малина', 'с малиной', 'из малины'],
    'Какого цвета фисташковый трюфель?': ['зеленый'],
    'Сколько сырников в порции?': ['три', '3']
}


@bot.message_handler(commands=['start'])
def add_user(message):
    if "{0}".format(message.chat.id) not in users.keys():
        users["{0}".format(message.chat.id)] = Test(message.chat.username)
        print(users)  # вывод на консоль для проверки
    users["{0}".format(message.chat.id)].start_attestation(message)


class Test:
    def __init__(self, message):
        self.i = 0
        self.count = 0
        self.random_questions = list(QUESTIONS.keys())

    def randomizer(self):
        random.shuffle(self.random_questions)

    @bot.message_handler(content_types='text')
    def start_attestation(self, message):
        bot.send_message(message.chat.id, 'Начнём тест')
        self.randomizer()
        self.test(message)

    def test(self, message):
        bot.send_message(message.chat.id, self.random_questions[self.i])
        print(self.i)
        bot.register_next_step_handler(message, self.chek)

    def chek(self, message):
        if message.text.lower() in QUESTIONS[self.random_questions[self.i]]:
            bot.send_message(message.chat.id, 'Правильно')
        else:
            bot.send_message(message.chat.id, 'Неправильно')
        self.i += 1

        if self.i == 3:
            bot.send_message(message.chat.id, 'Тест окончен')
            self.i = 0
        else:
            self.test(message)


bot.polling(none_stop=True, interval=0)
