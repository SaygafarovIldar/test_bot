from secure.main import *


@dp.callback_query_handler(lambda c: c.data == 'send_photo')
async def query(callback: types.CallbackQuery):
    await callback.answer(text='photo')
    await bot.edit_message_text('I wait Photo', callback.from_user.id, callback.message.message_id)
    await Photo.photo.set()

@dp.message_handler(state=Photo.photo, content_types=["photo"])
async def check_password(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    file_id = message.photo[0].file_id
    file_size = message.photo[0].file_size
    async with state.proxy() as photo:
        photo['photo_id'] = file_id
        photo['photo_size'] = file_size
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    await bot.send_message(chat_id, 'I get photo. Now add category', reply_markup=Buttons.pass_button(chat_id))
    await Photo.category.set()


@dp.message_handler(state=Photo.category)
async def check_password(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    text = message.text
    async with state.proxy() as photo:
        photo['photo_category'] = text
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    finish_button = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=1)
    finish_button.add('Continue', 'Finish')
    await bot.send_message(chat_id, 'Continue or Finish it', reply_markup=finish_button)
    await Photo.finish_continue.set()


@dp.message_handler(state=Photo.finish_continue)
async def check_password(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    if message.text == 'Continue':
        await bot.send_message(chat_id, 'Set comment to your file', reply_markup=Buttons.pass_button(chat_id))
        await Photo.comment.set()
    elif message.text == 'Finish':
        acc_id = db.get(table_name="users", field="user_id", value=message.from_user.id)[2]
        async with state.proxy() as photo:
            db.add_(table_name='users_photo',
                    field='photo_id',
                    date=datetime.date.today(),
                    user=acc_id,
                    name_id=photo['photo_id'],
                    category=photo['photo_category'],
                    hashtag='',
                    comment='',
                    size=photo['photo_size']
                    )
        await state.finish()
        await bot.send_message(chat_id, 'You are in menu', reply_markup=Buttons.secure(chat_id))


@dp.message_handler(state=Photo.comment)
async def check_password(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    text = message.text
    async with state.proxy() as photo:
        photo['photo_comment'] = text
    await bot.send_message(chat_id, 'Set hashtag to your file', reply_markup=Buttons.pass_button(chat_id))
    await Photo.hashtag.set()


@dp.message_handler(state=Photo.hashtag)
async def check_password(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    acc_id = db.get(table_name="users", field="user_id", value=message.from_user.id)[2]
    text = message.text
    async with state.proxy() as photo:
        db.add_(table_name='users_photo',
                field='photo_id',
                date=datetime.date.today(),
                user=acc_id,
                name_id=photo['photo_id'],
                category=photo['photo_category'],
                hashtag=text,
                comment=photo['photo_comment'],
                size=photo['photo_size']
                )
    await state.finish()
    await bot.send_message(chat_id, 'You are in menu', reply_markup=Buttons.secure(chat_id))
