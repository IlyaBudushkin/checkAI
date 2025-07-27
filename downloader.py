import os
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters
)
from PIL import Image




async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    # Определяем тип файла
    if message.document:
        file = message.document
        file_type = "document"
    elif message.photo:
        file = message.photo[-1]
        file_type = "photo"
    else:
        await message.reply_text("Пожалуйста, отправьте файл (документ или фото).")
        return

    # Получаем информацию о файле
    file_id = file.file_id
    file_name = getattr(file, 'file_name', None)
    mime_type = getattr(file, 'mime_type', None)

    if not file_name:
        file_name = f"file_{file_id[:8]}"

    # Определяем расширение
    if '.' in file_name:
        extension = file_name.split('.')[-1].lower()
    elif mime_type:
        extension = mime_type.split('/')[-1]
    else:
        extension = "unknown"

    await message.reply_text(
        f"📄 Имя файла: {file_name}\n"
        f"🔖 Тип файла: {file_type}\n"
        f"📌 MIME-тип: {mime_type}\n"
        f"🔍 Расширение: {extension}"
    )

    # Скачиваем файл (ВАЖНО: используем await!)
    file_obj = await context.bot.get_file(file_id)
    os.makedirs("downloads", exist_ok=True)
    file_path = os.path.join("downloads", f"{file_name}.{extension}" if '.' not in file_name else file_name)

    # Используем download_to_drive вместо download
    await file_obj.download_to_drive(file_path)

    await message.reply_text(f"✅ Файл сохранён: {file_path}")

    # Обработка файла
    if extension in ['jpg', 'jpeg', 'png']:
        try:
            img = Image.open(file_path)
            img.thumbnail((200, 200))
            thumb_path = os.path.join("downloads", f"thumb_{file_name}.jpg")
            img.save(thumb_path)
            await message.reply_photo(photo=open(thumb_path, 'rb'))
        except Exception as e:
            await message.reply_text(f"❌ Ошибка обработки изображения: {e}")

    elif extension == 'txt':
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(500)
                await message.reply_text(f"📝 Содержимое TXT:\n{content}")
        except Exception as e:
            await message.reply_text(f"❌ Ошибка чтения файла: {e}")

    elif extension == 'pdf':
        await message.reply_text("📚 Это PDF-файл. Можно обработать с помощью PyPDF2.")
    else:
        await message.reply_text("🤷‍♂️ Неизвестный формат файла.")