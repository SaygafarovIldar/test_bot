from aiogram.dispatcher.filters import Text

from imports import *
import secure.main
import secure.get.main_get
import profile

logging.basicConfig(level=logging.INFO)


# /start
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if not db.check_(table="users", table_name='user_id', value=user_id):
        db.add_user_id(user_id)
    elif not db.check_user_session(user_id):
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.send_message(chat_id, 'Hello choose one of them', reply_markup=Buttons.log(chat_id))
    else:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.send_message(chat_id, 'You are in main menu', reply_markup=Buttons.main_menu(message.chat.id))


@dp.message_handler(text="Log out")
async def handler(message: types.Message, state: FSMContext):
    db.set_account_id(user_id=message.from_user.id, account_id='')
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(message.chat.id, 'Successfully ☑', reply_markup=types.ReplyKeyboardRemove())
    await bot.delete_message(message.chat.id, message.message_id - 1)


@dp.message_handler(state='*', text="📄 Menu")
async def handler(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'You are in main menu', reply_markup=Buttons.main_menu(message.chat.id))
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@dp.callback_query_handler(lambda c: c.data == 'get_settings')
async def query(callback: types.CallbackQuery):
    await callback.answer(text='Coming soon')
#     acc_id = db.get(table_name="users", field="user_id", value=callback.from_user.id)[2]
#     # var = db.get_settings(account_id=acc_id)[0]
#     var = db.get(table_name="get_settings", field="account_id", value=acc_id)[0]
#
#     if callback.data == 'settings':
#         await bot.edit_message_text('⚙ Settings', callback.from_user.id, callback.message.message_id,
#                                     reply_markup=Buttons.settings(comment=f'commend {var[4]}',
#                                                                   hashtag=f'hashtag {var[5]}', date=f'date {var[6]}',
#                                                                   category=f'category {var[3]}',
#                                                                   self=callback.message.chat.id))
#     if callback.data == 'get_category':
#         lp = ''
#         if var[3] == '✔':
#             db.update_get_settings_category(account_id=acc_id, category='✖')
#             lp += 'False'
#             print(var[3], 'False')
#         else:
#             db.update_get_settings_category(account_id=acc_id, category='✔')
#             print(var[3], 'True')
#             lp += 'True'
#         await bot.edit_message_text(f'⚙ Settings: Category {lp}', callback.from_user.id, callback.message.message_id,
#                                     reply_markup=Buttons.settings(comment=f'commend {var[4]}',
#                                                                   hashtag=f'hashtag {var[5]}', date=f'date {var[6]}',
#                                                                   category=f'category {var[3]}',
#                                                                   self=callback.message.chat.id))
#     if callback.data == 'get_comment':
#         if var[4] == '✔':
#             await callback.answer(text='set ✔')
#             db.update_get_settings_comment(account_id=acc_id, comment='✔')
#             print(var[4], 'False')
#         else:
#             await callback.answer(text='set ✖')
#             db.update_get_settings_comment(account_id=acc_id, comment='✖')
#             print(var[4], 'True')
#     if callback.data == 'get_update':
#         await bot.edit_message_text(
#             f'⚙ Settings:\nComment: {var[4]}\nHashtag: {var[5]}\ndate: {var[6]}\ncategory: {var[3]}',
#             callback.from_user.id, callback.message.message_id, reply_markup=Buttons.settings(comment='commend',
#                                                                                               hashtag='hashtag',
#                                                                                               date='date',
#                                                                                               category='category',
#                                                                                               self=callback.message.chat.id))
#     else:
#         pass


# @dp.callback_query_handler()
# async def query(callback: types.CallbackQuery):

#     await bot.edit_message_text('Change your settings', callback.from_user.id, callback.message.message_id,
#                                 reply_markup=Buttons.settings(callback.message.chat.id, comment='comment'))


@dp.callback_query_handler(lambda c: c.data == 'remove')
async def remove(callback: types.CallbackQuery):
    await callback.answer(text='removed')
    await bot.delete_message(callback.from_user.id, callback.message.message_id)


@dp.message_handler()
async def end(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if not db.check_user_session(user_id):
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.send_message(chat_id, 'You need to log in to your account', reply_markup=Buttons.log(chat_id))
    else:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.send_message(chat_id, 'You are in main menu', reply_markup=Buttons.main_menu(message.chat.id))


if __name__ == '__main__':
    print('[INFO] ЗАПУЩЕН БОТ')
    executor.start_polling(dp, skip_updates=True)
