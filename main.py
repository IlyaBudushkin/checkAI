from config import API_TOKEN
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext
from telegram.ext import Application, ContextTypes

from downloader import handle_file
from file_processing.filling_template import filling_docx


async def button_resume(update: Update):
    await update.message.reply_text("Для составления резюме вам придется ответить на несколько вопросов.")
    new_text_list = []
    filling_docx('downloads/Шаблон.docx', new_text_list)

async def start(update: Update):
    buttons = [["Резюме"]]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("👋 Привет! Я — твой умный помощник в мире данных и документов!\n"
                                    "✨ Что я умею:\n"
                                    "✅ Создавать профессиональные резюме 📄 – просто ответь на пару вопросов, и я оформлю всё по красивому шаблону!\n"
                                    "📊 Строить диаграммы и графики из твоих таблиц – превращу скучные цифры в наглядную визуализацию!\n"
                                    "🧹 Чистить текст от невидимых символов и артефактов, которые оставляют ИИ – сделаю его идеально читаемым!\n"
                                    "\n"
                                    "Как начать?\n"
                                    "Просто выбери нужную кнопку:\n"
                                    "▫️ Резюме – создать резюме\n"
                                    "▫️ Анализ – построить график по вашим данным\n"
                                    "▫️ Чистка – очистить текст от следов ИИ\n", reply_markup=keyboard)

def main():
    # Создаем Application вместо Updater
    application = Application.builder().token(API_TOKEN).build()

    # Регистрируем обработчик
    # application.add_handler(
    #     MessageHandler(filters.Document.ALL | filters.PHOTO, handle_file)
    # )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^Резюме$"), button_resume))

    # Запускаем бота
    application.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())