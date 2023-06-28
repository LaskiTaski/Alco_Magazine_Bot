from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from button.other_kb import *
from database import sql_db_other


class FSMAdmin(StatesGroup):
    start = State()


# @dp.message_handler( commands=['start'], state = '*' )
async def cmd_start(message: types.Message, state: FSMContext):
    """Показ всех ВИДОВ алкоголя"""

    async with state.proxy() as data: # Данных в FSM
        data['user'] = f'tg://user?id={message.from_user.id}' # Сохраняем ID пользователя

    start_kb = types.InlineKeyboardMarkup(row_width=2)
    start_kb.add(*gen_chapter()) # Генерируем Разделы

    await FSMAdmin.start.set()
    await message.answer(f'[Какой бывает алкоголь](https://telegra.ph/Kakoj-vyberesh-ty-05-31)',
                         reply_markup=start_kb)


# @dp.callback_query_handler( text='start', state = '*' )
async def cb_menu(callback: types.CallbackQuery):
    """Показ всех ВИДОВ алкоголя"""

    start_kb = types.InlineKeyboardMarkup(row_width=2)
    start_kb.add(*gen_chapter()) #Генерируем Разделы

    await callback.message.edit_text(f'[Какой бывает алкоголь](https://telegra.ph/Kakoj-vyberesh-ty-05-31)',
                                     reply_markup=start_kb)


# @dp.callback_query_handler( lambda x: x.data in [i[0] for i in sql_db_other.sql_gen_chapter()], state = '*' )
async def cb_alcohol(callback: types.CallbackQuery, state: FSMContext):
    """Показ всех МАРОК алкоголя"""
    global chapter

    async with state.proxy() as data:
        data['chapter'] = callback.data # Сохраняем предыдущий запрос раздела

    user_data = await state.get_data()
    chapter = user_data['chapter'] # Вызываем запрос раздела из FSM

    start_kb = types.InlineKeyboardMarkup(row_width=2)
    start_kb.add(*gen_names(chapter)) # Генерируем марки алкоголя
    start_kb.row(allmenu)# Отдельной строкой добавляем кнопки "ГЛАВНОЕ МЕНЮ"

    await callback.message.edit_text(f'[Виды алкоголя](https://telegra.ph/Kakoj-vyberesh-ty-05-31)',
                                     reply_markup=start_kb)


# @dp.callback_query_handler( lambda x: x.data in [i[0] for i in sql_db_other.sql_gen_chapter()], state = '*' )
async def cb_trademark(callback: types.CallbackQuery, state: FSMContext):
    """Показ всей ИНФОРМАЦИИ  об алкоголе"""

    async with state.proxy() as data:
        data['product'] = callback.data # Сохраняем имя продукта
        data['quantity'] = 0 # Создаём для каждого пользователя счётчик конкретного алкоголя

    user_data = await state.get_data()
    product = user_data['product'] # Вытаскиваем имя товара
    chapter = user_data['chapter'] # Вытаскиваем имя раздела
    user = user_data['user'] # Вытаскиваем имя пользователя
    quanti = user_data['quantity'] # Вытаскиваем кол-во

    all_info = sql_db_other.sql_gen_info(product) #Вся информация о товаре
    price = all_info[0] # Цена
    url_telegraph = all_info[1] # Ссылка на описание товара
    in_stock = all_info[2] # Информация о кол-ве товара на складе
    all_price = quanti*price # Расчёт стоимости

    product_information = [user, product, quanti, price, all_price]
    await sql_db_client.sql_add_client(product_information)

    start_kb = types.InlineKeyboardMarkup(row_width=3)
    quantity = InlineKeyboardButton(str(sql_db_client.sql_read_client(product)[0]), callback_data='None')
    back = InlineKeyboardButton('Назад◀', callback_data=chapter)

    start_kb.add(plus, quantity, minus)
    start_kb.row(back, allmenu)

    print(quanti)
    print(sql_db_client.sql_read_client(product))
    await callback.message.edit_text(f'[{product}]({url_telegraph})\n'
                                     f'Цена: {price}руб.\n'
                                     f'Всего на складе: {in_stock}шт.',
                                     reply_markup=start_kb)

# @dp.callback_query_handler( text='plus', state = '*' )
async def cb_plus(callback: types.CallbackQuery, state: FSMContext):
    """Добавить алкого"""

    async with state.proxy() as data:
        data['quantity'] += 1 # Добавляем в кол-во 1


    user_data = await state.get_data()
    product = user_data['product']  # Вытаскиваем имя товара
    quanti = user_data['quantity'] # Вытаскиваем кол-во по конкретному товару

    sql_db_other.sql_plus(product)

    all_info = sql_db_other.sql_gen_info(product)  # Вся информация о товаре
    price = all_info[0]
    url_telegraph = all_info[1]
    in_stock = all_info[2]
    all_price = quanti * price

    await sql_db_client.sql_update_client('Количество', quanti, product)
    await sql_db_client.sql_update_client('Общая', all_price, product)

    start_kb = types.InlineKeyboardMarkup(row_width=3)
    print(sql_db_client.sql_read_client(product))
    quantity = InlineKeyboardButton(str(sql_db_client.sql_read_client(product)[0]), callback_data='None')
    back = InlineKeyboardButton('Назад◀', callback_data=chapter)

    start_kb.add(plus, quantity, minus)
    start_kb.row(back, allmenu)

    await callback.message.edit_text(f'[{product}]({url_telegraph})\n'
                                     f'Цена: {price}руб.\n'
                                     f'Всего на складе: {in_stock}шт.'
                                     f'В вашей корзине: '
                                     f'Хотите добавить: {quanti}',
                                     reply_markup=start_kb)


# @dp.callback_query_handler( text='minus', state = '*' )
async def cb_minus(callback: types.CallbackQuery, state: FSMContext):
    """Добавить алкоголь"""

    async with state.proxy() as data:
        if data['quantity'] > 0:
            data['quantity'] -= 1

    user_data = await state.get_data()
    product = user_data['product']  # Вытаскиваем имя товара
    quanti = user_data['quantity'] # Вытаскиваем кол-во товара

    all_info = sql_db_other.sql_gen_info(product)  # Вся информация о товаре
    price = all_info[0]
    url_telegraph = all_info[1]
    in_stock = all_info[2]
    all_price = quanti * price

    await sql_db_client.sql_update_client('Количество', quanti, product)
    await sql_db_client.sql_update_client('Общая', all_price, product)

    start_kb = types.InlineKeyboardMarkup(row_width=3)
    print(sql_db_client.sql_read_client(product))
    quantity = InlineKeyboardButton(str(sql_db_client.sql_read_client(product)[0]), callback_data='None')
    back = InlineKeyboardButton('Назад◀', callback_data=chapter)

    start_kb.add(plus, quantity, minus)
    start_kb.row(back, allmenu)

    await callback.message.edit_text(f'[{product}]({url_telegraph})\n'
                                     f'Цена: {price}руб.\n'
                                     f'Всего на складе: {in_stock}шт.'
                                     f'В вашей корзине: '
                                     f'Хотите добавить: {quanti}',
                                     reply_markup=start_kb)


# @dp.callback_query_handler( text='drop_check', state = '*' )
async def cb_check(callback: types.CallbackQuery, state: FSMContext):
    """Выдать чек"""
    # 1846023358
    async with state.proxy() as data:
        data['chapter'] = callback.data # Сохраняем предыдущий запрос раздела

    user_data = await state.get_data()
    chapter = user_data['chapter'] # Вызываем запрос раздела из FSM

    start_kb = types.InlineKeyboardMarkup(row_width=2)
    start_kb.add(*gen_names(chapter)) # Генерируем марки алкоголя
    start_kb.row(allmenu)# Отдельной строкой добавляем кнопки "ГЛАВНОЕ МЕНЮ"

    await callback.message.edit_text(f'[Виды алкоголя](https://telegra.ph/Kakoj-vyberesh-ty-05-31)',
                                     reply_markup=start_kb)



def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'], state='*')
    dp.register_callback_query_handler(cb_menu, text='start', state='*')
    dp.register_callback_query_handler(cb_alcohol, lambda x: x.data in [i[0] for i in sql_db_other.sql_gen_chapter()],
                                       state='*')
    dp.register_callback_query_handler(cb_trademark, lambda x: x.data in [i[0] for i in sql_db_other.sql_gen_name(chapter)],
                                       state='*')
    dp.register_callback_query_handler(cb_plus, text='plus', state = '*')
    dp.register_callback_query_handler(cb_minus, text='minus', state='*')