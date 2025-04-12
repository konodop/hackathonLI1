import json
import logging
import os

import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


# Состояния FSM
class ReadStates(StatesGroup):
    waiting_for_image = State()

def get_user_info(tg_id, info=None):
    get_info = False
    url = f"http://127.0.0.1:8080/api/profile"
    res = requests.post(url, json={"tg_id": tg_id})
    if get_info:
        if info:
            print(info)
        print(tg_id)
        print(res.status_code)
        print(res.json())
    return res.status_code, res.json()["message"]


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен вашего бота
TOKEN = "8139226754:AAHXJZwwS82ijvHcI615UicFxfeisqB_LPY"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()


# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    info = json.loads(message.model_dump_json())
    tg_id = "@" + info["from_user"]["username"]
    status, post = get_user_info(tg_id, info)
    if status != 200:
        await message.answer(
            "Не хватает прав на использование бота\n"
            "Чтобы решить эту проблему обратитесь к администратору"
        )
    # Создаем клавиатуру с кнопками
    kb = [
        [types.KeyboardButton(text="Помощь")],
        [types.KeyboardButton(text="Информация")],
        [types.KeyboardButton(text="Кнопки")],
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )

    await message.answer(
        f"Привет, {post}! Я бот от команды Ли1.\n"
        "Используй кнопки ниже или команды:\n"
        "/start - начать сначала\n"
        "/help - помощь\n"
        "/info - информация\n",
        reply_markup=keyboard
    )


# Обработчик команды /help
@dp.message(Command("help"))
@dp.message(F.text.lower() == "помощь")
async def cmd_help(message: types.Message):
    info = json.loads(message.model_dump_json())
    tg_id = "@" + info["from_user"]["username"]
    status, post = get_user_info(tg_id, info)
    if status != 200:
        await message.answer(
            "Не хватает прав на использование бота\n"
            "Чтобы решить эту проблему обратитесь к администратору"
        )

    if post == "ученик":
        await message.answer(
            "Это справочная информация:\n"
            "/start - начать сначала\n"
            "/help - помощь\n"
            "/info - информация\n"
            "/Create_qr_code - создать qr-code",
        )
    if post == "учитель":
        await message.answer(
            "Это справочная информация:\n"
            "/start - начать сначала\n"
            "/help - помощь\n"
            "/info - информация\n"
            "/read_qr_code - считать qr-code",
        )
    if post == "родитель":
        await message.answer(
            "Это справочная информация:\n"
            "/start - начать сначала\n"
            "/help - помощь\n"
            "/info - информация\n"
            "/about_child - о ребенке",
        )


# Обработчик команды /info
@dp.message(Command("info"))
@dp.message(F.text.lower() == "информация")
async def cmd_info(message: types.Message):
    await message.answer(
        "Этот бот создан для хакатона:\n"
    )


@dp.message(Command("create_qr_code"))
async def cmd_info(message: types.Message):
    info = json.loads(message.model_dump_json())
    tg_id = "@" + info["from_user"]["username"]
    status, post = get_user_info(tg_id, info)

    if status != 200 or post != "ученик":
        await message.answer(
            "Не хватает прав на использование бота\n"
            "Чтобы решить эту проблему обратитесь к администратору"
        )

    # url = "http://127.0.0.1:8080/api/getQR"
    # res = requests.get(url, {"tg_id": tg_id})
    #
    # res.status_code != 200
    #
    # try:
    #     # Открываем и отправляем фото
    #     with open(PATH_OUTPUT, 'rb') as photo:
    #         await message.reply_photo(photo, caption="Вот ваше изображение!")
    # except Exception as e:
    #     await message.reply(f"Произошла ошибка: {e}")



@dp.message(Command("read_qr_code"))
async def cmd_read(message: types.Message, state: FSMContext):
    info = json.loads(message.model_dump_json())
    tg_id = "@" + info["from_user"]["username"]
    status, post = get_user_info(tg_id, info)

    if status != 200 or post != "учитель":
        await message.answer(
            "Не хватает прав на использование бота\n"
            "Чтобы решить эту проблему обратитесь к администратору"
        )

    await message.answer("Читаю изображение... Отправьте мне фото.")
    await state.set_state(ReadStates.waiting_for_image)


# Получение фото
@dp.message(ReadStates.waiting_for_image, F.photo)
async def handle_image(message: types.Message, state: FSMContext):
    # Получаем файл с максимальным разрешением
    photo = message.photo[-1]
    file_id = photo.file_id

    # Получаем информацию о файле
    file = await bot.get_file(file_id)
    file_path = file.file_path

    # Генерируем имя файла
    file_name = f"мусор.jpg"
    save_path = os.path.join(file_name)

    # Скачиваем и сохраняем файл
    file_data = await bot.download_file(file_path)
    with open(save_path, 'wb') as new_file:
        new_file.write(file_data.read())

    url = 'http://localhost:8080/api/upload'
    place_data = {"place": "Столовая"}  # можно написать вход либо выход
    files = {
        'file': open(save_path, 'rb'),
        'place': (None, str(place_data))  # Отправляем place как строку
    }

    response = requests.post(url, files=files)


# Обработчик случая, когда ожидается фото, но пришло что-то другое
@dp.message(ReadStates.waiting_for_image)
async def handle_wrong_input(message: types.Message):
    await message.answer("Пожалуйста, отправьте изображение.")


# Обработчик текстовых сообщений
@dp.message()
async def echo(message: types.Message):
    info = json.loads(message.model_dump_json())
    tg_id = "@" + info["from_user"]["username"]
    status, post = get_user_info(tg_id, info)
    if status != 200:
        await message.answer(
            "Не хватает прав на использование бота\n"
            "Чтобы решить эту проблему обратитесь к администратору"
        )

    if post == "ученик":
        await message.answer(
            "Это справочная информация:\n"
            "/start - начать сначала\n"
            "/help - помощь\n"
            "/info - информация\n"
            "/Create_qr_code - создать qr-code",
        )
    if post == "учитель":
        await message.answer(
            "Это справочная информация:\n"
            "/start - начать сначала\n"
            "/help - помощь\n"
            "/info - информация\n"
            "/read_qr_code - считать qr-code",
        )
    if post == "родитель":
        await message.answer(
            "Это справочная информация:\n"
            "/start - начать сначала\n"
            "/help - помощь\n"
            "/info - информация\n"
            "/about_child - о ребенке",
        )


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
