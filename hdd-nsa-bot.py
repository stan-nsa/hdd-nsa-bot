from aiogram import Bot, Dispatcher, executor, types

#-- Чтение конфига --
import json
with open('config.json') as f:
    config = json.load(f)
#----

bot = Bot(token=config['API_TOKEN'])
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ Эхо-бот!\nОтправь мне любое сообщение, а я тебе обязательно отвечу!")

@dp.message_handler(commands=['schedule'])
async def send_schedule_team(message: types.Message):
    await message.reply("Расписание матчей <team>:\n. . .\n. . .\n. . .\n. . .\n. . .\n")

@dp.message_handler(commands=['today'])
async def send_schedule_today(message: types.Message):
    from datetime import date
    await message.reply("Расписание матчей на сегодня - "+date.today().strftime("%d %B %Y")+":\n. . .\n. . .\n. . .\n. . .\n. . .\n")

@dp.message_handler(commands=['results'])
async def send_results_today(message: types.Message):
    from datetime import date
    await message.reply("Результаты матчей на сегодня - "+date.today().strftime("%d %B %Y")+":\n. . .\n. . .\n. . .\n. . .\n. . .\n")

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

