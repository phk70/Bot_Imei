from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import os
import requests


TOKEN = '8098723084:AAFcdHWivkKHgQ4npufEhHpyPv7fO4UeCBA'

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Введите IMEI для проверки.')

async def register(update: Update, context: CallbackContext) -> None:
    telegram_id = update.message.from_user.id
    response = requests.post('http://localhost:5000/api/register', json={"telegram_id": telegram_id})

    if response.status_code == 201:
        token = response.json()['token']
        await update.message.reply_text(f'Вы успешно зарегистрированы! Ваш токен: {token}')
    else:
        await update.message.reply_text('Ошибка регистрации.')

async def check_imei(update: Update, context: CallbackContext) -> None:
    imei = update.message.text
    print(f"Полученный IMEI: {imei}")  

    user_token = 'USER_AUTH_TOKEN'  # Тут нужно будет реализовать метод получения токена пользователя
    response = requests.post('http://localhost:5000/api/check-imei', json={"imei": imei, "token": user_token})

    print(f"Статус код ответа: {response.status_code}")
    if response.status_code == 200:
        services = response.json()
        # Отправьте сообщение пользователю с сервисами
    else:
        # Обработка ошибок
        await update.message.reply_text(response.json().get("error", "Произошла ошибка."))

def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_imei))

    app.run_polling()

if __name__ == '__main__':
    main()