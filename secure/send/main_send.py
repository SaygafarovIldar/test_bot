from secure.main import *
import secure.send.photo, secure.send.video, secure.send.document, secure.send.voice, secure.send.audio, secure.send.videoNote


@dp.message_handler(text="📥 Send")
async def handler(message: types.Message, state: FSMContext):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(message.chat.id, 'Choose for send:', reply_markup=Buttons.send(message.chat.id))
