from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import nhl


kb_user = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_favorites = KeyboardButton('/favorites')
button_followed = KeyboardButton('/followed')
kb_user.row(button_favorites, button_followed)


teams = nhl.get_teams()
kb_favorites_teams = InlineKeyboardMarkup()
kb_followed_teams = InlineKeyboardMarkup()
for team in teams:
    kb_favorites_teams.add(InlineKeyboardButton(text=team['name'], callback_data=f"favorites_{team['id']}:{team['name']}"))
    kb_followed_teams.add(InlineKeyboardButton(text=team['name'], callback_data=f"followed_{team['id']}:{team['name']}"))
