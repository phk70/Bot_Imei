import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from apps.handlers import router

load_dotenv()


bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
dp = Dispatcher() 




async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())















# def main_keyboard(user_telegram_id: int):     
#     if check_admin(user_telegram_id):
#         kb_list = [[KeyboardButton(text='Добавить пользователя'), KeyboardButton(text='Удалить пользователя')]]
#         keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=False)    
#         return keyboard


# @dp.message(Command('start'))
# async def start(message: types.Message):
#     '''Запуск бота'''
#     if check_admin(message.from_user.id):
#         await message.answer(f'Привет, {message.from_user.first_name}.\nВведи IMEI для проверки.', reply_markup=main_keyboard(message.from_user.id))

#     elif check_user_exists(message.from_user.id):
#         await message.answer(f'Привет, {message.from_user.first_name}.\nВведи IMEI для проверки.')
#     else:
#         await message.answer(f'Привет, {message.from_user.first_name}.\nУ тебя нет доступа к боту. Пожалуйста, зарегистрируйся.')


# last_messages = []  # Для того чтобы держать в памяти последнее сообщение чата

# @dp.message(Command('Удалить пользователя'))
# async def store_message(message: types.Message):    
#     last_messages.append(message.text) # Добавляем последнее сообщение в список типа "кеш":)    
    

# @dp.message()
# async def del_user(message: types.Message):    
#     print(last_messages[-1])    
#     if last_messages[-1]=='Удалить пользователя':
#         await message.answer('Введите telegram_id пользователя для удаления.')
#         telegram_id_for_delete = message.text  #Получаем элемент из списка        
#         delete_user(telegram_id_for_delete)
#         await message.answer(f'Пользователь c telegram_id - {telegram_id_for_delete} удален из базы данных.')

#     if last_messages[-1]=='Добавить пользователя': 
#         await message.answer('Введите telegram_id пользователя')
#         telegram_id_for_add = int(message.text)  # Получаем элемент из списка        
#         permission_user_exists(telegram_id_for_add)
#         await messsage.answer(f'Пользовател. c telegram_id - {telegram_id_for_delete} добавлен доступ к боту.')
        

# @dp.message()
# async def add_user(message: types.Message):
#     await message.answer('Введите telegram_id пользователя')
#     if last_messages:
#         last_msg = int(last_messages[0])  # Получаем элемент из списка
#         permission_user_exists(last_msg)
#         await message.answer(f'Пользователю c telegram_id - {last_msg} добавлен доступ к боту')
#     else:
#         await message.answer('Вы не ввели telegram_id пользователя.')


# @dp.message()
# async def del_user(message: types.Message):    
#     print(last_messages[-1])
#     if last_messages[-1]=='Удалить пользователя':
#         await message.answer('Введите telegram_id пользователя для удаления')
#         telegram_id_for_delete = int(message.text)  # Получаем элемент из списка        
#         delete_user(telegram_id_for_delete)
#         await message.answer(f'Пользователь c telegram_id - {telegram_id_for_delete} удален из базы данных') 



# @dp.message(Command('register'))
# async def register(message: types.Message):
#     '''Регистрация пользователя'''   
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     btn = types.KeyboardButton("Регистрация")
#     markup.add(btn)
#     await message.answer(reply_markup=markup)


# @dp.message()
# async def check_imei(message: types.Message):
#     '''Проверка IMEI'''
#     imei = message.text
#     if imei_is_valid(imei):  # Если IMEI валиден отправляем его по адресу API, передавая его и токен в теле запроса. Или просим ввести ещё раз
#         await message.reply(f"Ваш IMEI: {imei}\nПодождите завершения проверки.")
#         response = requests.post('http://localhost:5000/api/check-imei', json={'imei': imei, 'token': 'YOUR_TOKEN'})

#         if response.status_code == 200:  # Если запрос прошел успешно показываем пользователю список доступных услуг. Или выводим сообщение об ошибке
#             services = response.json()            
#             markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#             for service in services:
#                 btn = types.KeyboardButton(service['service_name'])
#                 markup.add(btn)
#             await message.answer("Выберите сервис:", reply_markup=markup)
#         else:
#             await message.answer("Ошибка при получении услуг.")
#     else:
#         await message.reply("Вы ввели не корректный IMEI. Попробуйте ещё раз.")


# def imei_is_valid(imei):
#     '''Валидация введенного IMEI по длине и составу'''
#     return (len(imei) in [15]) and imei.isdigit()








# bot = Bot(token=API_TOKEN)
# storage = MemoryStorage()
# dp = Dispatcher(bot, storage=storage)

# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     await message.answer("Привет! Отправь IMEI для проверки.")

# @dp.message_handler(func=lambda message: True)
# async def handle_imei(message: types.Message):
#     imei = message.text.strip()  # Получаем IMEI из сообщения
#     if not is_valid_imei(imei):
#         await message.answer("Некорректный IMEI. Попробуйте снова.")
#         return
    
#     # Выполняем запрос к API для получения услуг
#     response = requests.post('http://localhost:5000/api/check-imei', json={'imei': imei, 'token': 'YOUR_TOKEN'})
    
#     if response.status_code == 200:
#         services = response.json()
#         # Здесь мы формируем клавиатуру с кнопками для каждого сервиса
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         for service in services:
#             btn = types.KeyboardButton(service['service_name'])
#             markup.add(btn)
#         await message.answer("Выберите сервис:", reply_markup=markup)
#     else:
#         await message.answer("Ошибка при получении услуг.")

# def is_valid_imei(imei):
#     # Здесь можно реализовать простую проверку IMEI
#     return len(imei) in [15]

# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)