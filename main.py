import asyncio
import telebot.async_telebot as telebot

API_TOKEN = 'ВАШ_ТОКЕН_ОТ_BOTFATHER'
bot = telebot.AsyncTeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.reply_to(message, "Привет! Я асинхронный бот!")

@bot.message_handler(func=lambda message: True)
async def echo_all(message):
    await bot.reply_to(message, message.text)

asyncio.run(bot.polling())