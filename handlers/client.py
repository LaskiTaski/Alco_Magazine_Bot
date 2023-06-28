from button.client_kb import *
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMClient(StatesGroup):
    decoration = State()
    end = State()


# @dp.callback_query_handler(text='decor', state='*')
async def cb_price(callback: types.CallbackQuery, state: FSMContext):
    pass
