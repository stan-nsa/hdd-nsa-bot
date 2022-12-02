from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

button_favorites = KeyboardButton('/favorites')
button_followed = KeyboardButton('/followed')

kb_user = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_user.row(button_favorites, button_followed)
