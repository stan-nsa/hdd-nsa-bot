from aiogram import Bot, Dispatcher, executor, types
from emoji import emojize #Overview of all emoji: https://carpedm20.github.io/emoji/

import nhl
import db


#-- Чтение конфига --
import json
with open('config.json') as f:
    config = json.load(f)
#----


bot = Bot(token=config['API_TOKEN'])
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\n"
                        "Я NHL-бот канала \"Хоккей для друзей\"!\n\n"
                        "Я могу показывать:\n"
                        "/results - результаты сегодняшних матчей\n"
                        "/today - расписание матчей на сегодня\n"
                        "/yesterday - Расписание матчей на вчера\n"
                        "/tomorrow - Расписание матчей на завтра", parse_mode="HTML")


@dp.message_handler(commands=['gameday'])
async def send_schedule_gameday(message: types.Message):
    await message.answer(f"#GameDay - {emojize(':calendar:')} <b>Расписание матчей:</b>\n{nhl.get_schedule_today()}", parse_mode="HTML")


@dp.message_handler(commands=['schedule'])
async def send_schedule_team(message: types.Message):
    await message.reply("Расписание матчей <team>:\n. . .\n. . .\n. . .\n. . .\n. . .\n")


@dp.message_handler(commands=['today'])
async def send_schedule_today(message: types.Message):
    await message.reply(f"{emojize(':calendar:')} <b>Расписание матчей:</b>\n{nhl.get_schedule_today()}", parse_mode="HTML")


@dp.message_handler(commands=['tomorrow'])
async def send_schedule_today(message: types.Message):
    await message.reply(f"{emojize(':calendar:')} <b>Расписание матчей:</b>\n{nhl.get_schedule_tomorrow()}", parse_mode="HTML")


@dp.message_handler(commands=['yesterday'])
async def send_schedule_today(message: types.Message):
    await message.reply(f"{emojize(':calendar:')} <b>Расписание матчей:</b>\n{nhl.get_schedule_yesterday()}", parse_mode="HTML")


@dp.message_handler(commands=['results'])
async def send_results_today(message: types.Message):
    await message.reply(f"{emojize(':goal_net::ice_hockey:')} <b>Результаты матчей:</b>\n{nhl.get_results_today()}", parse_mode="HTML")


@dp.message_handler(commands=['test'])
async def send_schedule_team(message: types.Message):
    db.insert_user(message.from_user)
    await message.reply('<tg-spoiler><a href="https://ya.ru">CAR🏒PIT</a></tg-spoiler>', parse_mode="HTML")


"""
@dp.message_handler()
async def echo(message: types.Message):
    #print(message.text)
    #await message.answer(message.text)
    #await message.answer(message.text, parse_mode='HTML')
    #await message.answer(message.text, parse_mode='MarkdownV2')
    await message.answer(message.text)
    await message.answer(message.md_text)
    await message.answer(message.html_text)
    # Дополняем исходный текст:
    await message.answer(f'<u>Ваш текст</u>:\n\n{message.html_text}', parse_mode='HTML')
"""

if __name__ == '__main__':
    #db.db_connect()
    executor.start_polling(dp, skip_updates=True)
    #db.db_close()

