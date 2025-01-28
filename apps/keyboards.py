from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
# from services import get_services, purchase_service


# Создание клавиатуры для пользователя
main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Проверить IMEI')]], resize_keyboard=True, one_time_keyboard=False)


# Создание клавиатуры для администратора
admin = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Проверить IMEI')
    ],
    [
        KeyboardButton(text='Добавить пользователя'),
        KeyboardButton(text='Удалить пользователя')]], resize_keyboard=True, one_time_keyboard=False)


# Кнопка назад
back = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Назад')]], resize_keyboard=True, one_time_keyboard=True)


# Создание клавиатуры с услугами
services_kb = InlineKeyboardBuilder()
# services = get_services()
services = [
        {'name': 'service1', 'price': 1000, 'balance': 100}, 
        {'name': 'service2', 'price': 2000, 'balance': 2000}, 
        {'name': 'service3', 'price': 3000, 'balance': 2514}
        ]    
for service in services:    
    button_text = f"{service['name']} - Баланс: {service['balance']} - Цена: {service['price']}"
    button = InlineKeyboardButton(text=button_text, callback_data=service['name'])  # Используем имя сервиса как callback_data
    services_kb.add(button)



