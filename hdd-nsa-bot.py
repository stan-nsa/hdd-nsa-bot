from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from emoji import emojize #Overview of all emoji: https://carpedm20.github.io/emoji/

import nhl
import db
import keyboards


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
                        "Я NHL-бот!\n\n"
                        "Напиши мне по ссылке: @HDD_nsa_bot и запусти меня!\n"
                        "Я могу показывать:\n"
                        "/results - результаты сегодняшних матчей\n"
                        "/today - расписание матчей на сегодня\n"
                        "/yesterday - Расписание матчей на вчера\n"
                        "/tomorrow - Расписание матчей на завтра\n"
                        "\n"
                        "Сделай индивидуальные настройки:\n"
                        "/set\n"
                        "И тогда Я смогу показывать:\n"
                        "/schedule - Расписание матчей твоих любимых команд\n", \
                        parse_mode="HTML")


@dp.message_handler(commands=['gameday'])
async def send_schedule_gameday(message: types.Message):
    await message.answer(f"#GameDay - {emojize(':calendar:')} <b>Расписание матчей:</b>\n{nhl.get_schedule_today()}", parse_mode="HTML")


@dp.message_handler(commands=['schedule'])
async def send_schedule_team(message: types.Message):
    await message.reply(f"{emojize(':calendar:')} <b>Расписание матчей любимых команд:</b>\n{nhl.get_schedule_user_teams(message.from_user)}", parse_mode="HTML")


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


@dp.message_handler(commands=['set'])
async def user_settings(message: types.Message):
    db.insert_user(message.from_user)
    await message.reply(f"Привет, {message.from_user['first_name']}!\nЗа какую команду ты болеешь?", parse_mode="HTML", reply_markup=keyboards.init_kb_user_settings())


@dp.message_handler(commands=['favorites'])
async def user_settings(message: types.Message):
    await message.answer("Выбери команду, за которую болеешь:", reply_markup=keyboards.init_kb_user_favorites_teams(message.from_user))


@dp.message_handler(commands=['followed'])
async def user_settings(message: types.Message):
    await message.reply(f"Выбери команды, за которыми будешь следить:", reply_markup=keyboards.init_kb_followed_teams(message.from_user))


@dp.callback_query_handler(Text(startswith='favorites_'))
async def favorites(callback : types.CallbackQuery):
    team = callback.data.split('_')[1]
    user = callback.from_user
    db.insert_favorites(user, team)
    await callback.answer(f"Команда '{team.split(':')[1]}' добавлена в ваш список Избранное!", show_alert=True)


@dp.callback_query_handler(Text(startswith='followed_'))
async def followed(callback : types.CallbackQuery):
    team = callback.data.split('_')[1]
    user = callback.from_user
    db.insert_favorites(user, team, 'followed')
    await callback.answer(f"Команда '{team.split(':')[1]}' добавлена в ваш список Слежения!", show_alert=True)


@dp.message_handler(commands=['test'])
async def send_test(message: types.Message):
    await message.reply('<tg-spoiler><a href="https://ya.ru">CAR🏒PIT</a></tg-spoiler>', parse_mode="HTML")
    await bot.send_message(message.from_user.id, 'test')
    await message.delete()


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
    executor.start_polling(dp, skip_updates=True)

