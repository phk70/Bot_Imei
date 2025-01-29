from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Проверить IMEI')]], resize_keyboard=True, one_time_keyboard=False)


admin = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Проверить IMEI')
    ],
    [
        KeyboardButton(text='Добавить пользователя'),
        KeyboardButton(text='Удалить пользователя')]], resize_keyboard=True, one_time_keyboard=False)


back = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Назад')]], resize_keyboard=True, one_time_keyboard=True)


async def services_kb():
    services_kb = InlineKeyboardBuilder()
    # services = get_services()
    services = [
            {'name': 'service1', 'price': 1000, 'balance': 100}, 
            {'name': 'service2', 'price': 2000, 'balance': 2000}, 
            {'name': 'service3', 'price': 3000, 'balance': 2514}
            ]    
    for service in services:    
        button_text = f"{service['name']} - Цена: {service['price']} - Баланс: {service['balance']}"
        print(button_text)
        button = InlineKeyboardButton(text=button_text, callback_data=service['name']) 
        services_kb.add(button)
    print(services_kb)
    return services_kb.adjust(1).as_markup()


