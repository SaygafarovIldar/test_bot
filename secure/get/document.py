from secure.main import *


@dp.callback_query_handler(lambda c: c.data == 'get_document')
async def query(callback: types.CallbackQuery):
    acc_id = db.get(table_name="users", field="user_id", value=callback.from_user.id)[2]
    await bot.send_message(callback.message.chat.id, "Choose category document",
                           reply_markup=Buttons.categories(acc_id, table_name='users_document', _type='document'))


@dp.callback_query_handler(lambda call: "cat_document" in call.data)
async def get_cat_document(callback: types.CallbackQuery):
    category = callback.data.split('_')[-1]
    await callback.answer(text=f'Documents by Category {category}')
    acc_id = db.get(table_name="users", field="user_id", value=callback.from_user.id)[2]
    documents = db.get(table_name="users_document", field="user", value=acc_id, fetch="all")
    print(documents)
    for document in documents:
        if document[8].lower() == category.lower():
            await bot.send_document(chat_id=callback.message.chat.id, document=document[3],
                                 caption=f'''
<b>🖼 id</b>: <code>{document[0]}</code>
<b>🗂 category</b>:  <code>{document[7]}</code>
<b>💭 comment</b>: <code>{document[5]}</code>
<b>🧷 hashtag</b>: <code>{document[-2]}</code>
<b>🕐 date</b>: <code>{document[2]}</code>
<b>💾 size</b>: <code>{document[4]}</code>''',
                                 parse_mode='html',
                                 reply_markup=Buttons.remove_btn(callback.message.chat.id))
