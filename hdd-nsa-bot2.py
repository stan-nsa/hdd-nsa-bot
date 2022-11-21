import telebot
import random
from telebot import types

# Создаем бота
bot = telebot.TeleBot('5661825852:AAFU7t-PSe5smkgDKnSYORKewHfMUoD6bL8')

# Команда start
@bot.message_handler(commands=["start"])
def start(m, res=False):
        # Добавляем две кнопки
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Факт")
        item2=types.KeyboardButton("Поговорка")
        markup.add(item1)
        markup.add(item2)
        bot.send_message(m.chat.id, 'Нажми: \nФакт для получения интересного факта\nПоговорка — для получения мудрой цитаты ',  reply_markup=markup)

# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    # Если юзер прислал 1, выдаем ему случайный факт
    if message.text.strip() == 'Факт' :
            answer = 'Fuckt'
    # Если юзер прислал 2, выдаем умную мысль
    elif message.text.strip() == 'Поговорка':
            answer = 'Pogovorka'
    # Отсылаем юзеру сообщение в его чат
    bot.send_message(message.chat.id, answer)

# Запускаем бота
bot.polling(none_stop=True, interval=1)
