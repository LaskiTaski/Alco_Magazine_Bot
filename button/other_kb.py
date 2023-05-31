from data_base import sql_db_other
from aiogram.types import InlineKeyboardButton


# Возвращает кнопки всех разделов в главное меню.
def gen_chapter():
    chapter_list = []
    for i in sql_db_other.sql_gen_chapter():
        chapter_list.append(button := InlineKeyboardButton(i[0], callback_data=i[0]))
    return chapter_list
