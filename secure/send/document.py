from secure.main import *


@dp.callback_query_handler(lambda c: c.data == 'send_document')
async def query(callback: types.CallbackQuery):
    await callback.answer(text='document')
    await bot.edit_message_text('I wait Document', callback.from_user.id, callback.message.message_id)
    await Document.document.set()


@dp.message_handler(state=Document.document, content_types=["document"])
async def document(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    file_id = message.document.file_id
    document_size = message.document.file_size
    async with state.proxy() as document:
        document['document_id'] = file_id
        document['document_size'] = document_size
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    await bot.send_message(chat_id, 'I get photo. Now add category', reply_markup=Buttons.pass_button(chat_id))
    await Document.category.set()


@dp.message_handler(state=Document.category)
async def check_password(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    text = message.text
    async with state.proxy() as document:
        document['document_category'] = text
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    finish_button = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=1)
    finish_button.add('Continue', 'Finish')
    await bot.send_message(chat_id, 'Continue or Finish it', reply_markup=finish_button)
    await Document.finish_continue.set()


@dp.message_handler(state=Document.finish_continue)
async def document_finish(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    if message.text == 'Continue':
        await bot.send_message(chat_id, 'Set comment to your document', reply_markup=Buttons.pass_button(chat_id))
        await Document.comment.set()
    elif message.text == 'Finish':
        acc_id = db.get(table_name="users", field="user_id", value=message.from_user.id)[2]
        async with state.proxy() as video:
            db.add_(table_name='users_document',
                    field='document_id',
                    date=datetime.date.today(),
                    user=acc_id,
                    name_id=video['document_id'],
                    category=video['document_category'],
                    hashtag='',
                    comment='',
                    size=video['document_size']
                    )
        await state.finish()
        await bot.send_message(chat_id, 'You are in menu', reply_markup=Buttons.secure(chat_id))


@dp.message_handler(state=Document.comment)
async def document_comment(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    text = message.text
    async with state.proxy() as document:
        document['document_comment'] = text
    await bot.send_message(chat_id, 'Set hashtag to your document', reply_markup=Buttons.pass_button(chat_id))
    await Document.hashtag.set()


@dp.message_handler(state=Document.hashtag)
async def document_hashtag(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.delete_message(chat_id, message.message_id)
    await bot.delete_message(chat_id, message.message_id - 1)
    acc_id = db.get(table_name="users", field="user_id", value=message.from_user.id)[2]
    text = message.text
    async with state.proxy() as video:
        db.add_(table_name='users_document',
                field='document_id',
                date=datetime.date.today(),
                user=acc_id,
                name_id=video['document_id'],
                category=video['document_category'],
                hashtag=text,
                comment=video['document_comment'],
                size=video['document_size']
                )
    await state.finish()
    await bot.send_message(chat_id, 'You are in menu', reply_markup=Buttons.secure(chat_id))
