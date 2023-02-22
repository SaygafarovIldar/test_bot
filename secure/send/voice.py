from secure.main import *


@dp.callback_query_handler(lambda c: c.data == 'send_voice')
async def query(callback: types.CallbackQuery):
    await callback.answer(text='voice')
    await bot.edit_message_text('I wait voice', callback.from_user.id, callback.message.message_id)
    await Voice.voice.set()


@dp.message_handler(state=Voice.voice, content_types=["voice"])
async def check_password(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    file_id = message.voice.file_id
    file_size = message.voice.file_size
    async with state.proxy() as voice:
        voice['voice_id'] = file_id
        voice['voice_size'] = file_size
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    await bot.send_message(chat_id, 'I get your voice. Now add category', reply_markup=Buttons.pass_button(chat_id))
    await Voice.category.set()


@dp.message_handler(state=Voice.category)
async def voice_cat(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    text = message.text
    async with state.proxy() as voice:
        voice['voice_category'] = text
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    finish_button = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=1)
    finish_button.add('Continue', 'Finish')
    await bot.send_message(chat_id, 'Continue or Finish it', reply_markup=finish_button)
    await Audio.finish_continue.set()


@dp.message_handler(state=Voice.finish_continue)
async def voice_finish_continue(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    if message.text == 'Continue':
        await bot.send_message(chat_id, 'Set comment to your file', reply_markup=Buttons.pass_button(chat_id))
        await Voice.comment.set()
    elif message.text == 'Finish':
        acc_id = db.get(table_name="users", field="user_id", value=message.from_user.id)[2]
        async with state.proxy() as voice:
            db.add_(table_name='users_voice',
                    field='voice_id',
                    date=datetime.date.today(),
                    user=acc_id,
                    name_id=voice['voice_id'],
                    category=voice['voice_category'],
                    hashtag='',
                    comment='',
                    size=voice['voice_size']
                    )
        await state.finish()
        await bot.send_message(chat_id, 'You are in menu', reply_markup=Buttons.secure(chat_id))


@dp.message_handler(state=Voice.comment)
async def check_password(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    text = message.text
    async with state.proxy() as voice:
        voice['voice_comment'] = text
    await bot.send_message(chat_id, 'Set hashtag to your file', reply_markup=Buttons.pass_button(chat_id))
    await Audio.hashtag.set()


@dp.message_handler(state=Voice.hashtag)
async def check_password(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    acc_id = db.get(table_name="users", field="user_id", value=message.from_user.id)[2]
    print(acc_id)
    text = message.text
    async with state.proxy() as voice:
        db.add_(table_name='users_voice',
                field='voice_id',
                date=datetime.date.today(),
                user=acc_id,
                name_id=voice['voice_id'],
                category=voice['voice_category'],
                hashtag=text,
                comment=voice['voice_comment'],
                size=voice['voice_size']
                )
    await state.finish()
    await bot.send_message(chat_id, 'You are in menu', reply_markup=Buttons.secure(chat_id))
