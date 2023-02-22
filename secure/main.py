from imports import *
import secure.send.main_send, secure.get.main_get


@dp.message_handler(text="Secure")
async def handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if not db.check_user_session(user_id):
        await bot.send_message(chat_id, 'Hello choose one of them', reply_markup=Buttons.log(chat_id))
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    else:
        await bot.send_message(chat_id, 'Choose one of them', reply_markup=Buttons.secure(message.chat.id))
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
