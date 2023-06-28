from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from button.other_kb import *
from database import sql_db_gen, sql_db_client


class FSMAdmin(StatesGroup):
    start = State()


# @dp.message_handler( commands=['start'], state = '*' )
async def cmd_start(message: types.Message, state: FSMContext):
    """
    Показ всех ВИДОВ алкоголя.
    :param message: Сообщение /start от пользователя.
    :param state: Состояние - любое.
    """

    async with state.proxy() as data:  # Все данные FSM
        data['user'] = message.from_user.id  # Сохраняем ID пользователя
    start_kb = types.InlineKeyboardMarkup(row_width=2)
    start_kb.add(*gen_chapter())  # Генерируем Разделы

    await FSMAdmin.start.set()
    await message.answer(f'[Какой бывает алкоголь](https://telegra.ph/Kakoj-vyberesh-ty-05-31)',
                         reply_markup=start_kb)


# @dp.callback_query_handler( text='start', state = '*' )
async def cb_menu(callback: types.CallbackQuery):
    """
    Показ всех Разделов алкоголя.
    :param callback: Нажатие на кнопку Главное меню.
    """

    start_kb = types.InlineKeyboardMarkup(row_width=2)
    start_kb.add(*gen_chapter())  # Генерируем Разделы
    start_kb.row(check, buy)

    await callback.message.edit_text(f'[Какой бывает алкоголь](https://telegra.ph/Kakoj-vyberesh-ty-05-31)',
                                     reply_markup=start_kb)


# @dp.callback_query_handler( lambda x: x.data in [i[0] for i in sql_db_other.sql_gen_chapter()], state = '*' )
async def cb_alcohol(callback: types.CallbackQuery, state: FSMContext):
    """
    Показ всех МАРОК алкоголя.
    :param callback: Нажатие на кнопку одногого из Раделов.
    :param state: Состояние - любое.
    """

    global chapter

    async with state.proxy() as data:
        data['chapter'] = callback.data  # Сохраняем предыдущий запрос раздела

    data = await state.get_data()
    chapter = data['chapter']  # Вызываем запрос раздела из FSM

    start_kb = types.InlineKeyboardMarkup(row_width=2)
    start_kb.add(*gen_names(chapter))  # Генерируем марки алкоголя
    start_kb.row(check, buy)
    start_kb.row(allmenu)  # Отдельной строкой добавляем кнопки "ГЛАВНОЕ МЕНЮ"

    await callback.message.edit_text(f'[Виды алкоголя](https://telegra.ph/Kakoj-vyberesh-ty-05-31)',
                                     reply_markup=start_kb)


# @dp.callback_query_handler( lambda x: x.data in [i[0] for i in sql_db_other.sql_gen_chapter()], state = '*' )
async def cb_trademark(callback: types.CallbackQuery, state: FSMContext):
    """
    Показ всей ИНФОРМАЦИИ  об алкоголе.
    :param callback: Нажатие на кнопку Алкоголя.
    :param state: Состояние - любое.
    """

    async with state.proxy() as data:
        data['product'] = callback.data  # Сохраняем имя продукта
        data['quantity'] = 0  # Создаём для каждого пользователя счётчик конкретного алкоголя

    data = await state.get_data()
    product = data['product']  # Вытаскиваем имя товара
    chapter = data['chapter']  # Вытаскиваем имя раздела
    user = data['user']  # Вытаскиваем имя пользователя
    quanti = data['quantity']  # Вытаскиваем кол-во

    all_info = sql_db_gen.info(product)  # Вся информация о товаре
    price = all_info[0]  # Цена
    url_telegraph = all_info[1]  # Ссылка на описание товара
    in_stock = all_info[2]  # Информация о кол-ве товара на складе
    all_price = quanti * price  # Расчёт стоимости

    product_information = [user, product, quanti, price, all_price]
    await sql_db_client.add(product_information)

    start_kb = types.InlineKeyboardMarkup(row_width=3)
    quantity = InlineKeyboardButton(str(sql_db_client.read(product)[0]), callback_data='None')
    back = InlineKeyboardButton('Назад◀', callback_data=chapter)

    start_kb.add(plus, quantity, minus)
    start_kb.row(check, buy)
    start_kb.row(back, allmenu)

    await callback.message.edit_text(f'[{product}]({url_telegraph})\n'
                                     f'Цена: {price}руб.\n'
                                     f'Всего на складе: {in_stock}шт.',
                                     reply_markup=start_kb)


# @dp.callback_query_handler( text='plus', state = '*' )
async def cb_plus(callback: types.CallbackQuery, state: FSMContext):
    """
    Добавать +1 товар в корзину.
    :param callback:  Нажатие на кнопку +.
    :param state: Состояние - любое.
    """

    data = await state.get_data()
    product = data['product']  # Вытаскиваем имя товара

    async with state.proxy() as data:
        try:
            if sql_db_other.read(product)[0] != 0:
                sql_db_other.plus(product)
                data['quantity'] += 1  # Добавляем в кол-во 1
                print(f"{data['quantity']},Добавлено")
        except:
            await callback.answer(text='На складе данного товара больше нет.', show_alert=True)
            print(f"PLUS ERROR------> OTHER HANDLER -----------------------> OTHER HANDLER")

    quanti = data['quantity']  # Вытаскиваем кол-во по конкретному товару

    all_info = sql_db_gen.info(product)  # Вся информация о товаре
    price = all_info[0]
    url_telegraph = all_info[1]
    in_stock = all_info[2]
    all_price = quanti * price

    await sql_db_client.updata('Количество', quanti, product)
    await sql_db_client.updata('Общая', all_price, product)

    start_kb = types.InlineKeyboardMarkup(row_width=3)
    quantity = InlineKeyboardButton(str(sql_db_client.read(product)[0]), callback_data='None')
    back = InlineKeyboardButton('Назад◀', callback_data=chapter)

    start_kb.add(plus, quantity, minus)
    start_kb.row(check, buy)
    start_kb.row(back, allmenu)

    await callback.message.edit_text(f'[{product}]({url_telegraph})\n'
                                     f'Цена: {price}руб.\n'
                                     f'Всего на складе: {in_stock}шт.\n'
                                     f'В вашей корзине: ??\n'
                                     f'Хотите добавить: {quanti}',
                                     reply_markup=start_kb)


# @dp.callback_query_handler( text='minus', state = '*' )
async def cb_minus(callback: types.CallbackQuery, state: FSMContext):
    """
    Убрать -1 товар из корзины.
    :param callback:  Нажатие на кнопку -.
    :param state: Состояние - любое.
    """

    data = await state.get_data()
    product = data['product']  # Вытаскиваем имя товара

    async with state.proxy() as data:
        if data['quantity'] > 0:
            sql_db_other.minus(product)
            data['quantity'] -= 1
        else:
            await callback.answer(text='Убирать больше нечего.', show_alert=True)
            print(f"MINUS ERROR------> OTHER HANDLER -----------------------> OTHER HANDLER")

    quanti = data['quantity']  # Вытаскиваем кол-во товара

    all_info = sql_db_gen.info(product)  # Вся информация о товаре
    price = all_info[0]
    url_telegraph = all_info[1]
    in_stock = all_info[2]
    all_price = quanti * price

    await sql_db_client.updata('Количество', quanti, product)
    await sql_db_client.updata('Общая', all_price, product)

    start_kb = types.InlineKeyboardMarkup(row_width=3)
    quantity = InlineKeyboardButton(str(sql_db_client.read(product)[0]), callback_data='None')
    back = InlineKeyboardButton('Назад◀', callback_data=chapter)

    start_kb.add(plus, quantity, minus)
    start_kb.add(check, buy)
    start_kb.row(back, allmenu)

    await callback.message.edit_text(f'[{product}]({url_telegraph})\n'
                                     f'Цена: {price}руб.\n'
                                     f'Всего на складе: {in_stock}шт.'
                                     f'В вашей корзине: ??'
                                     f'Хотите добавить: {quanti}',
                                     reply_markup=start_kb)


# @dp.callback_query_handler( text='drop_check', state = '*' )
async def cb_check(callback: types.CallbackQuery, state: FSMContext):
    """
    Выдать чек.
    :param callback:  Нажатие на кнопку Выдать чек.
    :param state: Состояние - любое.
    """

    async with state.proxy() as data:
        ID = data['user']

    start_kb = types.InlineKeyboardMarkup(row_width=1)
    back = InlineKeyboardButton('Назад◀', callback_data=chapter)
    start_kb.add(back, buy)
    await callback.message.edit_text(f'Ваш заказ:\n{sql_db_client.check(ID)}',
                                     reply_markup=start_kb)


def register_handlers_other(dp: Dispatcher):
    """
    Регистрирует наши хендлеры в отдельную ф-ию.
    :param dp: Dispatcher.
    """
    dp.register_message_handler(cmd_start, commands=['start'], state='*')
    dp.register_callback_query_handler(cb_menu, text='start', state='*')
    dp.register_callback_query_handler(cb_alcohol, lambda x: x.data in [i[0] for i in sql_db_gen.chapter()],
                                       state='*')
    dp.register_callback_query_handler(cb_trademark, lambda x: x.data in [i[0] for i in sql_db_gen.name(chapter)],
                                       state='*')
    dp.register_callback_query_handler(cb_plus, text='plus', state='*')
    dp.register_callback_query_handler(cb_minus, text='minus', state='*')
    dp.register_callback_query_handler(cb_check, text='drop_check', state='*')
