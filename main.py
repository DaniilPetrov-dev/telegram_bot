import telebot
import random
import nltk

token = "5049484687:AAGPG0cU2SltEi_UvfEEQORDnsAp7QmeNyA"
bot = telebot.TeleBot(token)
users = {}

QUESTIONS = {
    'Какое сабле в пекане?': ['миндальное', 'миндаль', 'с миндалём', 'из миндаля'],
    'Какой (или какие) крем в ванильном флане?': ['заварной' 'заварной крем'],
    'С чем ганаш, который идет в большиство круассанов и макарунов?': ['белый шоколад', 'с белым шоколадом'],
    'Какой (или какие) крем в красном бархате?': ['крем-чиз', 'сырный', 'маскарпоне', 'из сыра', 'кремчиз и маскарпоне', 'кремчиз'],
    'Какой соус в кишах?': ['сливочно-сырный', 'сливочный с сыром'],
    'Какое пюре в фрамбуа?': ['малиновое', 'с малиной', 'из малины', 'малина'],
    'Из чего сделаны крышки макоронов?': ['меренга', 'из меренги', 'итальянская меренга', 'из итальянской меренги'],
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
        print(self.i)  # вывод на консоль для проверки
        bot.register_next_step_handler(message, self.chek)

    def chek(self, message):
        answer = message.text.lower()
        r = 0
        for right_answer in QUESTIONS[self.random_questions[self.i]]:
            if nltk.edit_distance(answer, right_answer) / max(len(answer), len(right_answer)) < 0.4:
                bot.send_message(message.chat.id, 'Правильно')
                self.count += 1
                break
            else:
                r += 1
            if r == len(QUESTIONS[self.random_questions[self.i]]):
                bot.send_message(message.chat.id, 'Неправильно')

        self.i += 1

        if self.i == len(self.random_questions):
            bot.send_message(message.chat.id, 'Тест окончен')
            bot.send_message(
                message.chat.id, f'Правильных ответов: {self.count} из 7')
            self.i = 0
            self.count = 0
        else:
            self.test(message)


bot.polling(none_stop=True, interval=0)
