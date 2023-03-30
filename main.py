import asyncio
import logging
from aiogram.handlers import InlineQueryHandler
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message,InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton
from quickdb_Help import MONGODB
from aiogram.types import InputMediaPhoto,InputFile
import requests
import random
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import FSInputFile,InputMedia,InputMediaPhoto
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
from pytz import timezone
from aiogram.utils.keyboard import InlineKeyboardBuilder
import requests # Модуль для обработки URL
from bs4 import BeautifulSoup # Модуль для работы с HTML
import time # Модуль для остановки программы
import smtplib # Модуль для работы с почтой
from aiogram import Router
from aiogram.filters import Filter
from aiogram.types import Message


class Handler(Filter):
    def __init__(self,text) -> None:
       self.text= text

    async def __call__(self, message: Message) -> bool:

        try:
         print(message.text)
         return message.text == self.text
        except:
            pass
    

db = MONGODB(
    mongouri="mongodb://mongo:0cYDn1eBCEXPj8xmE8CI@containers-us-west-148.railway.app:5758",
    collection="StarCard",
    db="Card"
              )
keyboard = ReplyKeyboardMarkup(
    keyboard=[
     [KeyboardButton(text="🍀 Получить карту")],],
    
    resize_keyboard=True,
    row_width=3
)
TOKEN = "5647489863:AAEQ985yPzihTFx6rwqD01hEfn4RScKmSDw"
router = Router()
bot = Bot(TOKEN, parse_mode="HTML")
dp = Dispatcher()

@router.message(Handler('/card'))
async def t(message:Message):
   await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile("card_image/Vegapunk.jpg"),caption=f'🌠 Держи свою карточку\n\n<b>Vegapunk</b>\n\n💫 Редкость: Четыре звезды (+4звезд)\n☀️ Всего: {db.get(f"user_{message.from_user.id}")} звёзд\n\n🕛 Следущая попытка будет доступна через <b>4 часа.</b> Приходите снова!')



@router.message(Handler('/start'))
async def start(message:Message):
   await bot.send_message(chat_id=message.chat.id,text=f"Кнопки Успешно были добавлены",reply_markup=keyboard)

@router.message(Handler('/s'))
async def start(message:Message):
   if db.get(f'time_{message.from_user.id}') is not None:await bot.send_message(chat_id=message.chat.id,text=f"Дождитесь снятие КД!",)
   generator = random.randint(0,100)
   if generator < 5:
      image = random.choice(['Vegapunk','Monkey D Luffy'])
      if image == "Vegapunk":
         if db.get(f'Vegapunk_{message.from_user.id}') is None:
            db.add(f'user_{message.from_user.id}',4) or 0
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile("card_image/Vegapunk.jpg"),caption=f'🌠 Держи свою карточку\n\n<b>Vegapunk</b>\n\n💫 Редкость: Четыре звезды (+4 звезд)\n☀️ Всего: {db.get(f"user_{message.from_user.id}")} звёзд\n\n🕛 Следущая попытка будет доступна через 4 часа. Приходите снова!')
            db.set(f'Vegapunk_{message.from_user.id}',".")
             
         if db.get(f'Vegapunk_{message.from_user.id}') is not None:
            db.add(f'user_{message.from_user.id}',4) or 0
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile("card_image/Vegapunk.jpg"),caption=f'🌠 Держи свою карточку\n\n<b>Vegapunk (Дубликат)</b>\n\n💫 Редкость: Четыре звезды (+4 звезд)\n☀️ Всего: {db.get(f"user_{message.from_user.id}")} звёзд\n\n🕛 Следущая попытка будет доступна через 4 часа. Приходите снова!')
             
      if image == "Monkey D Luffy":
         if db.get(f'Monkey D Luffy_{message.from_user.id}') is None:
            db.add(f'user_{message.from_user.id}',4) or 0
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile("card_image/Monkey.D.Luffy.jpg"),caption=f'🌠 Держи свою карточку\n\n<b>Monkey D Luffy</b>\n\n💫 Редкость: Четыре звезды (+4 звезд)\n☀️ Всего: {db.get(f"user_{message.from_user.id}")} звёзд\n\n🕛 Следущая попытка будет доступна через 4 часа. Приходите снова!')
            db.set(f'Monkey D Luffy_{message.from_user.id}',".")
             
         if db.get(f'Monkey D Luffy_{message.from_user.id}') is not None:
            db.add(f'user_{message.from_user.id}',4) or 0
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile("card_image/Monkey.D.Luffy.jpg"),caption=f'🌠 Держи свою карточку\n\n<b>Monkey D Luffy (Дубликат)</b>\n\n💫 Редкость: Четыре звезды (+4 звезд)\n☀️ Всего: {db.get(f"user_{message.from_user.id}")} звёзд\n\n🕛 Следущая попытка будет доступна через 4 часа. Приходите снова!')
             
         
   if generator < 10:
      image = random.choice(['Crocodile','King','Roronoa'])
      if image == "Crocodile":
         if db.get(f'Crocodile_{message.from_user.id}') is None:
            db.add(f'user_{message.from_user.id}',3) or 0
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile("card_image/Crocodile.jpg"),caption=f'🌠 Держи свою карточку\n\n<b>Crocodile</b>\n\n💫 Редкость: Три звезды (+3 звезд)\n☀️ Всего: {db.get(f"user_{message.from_user.id}")} звёзд\n\n🕛 Следущая попытка будет доступна через 4 часа. Приходите снова!')
            db.set(f'Crocodile_{message.from_user.id}',".")
             
         if db.get(f'Crocodile_{message.from_user.id}') is not None:
            db.add(f'user_{message.from_user.id}',3) or 0
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile("card_image/Crocodile.jpg"),caption=f'🌠 Держи свою карточку\n\n<b>Crocodile (Дубликат)</b>\n\n💫 Редкость: Три звезды (+3 звезд)\n☀️ Всего: {db.get(f"user_{message.from_user.id}")} звёзд\n\n🕛 Следущая попытка будет доступна через 4 часа. Приходите снова!')
             
      if image == "King":
         if db.get(f'King_{message.from_user.id}') is None:
            db.add(f'user_{message.from_user.id}',3) or 0
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile("card_image/King.jpg"),caption=f'🌠 Держи свою карточку\n\n<b>King</b>\n\n💫 Редкость: Три звезды (+3 звезд)\n☀️ Всего: {db.get(f"user_{message.from_user.id}")} звёзд\n\n🕛 Следущая попытка будет доступна через 4 часа. Приходите снова!')
            db.set(f'King_{message.from_user.id}',".")
             
         if db.get(f'King_{message.from_user.id}') is not None:
            db.add(f'user_{message.from_user.id}',3) or 0
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile("card_image/King.jpg"),caption=f'🌠 Держи свою карточку\n\n<b>King (Дубликат)</b>\n\n💫 Редкость: Три звезды (+3 звезд)\n☀️ Всего: {db.get(f"user_{message.from_user.id}")} звёзд\n\n🕛 Следущая попытка будет доступна через 4 часа. Приходите снова!')
             
      if image == "Roronoa":
         if db.get(f'Roronoa_{message.from_user.id}') is None:
            db.add(f'user_{message.from_user.id}',3) or 0
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile("card_image/Roronoa Zoro.jpg"),caption=f'🌠 Держи свою карточку\n\n<b>Roronoa Zoro</b>\n\n💫 Редкость: Три звезды (+3 звезд)\n☀️ Всего: {db.get(f"user_{message.from_user.id}")} звёзд\n\n🕛 Следущая попытка будет доступна через 4 часа. Приходите снова!')
            db.set(f'Roronoa_{message.from_user.id}',".")
             
         if db.get(f'Roronoa_{message.from_user.id}') is not None:
            db.add(f'user_{message.from_user.id}',3) or 0
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile("card_image/Roronoa Zoro.jpg"),caption=f'🌠 Держи свою карточку\n\n<b>Roronoa Zoro (Дубликат)</b>\n\n💫 Редкость: Три звезды (+3 звезд)\n☀️ Всего: {db.get(f"user_{message.from_user.id}")} звёзд\n\n🕛 Следущая попытка будет доступна через 4 часа. Приходите снова!')
             
         
   if generator < 15:
      image = random.choice(['Basil','Cracker','Perona'])
      if image == "Basil":
         if db.get(f'Basil_{message.from_user.id}') is None:
            db.add(f'user_{message.from_user.id}',2) or 0
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile("card_image/Basil.jpg"),caption=f'🌠 Держи свою карточку\n\n<b>Basil</b>\n\n💫 Редкость: Две звезды (+2 звезд)\n☀️ Всего: {db.get(f"user_{message.from_user.id}")} звёзд\n\n🕛 Следущая попытка будет доступна через 4 часа. Приходите снова!')
            db.set(f'Basil_{message.from_user.id}',".")
             
         if db.get(f'Basil_{message.from_user.id}') is not None:
            db.add(f'user_{message.from_user.id}',2) or 0
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile("card_image/Basil.jpg"),caption=f'🌠 Держи свою карточку\n\n<b>Basil (Дубликат)</b>\n\n💫 Редкость: Две звезды (+2 звезд)\n☀️ Всего: {db.get(f"user_{message.from_user.id}")} звёзд\n\n🕛 Следущая попытка будет доступна через 4 часа. Приходите снова!')
             
      if image == "Cracker":
         if db.get(f'Cracker_{message.from_user.id}') is None:
            db.add(f'user_{message.from_user.id}',2) or 0
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile("card_image/Cracker.jpg"),caption=f'🌠 Держи свою карточку\n\n<b>Cracker</b>\n\n💫 Редкость: Две звезды (+2 звезд)\n☀️ Всего: {db.get(f"user_{message.from_user.id}")} звёзд\n\n🕛 Следущая попытка будет доступна через 4 часа. Приходите снова!')
            db.set(f'Cracker{message.from_user.id}',".")
             
         if db.get(f'Cracker_{message.from_user.id}') is not None:
            db.add(f'user_{message.from_user.id}',2) or 0
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile("card_image/Cracker.jpg"),caption=f'🌠 Держи свою карточку\n\n<b>Cracker (Дубликат)</b>\n\n💫 Редкость: Две звезды (+2 звезд)\n☀️ Всего: {db.get(f"user_{message.from_user.id}")} звёзд\n\n🕛 Следущая попытка будет доступна через 4 часа. Приходите снова!')
             
      if image == "Perona":
         if db.get(f'Perona_{message.from_user.id}') is None:
            db.add(f'user_{message.from_user.id}',2) or 0
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile("card_image/Perona.jpg"),caption=f'🌠 Держи свою карточку\n\n<b>Perona</b>\n\n💫 Редкость: Две звезды (+2 звезд)\n☀️ Всего: {db.get(f"user_{message.from_user.id}")} звёзд\n\n🕛 Следущая попытка будет доступна через 4 часа. Приходите снова!')
            db.set(f'Perona_{message.from_user.id}',".")
             
         if db.get(f'Perona_{message.from_user.id}') is not None:
            db.add(f'user_{message.from_user.id}',2) or 0
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile("card_image/Perona.jpg"),caption=f'🌠 Держи свою карточку\n\n<b>Perona(Дубликат)</b>\n\n💫 Редкость: Две звезды (+2 звезд)\n☀️ Всего: {db.get(f"user_{message.from_user.id}")} звёзд\n\n🕛 Следущая попытка будет доступна через 4 часа. Приходите снова!')
             
   if generator < 70:
      image = random.choice(['Kalifa','Cracker','Perona'])
      if image == "Kalifa":
         if db.get(f'Kalifa_{message.from_user.id}') is None:
            db.add(f'user_{message.from_user.id}',1) or 0
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile("card_image/Kalifa.jpg"),caption=f'🌠 Держи свою карточку\n\n<b>Kalifa</b>\n\n💫 Редкость: Одна звезда (+1 звезда)\n☀️ Всего: {db.get(f"user_{message.from_user.id}")} звёзд\n\n🕛 Следущая попытка будет доступна через 4 часа. Приходите снова!')
            db.set(f'Kalifa_{message.from_user.id}',".")
             
         if db.get(f'Kalifa_{message.from_user.id}') is not None:
            db.add(f'user_{message.from_user.id}',1) or 0
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile("card_image/Kalifa.jpg"),caption=f'🌠 Держи свою карточку\n\n<b>Kalifa (Дубликат)</b>\n\n💫 Редкость:Одна звезды (+1 звезда)\n☀️ Всего: {db.get(f"user_{message.from_user.id}")} звёзд\n\n🕛 Следущая попытка будет доступна через 4 часа. Приходите снова!')
             
      if image == "Shakuyaku":
         if db.get(f'Shakuyaku_{message.from_user.id}') is None:
            db.add(f'user_{message.from_user.id}',1) or 0
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile("card_image/Shakuyaku.jpg"),caption=f'🌠 Держи свою карточку\n\n<b>Shakuyaku</b>\n\n💫 Редкость: Одна звезды (+1 звезда)\n☀️ Всего: {db.get(f"user_{message.from_user.id}")} звёзд\n\n🕛 Следущая попытка будет доступна через 4 часа. Приходите снова!')
            db.set(f'Shakuyaku_{message.from_user.id}',".")
             
         if db.get(f'Shakuyaku_{message.from_user.id}') is not None:
            db.add(f'user_{message.from_user.id}',1) or 0
            await bot.send_photo(chat_id=message.chat.id,photo=FSInputFile("card_image/Shakuyaku.jpg"),caption=f'🌠 Держи свою карточку\n\n<b>Shakuyaku (Дубликат)</b>\n\n💫 Редкость: Одна звезды (+1 звезда)\n☀️ Всего: {db.get(f"user_{message.from_user.id}")} звёзд\n\n🕛 Следущая попытка будет доступна через 4 часа. Приходите снова!')
            
         await bot.send_message(chat_id=message.chat.id,text='test')


async def main() -> None:
    # Dispatcher is a root router
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode="HTML")
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
