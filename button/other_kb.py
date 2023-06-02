from database import sql_db_other, sql_db_client
from aiogram.types import InlineKeyboardButton


# Возвращает все виды алкоголя.
def gen_chapter():
    chapter_list = []
    for i in sql_db_other.sql_gen_chapter():
        chapter_list.append(button := InlineKeyboardButton(i[0], callback_data=i[0]))
    return chapter_list


# Возвращает все марки алкоголя.
def gen_names(state):
    names_list = []
    for i in sql_db_other.sql_gen_name(state):
        names_list.append(button := InlineKeyboardButton(i[0], callback_data=i[0]))
    return names_list

allmenu = InlineKeyboardButton('Главное меню🔙', callback_data='start')

plus = InlineKeyboardButton('+', callback_data='plus')
minus = InlineKeyboardButton('-', callback_data='minus')