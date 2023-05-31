from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from button import other_kb



# @dp.message_handler( commands=['start'], state = '*' )
async def cmd_start( message : types.Message, state : FSMContext ):
    start_kb= types.InlineKeyboardMarkup(row_width=2)
    start_kb.add(*other_kb.gen_chapter())
    await message.answer(f'[Виды алкоголя](https://telegra.ph/Kakoj-vyberesh-ty-05-31)',
                         reply_markup=start_kb)


# @dp.callback_query_handler( text='start', state = '*' )
async def cb_menu(callback: types.CallbackQuery):
    start_kb= types.InlineKeyboardMarkup(row_width=2)
    start_kb.add(*other_kb.gen_chapter())
    await callback.message.edit_text(f'[Виды алкоголя](https://telegra.ph/Kakoj-vyberesh-ty-05-31)',
                                     reply_markup=start_kb)


def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'], state='*')
    dp.register_callback_query_handler(cb_menu, text='start', state='*')