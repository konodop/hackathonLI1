# import telebot
import asyncio
import json

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

data = json.load(open("data.json", "r"))

token = "7852103064:AAHSVFQeOZFxj1wsVDodSfj1QBRAMHw_0oE"
bot = Bot(token=token)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Бот для хакатона от Ли1")
    await message.answer("""Введите логин и пароль\nПо типу '{login} {password}'""")


@dp.message()
async def start(message: types.Message):
    info = json.loads(message.model_dump_json())
    print(info)

    if info["text"]:
        tg_id = info["from_user"]["username"]
        if tg_id not in data:
            sp = info["text"].split()
            if len(sp) != 2:
                await message.answer("""Неверный формат ввода""")
                await message.answer("""Введите логин и пароль\nПо типу '{login} {password}'""")
            else:
                login, password = sp
                url = f"http://127.0.0.1:8080/api/student/sign-up"
                res = requests.post(
                    url, json={"login": login, "password": password}
                )
                print(res)
    else:
        await message.answer("""Я не могу вас понять\nЯ пока умею работать только с текстом""")


async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot)


asyncio.run(main())
