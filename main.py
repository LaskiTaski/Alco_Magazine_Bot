from aiogram.utils import executor
from create_bot import  dp
# from handlers import other,client, admin
# from data_base import sql_db_admin, sql_db_client
#
# admin.register_handlers_admin(dp)
# other.register_handlers_other(dp)
# client.register_handlers_client(dp)



if __name__ == '__main__':
    print('Работаем!')
    # sql_db_admin.sql_start_admin()
    # sql_db_client.sql_start_client()
    executor.start_polling(dp, skip_updates=True)
