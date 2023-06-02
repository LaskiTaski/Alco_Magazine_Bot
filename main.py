from aiogram.utils import executor
from create_bot import dp
from database import sql_db_other, sql_db_client
from excel_table import load_et
from handlers import other

other.register_handlers_other(dp)

if __name__ == '__main__':
    print('Работаем!')
    sql_db_other.sql_start()
    sql_db_client.sql_start_client()
    load_et.read_file()
    executor.start_polling(dp, skip_updates=True)
