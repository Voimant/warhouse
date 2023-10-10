from aiogram import types, Dispatcher, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.types import FSInputFile, BufferedInputFile
from pprint import pprint
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from keyboards import main_markup, input_markup, gen_markup, output_markup
from create_bot import bot
from warehouse_db.DB import conn
from warehouse_db.main_db import data_order, add_order


class FSMput(StatesGroup):
    name = State()
    sheif = State()
    shelves = State()
    pices = State()
    namb_of_zakaz = State()
    ready_z = State()

class FSMoput(StatesGroup):
    name = State()
    pices = State()
    ready_s = State()


async def cmd_start(message: types.Message):
    await bot.send_message(message.chat.id, 'Складской бот, что нужно сделать?', reply_markup=main_markup)


async def input_warhouse(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, 'Введите название',)
    await state.set_state(FSMput.name)


async def input_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await bot.send_message(message.chat.id, 'Введите номер стелажа')
    await state.set_state(FSMput.sheif)


async def input_shelves(message: types.Message, state: FSMContext):
    await state.update_data(sheif=message.text)
    await bot.send_message(message.chat.id, "Введите номер полки")
    await state.set_state(FSMput.shelves)


async def input_pices(message: types.Message, state: FSMContext):
    await state.update_data(shelves=message.text)
    await bot.send_message(message.chat.id, 'Введите количество?')
    await state.set_state(FSMput.pices)


async def input_zakaz(message: types.Message, state: FSMContext):
    await state.update_data(pices=message.text)
    await bot.send_message(message.chat.id, 'для какого заказа?')
    await state.set_state(FSMput.namb_of_zakaz)


async def input_ready_z(message: types.Message, state: FSMContext):
    await state.update_data(namb_of_zakaz=message.text)

    data = await state.get_data()
    print(data)
    x = f"""
    Название: {data['name']}
    Стелаж: {data['sheif']}
    Полка: {data['shelves']}
    Кол-во: {data['pices']}
    Номер заказа: {data['namb_of_zakaz']}"""
    await bot.send_message(message.chat.id, x)
    await bot.send_message(message.chat.id, 'если все правильно нажмите <ВНЕСТИ НА СКЛАД>, Что бы изменить <ОТМЕНА>',
                        reply_markup=input_markup)


async def inpute_base(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'input':
        data = await state.get_data()
        print(data)
        x = f"""
        Название: {data['name']}
        Стелаж: {data['sheif']}
        Полка: {data['shelves']}
        Кол-во: {data['pices']}
        Номер заказа: {data['namb_of_zakaz']}"""
        add_order(data['namb_of_zakaz'])
        conn.commit()
        data_order(data['sheif'], data['shelves'], data['name'], data['pices'], data['namb_of_zakaz'])
        conn.commit()
        await bot.send_message(call.from_user.id, x)
        await state.clear()


async def input_final_cancel(call: types.CallbackQuery, state: FSMContext):
        await state.clear()
        await bot.send_message(call.from_user.id, 'Складской бот, что нужно сделать?', reply_markup=main_markup)


async def output_s(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, 'что будем забирать', reply_markup=gen_markup())
    await state.set_state(FSMoput.name)


async def outuput_state_name(call:types.CallbackQuery, state: FSMContext):
    await state.update_data(name=call.data)
    await bot.send_message(call.from_user.id, 'Какое количество требуется')
    await state.set_state(FSMoput.pices)


async def ready_output(message: types.Message, state: FSMContext):
    await state.update_data(pices=message.text)
    await bot.send_message(message.chat.id, 'Уверены что хотите снять со склада товар?', reply_markup=output_markup)


async def get_update_negative(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(ready_s=call.data)
    data = await state.get_data()





def register_handlers(dp: Dispatcher):
    """*******************ЗАБРАТЬ СО СКЛАДА*********************"""
    dp.message.register(ready_output, FSMoput.pices)
    dp.callback_query.register(outuput_state_name, FSMoput.name)
    dp.callback_query.register(output_s, F.data == 'output_w')
    """*********************COMMANDS*************************"""
    dp.message.register(cmd_start, Command('start'))
    """*************************ПОЛОЖИТЬ НА СКЛАД******************************"""
    dp.callback_query.register(input_warhouse, F.data == 'input_w')
    dp.message.register(input_name, FSMput.name)
    dp.message.register(input_shelves, FSMput.sheif)
    dp.message.register(input_pices, FSMput.shelves)
    dp.message.register(input_zakaz, FSMput.pices)
    dp.message.register(input_ready_z, FSMput.namb_of_zakaz)
    dp.callback_query.register(input_final_cancel, F.data == 'cancel')
    dp.callback_query.register(inpute_base, F.data == 'input')




