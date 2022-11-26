from aiogram import Bot, Dispatcher, executor, types
import nhl
from emoji import emojize #Overview of all emoji: https://carpedm20.github.io/emoji/

#-- Чтение конфига --
import json
with open('config.json') as f:
    config = json.load(f)
#----

bot = Bot(token=config['API_TOKEN'])
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ NHL-бот канала \"Хоккей для друзей\"!\n\nЯ могу показывать:\n/today - Расписание матчей на сегодня\n/results - результаты сегодняшних матчей")

@dp.message_handler(commands=['schedule'])
async def send_schedule_team(message: types.Message):
    await message.reply("Расписание матчей <team>:\n. . .\n. . .\n. . .\n. . .\n. . .\n")

@dp.message_handler(commands=['today'])
async def send_schedule_today(message: types.Message):
    from datetime import date
    #await message.reply("Расписание матчей на сегодня - "+date.today().strftime("%d %B %Y")+":"+nhl.get_schedule_today())
    await message.reply("Расписание матчей:" + nhl.get_schedule_today(), parse_mode="HTML")

@dp.message_handler(commands=['results'])
async def send_results_today(message: types.Message):
    from datetime import date
    #await message.reply("Результаты матчей на сегодня - "+date.today().strftime("%d %B %Y")+":"+nhl.get_schedule_today())
    await message.reply("Результаты матчей: " + emojize(':goal_net::ice_hockey:') + nhl.get_schedule_today(), parse_mode="HTML")

@dp.message_handler(commands=['test'])
async def send_schedule_team(message: types.Message):
    await message.reply('<a href="https://ya.ru">Текст</a>\n<a href="/start">Старт</a>', parse_mode="HTML")

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text, parse_mode="HTML")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

