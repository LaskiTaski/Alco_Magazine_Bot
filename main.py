from aiogram.utils import executor
from create_bot import dp
from database import sql_db_other, sql_db_client, sql_db_gen
from excel_table import load_table
from handlers import other

other.register_handlers_other(dp)

if __name__ == '__main__':
    print('Считывание таблицы...')
    sql_db_gen.create()  # БД Товаров
    sql_db_client.create()  # БД Пользователя
    load_table.read_file()
    executor.start_polling(dp, skip_updates=True)
