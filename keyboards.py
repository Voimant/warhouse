from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from warehouse_db.main_db import data_category, list_rack, list_shelf, data_from_shelf

main_menu = [
    [
        InlineKeyboardButton(text='Внести на склад', callback_data='input_w'),
        InlineKeyboardButton(text='Забрать со склада', callback_data='output_w')
    ],
    [
        InlineKeyboardButton(text='Посмотреть где лежит', callback_data='search')
    ]
]
input_sclad_button = [[
    InlineKeyboardButton(text="ВНЕСТИ НА СКЛАД", callback_data='input'),
    InlineKeyboardButton(text="ОТМЕНА", callback_data='cancel')
]]

output_sclad_button = [[
    InlineKeyboardButton(text='ЗАБРАТЬ МАТЕРИАЛЫ', callback_data='output'),
    InlineKeyboardButton(text='ОТМЕНА', callback_data='cancel')
]]

order_not_order_button = [[
    InlineKeyboardButton(text='Добавить к заказу?', callback_data='with_order'),
    InlineKeyboardButton(text='Внести без заказа', callback_data='not_order')
]]
cancel_button = [[
    InlineKeyboardButton(text='ОТМЕНА', callback_data='cancel')
]]

redact_button = [[
    InlineKeyboardButton(text='Редактировать', callback_data='edit'),
    InlineKeyboardButton(text='Забрать', callback_data='output_1')
]]


search_menu_button = [
    [InlineKeyboardButton(text='По номеру заказа', callback_data='searchorder')],
    [InlineKeyboardButton(text='по номеру стелажа и полки', callback_data='searchrack')],
    [InlineKeyboardButton(text="По наименованию", callback_data='searchname')]
]

admin_button = [[
    InlineKeyboardButton(text='Скачать базу CSV', callback_data='csv'),
    InlineKeyboardButton(text='Отмена',callback_data='canc')
]]
admin_markup = InlineKeyboardMarkup(inline_keyboard=admin_button)


search_menu_markup = InlineKeyboardMarkup(inline_keyboard=search_menu_button)

redact_markup = InlineKeyboardMarkup(inline_keyboard=redact_button)
cancel_markup = InlineKeyboardMarkup(inline_keyboard=cancel_button)
order_not_markup = InlineKeyboardMarkup(inline_keyboard=order_not_order_button)
output_markup = InlineKeyboardMarkup(inline_keyboard=output_sclad_button)
input_markup = InlineKeyboardMarkup(inline_keyboard=input_sclad_button)
main_markup = InlineKeyboardMarkup(inline_keyboard=main_menu)



def gen_markup():
    my_db = data_category()
    button = []
    for out in my_db:
        x = InlineKeyboardButton(text=out, callback_data=out)
        y = [x]
        button.append(y)
    markup = InlineKeyboardMarkup(inline_keyboard=button)
    return markup


def gen_shelf_markup():
    rack = list_rack()
    button = []
    for out in rack:
        x = InlineKeyboardButton(text=out, callback_data=out)
        y = [x]
        if y in button:
            pass
        else:
            button.append(y)
    markup = InlineKeyboardMarkup(inline_keyboard=button)
    return markup


def gen_shelves_markup(rack):
    shelves = list_shelf(rack)
    button = []
    for out in shelves:
        x = InlineKeyboardButton(text=str(out), callback_data=str(out))
        y = [x]
        if y in button:
            pass
        else:
            button.append(y)
    markup = InlineKeyboardMarkup(inline_keyboard=button)
    return markup


def position_button(rack, shelf):
    list_name = data_from_shelf(str(rack), int(shelf))
    button = []
    for out in list_name:
        x = InlineKeyboardButton(text=str(out), callback_data=str(out))
        y = [x]
        button.append(y)
    markup = InlineKeyboardMarkup(inline_keyboard=button)
    return markup




# print(gen_markup())

