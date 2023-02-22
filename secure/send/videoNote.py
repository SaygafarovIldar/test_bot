from secure.main import *


@dp.callback_query_handler(lambda c: c.data == 'send_video_note')
async def query(callback: types.CallbackQuery):
    await callback.answer(text='video')
    await bot.edit_message_text('I wait Video', callback.from_user.id, callback.message.message_id)
    await VideoNote.videoNote.set()


@dp.message_handler(state=VideoNote.videoNote, content_types=["video_note"])
async def check_password(message: types.Message, state: FSMContext):
    print(message.video_note.file_id)
    chat_id = message.chat.id
    file_id = message.video_note.file_id
    file_size = message.video_note.file_size
    async with state.proxy() as video_note:
        video_note['VideoNote_id'] = file_id
        video_note['VideoNote_size'] = file_size
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    await bot.send_message(chat_id, 'I get video note. Now add category', reply_markup=Buttons.pass_button(chat_id))
    await VideoNote.category.set()


@dp.message_handler(state=VideoNote.category)
async def check_password(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    text = message.text
    async with state.proxy() as video_note:
        video_note['VideoNote_category'] = text
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    finish_button = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=1)
    finish_button.add('Continue', 'Finish')
    await bot.send_message(chat_id, 'Continue or Finish it', reply_markup=finish_button)
    await VideoNote.finish_continue.set()


@dp.message_handler(state=VideoNote.finish_continue)
async def continue_finish(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    if message.text == 'Continue':
        await bot.send_message(chat_id, 'Set comment to your file', reply_markup=Buttons.pass_button(chat_id))
        await Video.comment.set()
    elif message.text == 'Finish':
        print('kklsjgh')
        acc_id = db.get(table_name="users", field="user_id", value=message.from_user.id)[2]
        async with state.proxy() as video_note:
            db.add_(table_name='users_video_note',
                    field='video_note_id',
                    date=datetime.date.today(),
                    user=acc_id,
                    name_id=video_note['VideoNote_id'],
                    category=video_note['VideoNote_category'],
                    hashtag='',
                    comment='',
                    size=video_note['VideoNote_size']
                    )
        await state.finish()
        await bot.send_message(chat_id, 'You are in menu', reply_markup=Buttons.secure(chat_id))


@dp.message_handler(state=VideoNote.comment)
async def video_note_comment(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    text = message.text
    async with state.proxy() as video_note:
        video_note['VideoNote_comment'] = text
    await bot.send_message(chat_id, 'Set hashtag to your video', reply_markup=Buttons.pass_button(chat_id))
    await Video.hashtag.set()


@dp.message_handler(state=VideoNote.hashtag)
async def video_hashtag(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    acc_id = db.get(table_name="users", field="user_id", value=message.from_user.id)[2]
    text = message.text
    async with state.proxy() as video_note:
        db.add_(table_name='users_video_note',
                field='video_note',
                date=datetime.date.today(),
                user=acc_id,
                name_id=video_note['VideoNote_id'],
                category=video_note['VideoNote_category'],
                hashtag=text,
                comment=video_note['VideoNote_comment'],
                size=video_note['VideoNote_size']
                )
    await state.finish()
    await bot.send_message(chat_id, 'You are in menu', reply_markup=Buttons.secure(chat_id))
