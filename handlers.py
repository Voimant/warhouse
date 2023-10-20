from aiogram import types, Dispatcher, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.types import FSInputFile, BufferedInputFile
from pprint import pprint
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from keyboards import main_markup, input_markup, gen_markup, output_markup, order_not_markup, cancel_markup, \
    gen_shelf_markup, gen_shelves_markup, position_button, redact_markup, search_menu_markup, admin_markup
from create_bot import bot
from warehouse_db.DB import conn
from warehouse_db.main_db import data_order, add_order, data_without_order, data_from_shelf, data_racks_shelf, \
    search_id, data_order_number, subtract_the_amount_without_order_number, search_data, warinfo, \
    partial_search_by_category, partial_search_by_order_number, all_data_csv


class FSMput(StatesGroup):
    name = State()
    sheif = State()
    shelves = State()
    pices = State()
    ither_or = State()
    namb_of_zakaz = State()
    ready_z = State()
    ready_s = State()
    ready_w = State()




async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await bot.send_message(message.chat.id, 'Складской бот, что нужно сделать?', reply_markup=main_markup)

async def cmd_admin(message: types.Message):
    await bot.send_message(message.chat.id, "Скачать актуальные запасы?", reply_markup=admin_markup)


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
    await bot.send_message(message.chat.id, 'Далее', reply_markup=order_not_markup)
    await state.set_state(FSMput.ready_z)




async def input_ready_z(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'not_order':
        data = await state.get_data()
        print(data)
        x = f"""
            Название: {data['name']}
            Стелаж: {data['sheif']}
            Полка: {data['shelves']}
            Кол-во: {data['pices']}"""
        await bot.send_message(call.from_user.id, x)
        await bot.send_message(call.from_user.id, 'если все правильно нажмите <ВНЕСТИ НА СКЛАД>, Что бы изменить <ОТМЕНА>',
                                reply_markup=input_markup)
        await state.set_state(FSMput.ready_w)

    elif call.data == 'with_order':
        await bot.send_message(call.from_user.id, 'введите номер заказа', reply_markup=cancel_markup)
        await state.set_state(FSMput.namb_of_zakaz)

async def final_with_order(message: types.Message, state:FSMContext):
    await state.update_data(namb_of_zakaz=message.text)
    data = await state.get_data()
    print(data)
    x = f"""
                Название: {data['name']}
                Стелаж: {data['sheif']}
                Полка: {data['shelves']}
                Кол-во: {data['pices']}
                Номер заказа: {data['namb_of_zakaz']}"""
    await bot.send_message(message.chat.id,  x)
    await bot.send_message(message.chat.id, 'если все правильно нажмите <ВНЕСТИ НА СКЛАД>, Что бы изменить <ОТМЕНА>',
                           reply_markup=input_markup)
    await state.set_state(FSMput.ready_s)


async def input_base_not_order(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'input':
        data = await state.get_data()
        data_without_order(data['sheif'], data['shelves'], data['name'], data['pices'])
        conn.commit()
        await state.clear()
        await bot.send_message(call.from_user.id, "Операция выполнена", reply_markup=main_markup)



async def inpute_base(call: types.CallbackQuery, state: FSMContext):
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


class FSMoput(StatesGroup):
    shelf = State()
    shelves = State()
    name = State()
    redakt = State()
    varik = State()
    zakaz = State()
    pices = State()
    ready_s = State()
    ready_out = State()

async def output_s(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, 'Выберете стелаж', reply_markup=gen_shelf_markup())
    await state.set_state(FSMoput.shelf)


async def outuput_state_shelves(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(shelf=call.data)
    data = await state.get_data()
    await bot.send_message(call.from_user.id, 'Выберете полку', reply_markup=gen_shelves_markup(str(data['shelf'])))
    await state.set_state(FSMoput.name)


async def ready_output(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(shelves=call.data)
    data = await state.get_data()
    await bot.send_message(call.from_user.id, 'Какой товар вы хотите забрать?', reply_markup=position_button(data['shelf'], (data['shelves'])))
    print(data_from_shelf(data['shelf'], int(data['shelves'])))
    await state.set_state(FSMoput.redakt)

async def get_update_negative(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(ready_s=call.data)
    data = await state.get_data()


async def get_readact(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(name=call.data)
    await bot.send_message(call.from_user.id, 'Выберете действие', reply_markup=redact_markup)
    await state.set_state(FSMoput.varik)

async def get_next(call: types.callback_query, state: FSMContext):
    if call.data == 'output_1':
        data = await state.get_data()
        text = """Доступные остатки на складе\n"""
        x = data_racks_shelf(data['shelf'], data['shelves'])
        for i in x:
            text += f'Наименование: {i["category"]}, количество на складе : {i["quantity"]} шт \n'
        print(text)
        await bot.send_message(call.from_user.id, text)
        await bot.send_message(call.from_user.id, 'Введите кол-во')
        await state.set_state(FSMoput.pices)
    elif call.data == 'edit':
        await bot.send_message(call.from_user.id, 'К какому заказу нужно добавить данный материал?')
        await state.set_state(FSMoput.zakaz)


async def get_zakaz(mess: types.Message, state: FSMContext):
    await state.update_data(zakaz=mess.text)
    data = await state.get_data()
    id = search_id(data['shelf'], data['shelves'], data['name'])
    add_order(data['zakaz'])
    conn.commit()
    data_order_number(data['zakaz'], id)
    conn.commit()
    await bot.send_message(mess.chat.id, 'Номер заказа успешно прикреплен', reply_markup=main_markup)
    await state.clear()


async def get_pices(mess: types.Message, state:FSMContext):
    await state.update_data(pices=mess.text)
    data = await state.get_data()
    await bot.send_message(mess.chat.id, f'вы точно хотите забрать {data["name"]} х {data["pices"]} шт ', reply_markup=output_markup)
    await state.set_state(FSMoput.ready_out)

async def get_output(call: types.CallbackQuery, state:FSMContext):
    if call.data == 'output':
        data = await state.get_data()
        subtract_the_amount_without_order_number(data['pices'], data['shelf'], data['shelves'], data['name'])
        conn.commit()
        await bot.send_message(call.from_user.id, f'Вы забрали со склада: {data["name"]} х {data["pices"]} шт', reply_markup=main_markup)
        await state.clear()



async def search_menu(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, "Как искать заказ?", reply_markup=search_menu_markup)

class FSMsearch_1(StatesGroup):
    step_1 = State()
    step_2 = State()

async def numb_order(call: types.CallbackQuery, state:FSMContext):
    await bot.send_message(call.from_user.id, 'введеите номер заказа')
    await state.set_state(FSMsearch_1.step_1)

async def numb_order_1(mess: types.Message, state: FSMContext):
    await state.update_data(step_1=mess.text)
    data = await state.get_data()
    result = partial_search_by_order_number(data['step_1'])
    print(result)
    if result == []:
        await bot.send_message(mess.chat.id, "По вашему запросу ничего не найдено", reply_markup=main_markup)
        await state.clear()
    else:
        for list_1 in result:
            x = f"""<{list_1['category']}> х {list_1['quantity']}шт расположение: Стелаж {list_1['rack']} полка {list_1['shelf']}, заказ: {list_1["order_id"]}"""
            await bot.send_message(mess.chat.id, x)
        await bot.send_message(mess.chat.id, "Вы вернулись в главное меню", reply_markup=main_markup)
        await state.clear()


class FSMsearch_2(StatesGroup):
    step_3 = State()
    step_4 = State()

async def rack_shelf(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, "Введите номер стелажа")
    await state.set_state(FSMsearch_2.step_3)

async def rack_shelf_2(mess: types.Message, state: FSMContext):
    await state.update_data(step_3=mess.text)
    await bot.send_message(mess.chat.id, "Введите номер полки")
    await state.set_state(FSMsearch_2.step_4)

async def rack_shelf_3(mess:types.Message, state:FSMContext):
    await state.update_data(step_4=mess.text)
    data = await state.get_data()
    result = data_racks_shelf(data['step_3'], data['step_4'])
    if result == []:
        await bot.send_message(mess.chat.id, "По вашему запросу ничего не найдено", reply_markup=main_markup)
        await state.clear()
    else:
        for list_1 in result:
            x = f"Наименование <{list_1['category']}> x {list_1['quantity']} шт"
            await bot.send_message(mess.chat.id, x, reply_markup=main_markup)
        await state.clear()

class FSMcat(StatesGroup):
    cat_1 = State()

async def cat_search(call: types.CallbackQuery, state:FSMContext):
    await bot.send_message(call.from_user.id, 'Введите наименование товара для поиска')
    await state.set_state(FSMcat.cat_1)

async def cat2_search(mess: types.Message, state:FSMContext):
    await state.update_data(cat_1=mess.text)
    data = await state.get_data()
    x = partial_search_by_category(data['cat_1'])
    if x == []:
        await bot.send_message(mess.chat.id, "По вашему запросу ничего не найдено", reply_markup=main_markup)
        await state.clear()
    else:
        for list_1 in x:
            text = f'наименование: <{list_1["category"]}> кол-во: {list_1["quantity"]} Стелаж: {list_1["rack"]}, полка {list_1["shelf"]}, заказ: {list_1["order_id"]}'
            await bot.send_message(mess.chat.id, text)
    print(x)
    await bot.send_message(mess.chat.id, "Вы вернулись в главное меню", reply_markup=main_markup)
    await state.clear()


async def upload_csv(call: types.CallbackQuery):
    all_data_csv()
    await bot.send_document(call.from_user.id, FSInputFile('data_warehouse.csv'))
    await bot.send_message(call.from_user.id, "База упешно отправлена", reply_markup=main_markup)

async def canc(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, "Вы вернулись в главное меню", reply_markup=main_markup)


def register_handlers(dp: Dispatcher):
    """***************ADMIN**************"""
    dp.callback_query.register(canc, F.data == 'canc')
    dp.callback_query.register(upload_csv, F.data == 'csv')
    dp.message.register(cmd_admin, F.text == "3234hdsfdkf")
    """******************ПОСМОТРЕТЬ ГДЕ ЛЕЖИТ************************"""
    dp.message.register(cat2_search, FSMcat.cat_1)
    dp.callback_query.register(cat_search, F.data == 'searchname')
    dp.message.register(rack_shelf_3, FSMsearch_2.step_4)
    dp.message.register(rack_shelf_2, FSMsearch_2.step_3)
    dp.callback_query.register(rack_shelf, F.data == 'searchrack')
    dp.callback_query.register(numb_order, F.data == 'searchorder')
    dp.message.register(numb_order_1, FSMsearch_1.step_1)

    """*******************ЗАБРАТЬ СО СКЛАДА*********************"""
    dp.callback_query.register(search_menu, F.data == 'search')
    dp.callback_query.register(get_output, FSMoput.ready_out)
    dp.message.register(get_pices, FSMoput.pices)
    dp.message.register(get_zakaz, FSMoput.zakaz)
    dp.callback_query.register(get_next, FSMoput.varik)
    dp.callback_query.register(get_readact, FSMoput.redakt)
    dp.callback_query.register(ready_output, FSMoput.name)
    dp.callback_query.register(outuput_state_shelves, FSMoput.shelf)
    dp.callback_query.register(output_s, F.data == 'output_w')

    """*********************COMMANDS*************************"""
    dp.message.register(cmd_start, Command('start'))
    """*************************ПОЛОЖИТЬ НА СКЛАД******************************"""
    dp.callback_query.register(inpute_base, FSMput.ready_s)
    dp.callback_query.register(input_base_not_order, FSMput.ready_w)
    dp.callback_query.register(input_warhouse, F.data == 'input_w')
    dp.message.register(final_with_order, FSMput.namb_of_zakaz)
    dp.message.register(input_name, FSMput.name)
    dp.message.register(input_shelves, FSMput.sheif)
    dp.message.register(input_pices, FSMput.shelves)
    dp.message.register(input_zakaz, FSMput.pices)
    dp.callback_query.register(input_ready_z, FSMput.ready_z)
    dp.callback_query.register(input_final_cancel, F.data == 'cancel')





