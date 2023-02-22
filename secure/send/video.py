from secure.main import *


@dp.callback_query_handler(lambda c: c.data == 'send_video')
async def query(callback: types.CallbackQuery):
    await callback.answer(text='video')
    await bot.edit_message_text('I wait Video', callback.from_user.id, callback.message.message_id)
    await Video.video.set()


@dp.message_handler(state=Video.video, content_types=["video"])
async def check_password(message: types.Message, state: FSMContext):
    print(message.video.file_id)
    chat_id = message.chat.id
    file_id = message.video.file_id
    file_size = message.video.file_size
    async with state.proxy() as video:
        video['video_id'] = file_id
        video['video_size'] = file_size
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    await bot.send_message(chat_id, 'I get photo. Now add category', reply_markup=Buttons.pass_button(chat_id))
    await Video.category.set()


@dp.message_handler(state=Video.category)
async def check_password(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    text = message.text
    async with state.proxy() as video:
        video['video_category'] = text
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    finish_button = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=1)
    finish_button.add('Continue', 'Finish')
    await bot.send_message(chat_id, 'Continue or Finish it', reply_markup=finish_button)
    await Video.finish_continue.set()


@dp.message_handler(state=Video.finish_continue)
async def check_password(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    if message.text == 'Continue':
        await bot.send_message(chat_id, 'Set comment to your file', reply_markup=Buttons.pass_button(chat_id))
        await Video.comment.set()
    elif message.text == 'Finish':
        acc_id = db.get(table_name="users", field="user_id", value=message.from_user.id)[2]
        async with state.proxy() as video:
            db.add_(table_name='users_video',
                    field='video_id',
                    date=datetime.date.today(),
                    user=acc_id,
                    name_id=video['video_id'],
                    category=video['video_category'],
                    hashtag='',
                    comment='',
                    size=video['video_size']
                    )
        await state.finish()
        await bot.send_message(chat_id, 'You are in menu', reply_markup=Buttons.secure(chat_id))


@dp.message_handler(state=Video.comment)
async def video_comment(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    text = message.text
    async with state.proxy() as video:
        video['video_comment'] = text
    await bot.send_message(chat_id, 'Set hashtag to your video', reply_markup=Buttons.pass_button(chat_id))
    await Video.hashtag.set()


@dp.message_handler(state=Video.hashtag)
async def video_hashtag(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    acc_id = db.get(table_name="users", field="user_id", value=message.from_user.id)[2]
    text = message.text
    async with state.proxy() as video:
        db.add_(table_name='users_video',
                field='video_id',
                date=datetime.date.today(),
                user=acc_id,
                name_id=video['video_id'],
                category=video['video_category'],
                hashtag=text,
                comment=video['video_comment'],
                size=video['video_size']
                )
    await state.finish()
    await bot.send_message(chat_id, 'You are in menu', reply_markup=Buttons.secure(chat_id))
