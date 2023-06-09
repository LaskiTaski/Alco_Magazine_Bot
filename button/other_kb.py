from database import sql_db_other, sql_db_client, sql_db_gen
from aiogram.types import InlineKeyboardButton


# Возвращает все виды алкоголя.
def gen_chapter():  # Генерируем список кнопок
    chapter_list = []
    for i in sql_db_gen.chapter():
        chapter_list.append(button := InlineKeyboardButton(i[0], callback_data=i[0]))
    return chapter_list


# Возвращает все марки алкоголя.
def gen_names(state):
    names_list = []
    for i in sql_db_gen.name(state):
        names_list.append(button := InlineKeyboardButton(i[0], callback_data=i[0]))
    return names_list


allmenu = InlineKeyboardButton('Главное меню🔙', callback_data='start')

plus = InlineKeyboardButton('➕', callback_data='plus')
minus = InlineKeyboardButton('➖', callback_data='minus')
check = InlineKeyboardButton('Выдать чек🛒', callback_data='drop_check')
buy = InlineKeyboardButton('Оплатить покупку💳', callback_data='buy')
