from secure.main import *
import secure.get.photo, secure.get.video, secure.get.document, secure.get.voice, secure.get.audio, secure.get.video_note


@dp.message_handler(text="📤 Get")
async def handler(message: types.Message, state: FSMContext):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(message.chat.id, 'Choose for get:', reply_markup=Buttons.get(message.chat.id))
