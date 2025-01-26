from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
# import services
# from app import check_admin


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Проверить IMEI')]], resize_keyboard=True, one_time_keyboard=False)

admin = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Проверить IMEI')
    ],
    [
        KeyboardButton(text='Добавить пользователя'),
        KeyboardButton(text='Удалить пользователя')]], resize_keyboard=True, one_time_keyboard=False)

back = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Назад')]], resize_keyboard=True, one_time_keyboard=True)

# main = InlineKeyboardMarkup(inline_keyboard=[
#     [
#         InlineKeyboardButton(text='Проверить IMEI', callback_data='check_imei')        
#     ]
# ])

# admin = InlineKeyboardMarkup(inline_keyboard=[
#     [
#         InlineKeyboardButton(text='Проверить IMEI', callback_data='check_imei'),
#         InlineKeyboardButton(text='Добавить пользователя', callback_data='add_user'),
#         InlineKeyboardButton(text='Удалить пользователя', callback_data='del_user')
#     ]
# ])


# setttings = InlineKeyboardMarkup(inline_keyboard=[
#     [
#         InlineKeyboardButton(text='Добавить пользователя', callback_data='add_user'),
#         InlineKeyboardButton(text='Удалить пользователя', callback_data='del_user'),
#         InlineKeyboardButton(text='Перейти на сайт', url='https://trip-map.ru')
#     ]
# ])

# services = ['123', '456', '789']

# async def get_services():
#     keyboard = InlineKeyboardBuilder()
#     for i in services:
#         keyboard.add(InlineKeyboardButton(text=i, callback_data=i))
#     return keyboard.adjust(1).as_markup()