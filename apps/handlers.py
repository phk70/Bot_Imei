from gc import callbacks
from aiogram import F, Router, filters
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import apps.keyboards as kb
from apps.states import *
from app import create_db, check_admin, validate_imei, delete_user, check_user_exists, save_user, check_user_permission, open_permission_user
from apps.services import get_services
# import apps.services as services  # берем даннные из клавиатуры по простому


router = Router()

@router.message(CommandStart())
async def start(message: Message):   
    '''Обработка команды /start'''
    create_db()
    if not check_user_exists(message.from_user.id):
        save_user(message.from_user.id)
    
    elif not check_user_permission(message.from_user.id):
        await message.answer(f'Привет, {message.from_user.first_name}.\nУ вас нет доступа к боту. Обратитесь к администратору.')
    
    elif check_admin(message.from_user.id):
        await message.answer(f'Привет, {message.from_user.first_name}.\nТы администратор бота\nВыбери действие.', reply_markup=kb.admin)

    else: 
        await message.answer(f'Привет, {message.from_user.first_name}.\nВыбери действие.', reply_markup=kb.main)
    

@router.message(F.text=='Назад')
async def back(message: Message, state: FSMContext):
    '''Обработка команды /back при использовании reply клавиатуры'''
    if check_admin(message.from_user.id):
        await message.answer(f'Выбери действие.', reply_markup=kb.admin)
    else: 
        await message.answer(f'Выбери действие.', reply_markup=kb.main)
    await state.clear()


@router.message(F.text=='Добавить пользователя')
async def add_user(message: Message, state: FSMContext):   
    '''Ожидание telegram_id пользователя для добавления'''
    await state.set_state(AddUser.waiting_for_id)   
    await message.reply('Введите telegram_id пользователя для добавления', reply_markup=kb.back)


@router.message(AddUser.waiting_for_id)
async def enter_id_from_add(message: Message, state: FSMContext):
    '''Предоставление пользователю прав доступа к боту'''
    await state.update_data(id=message.text)       
    data = await state.get_data()
    id = data['id']
    if open_permission_user(id):
        await message.reply(f'Пользователю c telegram_id - {id} добавлен доступ к боту', reply_markup=kb.admin)
        await state.clear()
    else:
        await message.reply(f'Пользователь c telegram_id - {id} не найден', reply_markup=kb.admin)
        await state.clear()


@router.message(F.text=='Удалить пользователя')
async def del_user(message: Message, state: FSMContext):    
    '''Ожидание telegram_id пользователя для удаления'''
    await state.set_state(DelUser.waiting_for_id)   
    await message.reply('Введите telegram_id пользователя для удаления', reply_markup=kb.back)


@router.message(DelUser.waiting_for_id)
async def enter_id_from_del(message: Message, state: FSMContext):
    '''Удаление пользователя из базы данных'''
    await state.update_data(id=message.text)       
    data = await state.get_data()
    id = data['id']
    if check_user_exists(id):
        delete_user(id)
        await message.reply(f'Пользователь c telegram_id - {id} удален из базы', reply_markup=kb.admin)
        await state.clear()
    else:
        await message.reply('Такого пользователя нет в базе данных', reply_markup=kb.admin) 
        await state.clear()


@router.message(F.text=='Проверить IMEI')
async def check_imei(message: Message, state: FSMContext):    
    '''Ожидание IMEI для проверки'''
    await state.set_state(CheckIMEI.waiting_for_imei)   
    await message.reply('Введите IMEI для проверки', reply_markup=kb.back)


@router.message(CheckIMEI.waiting_for_imei)
async def enter_imei(message: Message, state: FSMContext):    
    '''Проверка IMEI на корректность'''
    await state.update_data(imei=message.text)       
    data = await state.get_data()
    imei = data['imei']
    await state.clear()
    if validate_imei(imei):
        await message.answer(f'Доступные сервисы', reply_markup=kb.services_kb.adjust(1).as_markup())  # Отображение всех сервисов    
    else:       
        if check_admin(message.from_user.id):
            await message.reply(f'Вы ввели не корректный IMEI. Попробуйте ещё раз.', reply_markup=kb.admin)
        else: 
            await message.reply(f'Вы ввели не корректный IMEI. Попробуйте ещё раз.', reply_markup=kb.main)
    



@router.callback_query()
async def service_payment(callback_query: CallbackQuery):
    service_name = callback_query.data  # Получаем данные callback
    print(service_name)
    await bot.send_message(callback_query.from_user.id, f"Услуга {service_name} оплачена!")
    
    # Отвечаем на callback_query, чтобы убрать "часики"
    await callback_query.answer()


@router.message()
async def none_message(message: Message):
    if check_admin(message.from_user.id):
        await message.reply(f'Не понимаю, что ты хочешь...', reply_markup=kb.admin)
    else: 
        await message.reply(f'Не понимаю, что ты хочешь...', reply_markup=kb.main)



# @router.callback_query(F.data == 'check_imei')
# async def check_imei(callback: CallbackQuery):
#     await callback.answer('')
#     await callback.message.answer('Введите IMEI для проверки')


# @router.message(Command('services'))
# async def services(message: Message):
    # await message.answer(f'Выбери действие.', reply_markup=await kb.get_services())
