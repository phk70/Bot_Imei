from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import apps.keyboards as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app import check_admin, validate_imei, delete_user, check_user_exists, save_user,check_user_permission, open_permission_user
router = Router()


class AddUser(StatesGroup):
    waiting_for_id = State()


class DelUser(StatesGroup):
    waiting_for_id = State()


class CheckIMEI(StatesGroup):
    waiting_for_imei = State()


@router.message(CommandStart())
async def start(message: Message):    
    if not check_user_exists(message.from_user.id):
        save_user(message.from_user.id)
    if not check_user_permission(message.from_user.id):
        await message.answer(f'Привет, {message.from_user.first_name}.\nУ вас нет доступа к боту. Обратитесь к администратору.')


    elif check_admin(message.from_user.id):
        await message.answer(f'Привет, {message.from_user.first_name}.\nТы администратор бота\nВыбери действие.', reply_markup=kb.admin)
    else: 
        await message.answer(f'Привет, {message.from_user.first_name}.\nВыбери действие.', reply_markup=kb.main)


@router.message(F.text=='Назад')
async def back(message: Message, state: FSMContext):
    if check_admin(message.from_user.id):
        await message.answer(f'Выбери действие.', reply_markup=kb.admin)
    else: 
        await message.answer(f'Выбери действие.', reply_markup=kb.main)
    await state.clear()

@router.message(F.text=='Добавить пользователя')
async def add_user(message: Message, state: FSMContext):    
    await state.set_state(AddUser.waiting_for_id)   
    await message.reply('Введите telegram_id пользователя для добавления', reply_markup=kb.back)


@router.message(AddUser.waiting_for_id)
async def enter_id_from_add(message: Message, state: FSMContext):
    await state.update_data(id=message.text)       
    data = await state.get_data()
    id = data['id']
    open_permission_user(id)
    await message.reply(f'Пользователю c telegram_id - {id} добавлен доступ к боту', reply_markup=kb.admin)
    await state.clear() 


@router.message(F.text=='Удалить пользователя')
async def del_user(message: Message, state: FSMContext):    
    await state.set_state(DelUser.waiting_for_id)   
    await message.reply('Введите telegram_id пользователя для удаления', reply_markup=kb.back)


@router.message(DelUser.waiting_for_id)
async def enter_id_from_del(message: Message, state: FSMContext):
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
    await state.set_state(CheckIMEI.waiting_for_imei)   
    await message.reply('Введите IMEI для проверки', reply_markup=kb.back)


@router.message(CheckIMEI.waiting_for_imei)
async def enter_imei(message: Message, state: FSMContext):    
    await state.update_data(imei=message.text)       
    data = await state.get_data()
    imei = data['imei']
    await state.clear()
    if validate_imei(imei):
        if check_admin(message.from_user.id):
            await message.reply(f'Подождите, ваш IMEI - {imei} проверяется', reply_markup=kb.admin)
        else: 
            await message.reply(f'Подождите, ваш IMEI - {imei} проверяется', reply_markup=kb.main)        
    else:       
        if check_admin(message.from_user.id):
            await message.reply(f'Вы ввели не корректный IMEI. Попробуйте ещё раз.', reply_markup=kb.admin)
        else: 
            await message.reply(f'Вы ввели не корректный IMEI. Попробуйте ещё раз.', reply_markup=kb.main)


# @router.callback_query(F.data == 'check_imei')
# async def check_imei(callback: CallbackQuery):
#     await callback.answer('')
#     await callback.message.answer('Введите IMEI для проверки')


# @router.message(Command('services'))
# async def services(message: Message):
    # await message.answer(f'Выбери действие.', reply_markup=await kb.get_services())
