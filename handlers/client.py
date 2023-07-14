# from aiogram import types, Dispatcher
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from button.other_kb import *
# from database import sql_db_gen, sql_db_client
#
#
#
# class FSMClient(StatesGroup):
#     decoration = State()
#     end = State()
#
#
# # @dp.callback_query_handler( text='plus', state = '*' )
# async def cb_plus(callback: types.CallbackQuery, state: FSMContext):
#     """
#     Добавать +1 товар в корзину.
#     :param callback:  Нажатие на кнопку +.
#     :param state: Состояние - любое.
#     """
#
#     data = await state.get_data()
#     product = data['product']  # Вытаскиваем имя товара
#     chapter = data['chapter']
#
#     async with state.proxy() as data:
#         if sql_db_other.read(product)[0] != 0:
#             sql_db_other.plus(product)
#             data['quantity'] += 1  # Добавляем в кол-во 1
#         else:
#             await callback.answer(text='На складе данного товара больше нет.', show_alert=True)
#             print(f"PLUS ERROR------> OTHER HANDLER -----------------------> OTHER HANDLER")
#
#     quanti = data['quantity']  # Вытаскиваем кол-во
#
#     all_info = sql_db_gen.info(product)  # Вся информация о товаре
#     price = all_info[0]
#     url_telegraph = all_info[1]
#     in_stock = all_info[2]
#     all_price = quanti * price
#
#     await sql_db_client.updata('Количество', quanti, product)
#     await sql_db_client.updata('Общая', all_price, product)
#
#     start_kb = types.InlineKeyboardMarkup(row_width=3)
#     quantity = InlineKeyboardButton(str(sql_db_client.read(product)[0]), callback_data='None')
#     back = InlineKeyboardButton('Назад◀', callback_data=chapter)
#
#     start_kb.add(plus, quantity, minus)
#     start_kb.row(check, buy)
#     start_kb.row(back, allmenu)
#
#     await callback.message.edit_text(f'[{product}]({url_telegraph})\n'
#                                      f'Цена: {price}руб.\n'
#                                      f'Всего на складе: {in_stock}шт.\n'
#                                      f'В вашей корзине: ??\n'
#                                      f'Хотите добавить: {quanti}',
#                                      reply_markup=start_kb)
#
# # @dp.callback_query_handler( text='minus', state = '*' )
# async def cb_minus(callback: types.CallbackQuery, state: FSMContext):
#     """
#     Убрать -1 товар из корзины.
#     :param callback:  Нажатие на кнопку -.
#     :param state: Состояние - любое.
#     """
#
#     data = await state.get_data()
#     product = data['product']  # Вытаскиваем имя товара
#     chapter = data['chapter']
#
#     async with state.proxy() as data:
#         if data['quantity'] > 0:
#             sql_db_other.minus(product)
#             data['quantity'] -= 1
#         else:
#             await callback.answer(text='Убирать больше нечего.', show_alert=True)
#             print(f"MINUS ERROR------> OTHER HANDLER -----------------------> OTHER HANDLER")
#
#     quanti = data['quantity']  # Вытаскиваем кол-во
#
#     all_info = sql_db_gen.info(product)  # Вся информация о товаре
#     price = all_info[0]
#     url_telegraph = all_info[1]
#     in_stock = all_info[2]
#     all_price = quanti * price
#
#     await sql_db_client.updata('Количество', quanti, product)
#     await sql_db_client.updata('Общая', all_price, product)
#
#     start_kb = types.InlineKeyboardMarkup(row_width=3)
#     quantity = InlineKeyboardButton(str(sql_db_client.read(product)[0]), callback_data='None')
#     back = InlineKeyboardButton('Назад◀', callback_data=chapter)
#
#     start_kb.add(plus, quantity, minus)
#     start_kb.add(check, buy)
#     start_kb.row(back, allmenu)
#
#     await callback.message.edit_text(f'[{product}]({url_telegraph})\n'
#                                      f'Цена: {price}руб.\n'
#                                      f'Всего на складе: {in_stock}шт.\n'
#                                      f'В вашей корзине: ??\n'
#                                      f'Хотите добавить: {quanti}',
#                                      reply_markup=start_kb)
#
# # @dp.callback_query_handler( text='drop_check', state = '*' )
# async def cb_check(callback: types.CallbackQuery, state: FSMContext):
#     """
#     Выдать чек.
#     :param callback:  Нажатие на кнопку Выдать чек.
#     :param state: Состояние - любое.
#     """
#
#     async with state.proxy() as data:
#         ID = data['user']
#         chapter = data['chapter']
#
#     start_kb = types.InlineKeyboardMarkup(row_width=1)
#     back = InlineKeyboardButton('Назад◀', callback_data=chapter)
#     start_kb.add(back, buy)
#     await callback.message.edit_text(f'Ваш заказ:\n{sql_db_client.check(ID)}',
#                                      reply_markup=start_kb)
#
# # @dp.callback_query_handler( text='buy', state = '*' )
# async def cb_buy(callback: types.CallbackQuery, state: FSMContext):
#     """
#     Выдать чек.
#     :param callback:  Нажатие на кнопку Оплатить.
#     :param state: Состояние - любое.
#     """
#
#     async with state.proxy() as data:
#         ID = data['user']
#         chapter = data['chapter']
#
#     start_kb = types.InlineKeyboardMarkup(row_width=1)
#     back = InlineKeyboardButton('Назад◀', callback_data=chapter)
#     start_kb.add(back)
#     await callback.message.edit_text(f'Ваш заказ:\n{sql_db_client.check(ID)}',
#                                      reply_markup=start_kb)
#
# def register_handlers_client(dp: Dispatcher):
#     dp.register_callback_query_handler(cb_plus, text='plus', state='*')
#     dp.register_callback_query_handler(cb_minus, text='minus', state='*')
#     dp.register_callback_query_handler(cb_check, text='drop_check', state='*')
#     dp.register_callback_query_handler(cb_buy, text='buy', state='*')
