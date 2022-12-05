from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize #Overview of all emoji: https://carpedm20.github.io/emoji/
import nhl
import db

kb_user_settings = None
kb_favorites_teams = None
kb_followed_teams = None

def init_kb_user_settings():
    global kb_user_settings

    kb_user_settings = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb_user_settings.row(KeyboardButton('/favorites'), \
                         KeyboardButton('/followed'))

    return kb_user_settings


def init_kb_user_favorites_teams(user=None):
    global kb_favorites_teams

    teams = nhl.get_teams()
    user_teams = db.get_user_favorites_teams(user)

    kb_favorites_teams = InlineKeyboardMarkup()
    for team in teams:
        kb_favorites_teams.add(InlineKeyboardButton(text=team['name'] + (emojize(':red_heart:') if (team['id'],) in user_teams else ''), \
                                                    callback_data=f"favorites_{team['id']}:{team['name']}"))

    return kb_favorites_teams

def init_kb_followed_teams(user=None):
    global kb_followed_teams

    teams = nhl.get_teams()
    user_teams = db.get_user_favorites_teams(user, 'followed')

    kb_followed_teams = InlineKeyboardMarkup()
    for team in teams:
        kb_followed_teams.add(
            InlineKeyboardButton(text=team['name'] + (emojize(':eye:') if (team['id'],) in user_teams else ''), \
                                 callback_data=f"followed_{team['id']}:{team['name']}"))

    return kb_followed_teams


