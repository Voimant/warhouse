from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from warehouse_db.main_db import data_category

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


print(gen_markup())

