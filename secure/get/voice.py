from secure.main import *


@dp.callback_query_handler(lambda c: c.data == 'get_voice')
async def query(callback: types.CallbackQuery):
    acc_id = db.get(table_name="users", field="user_id", value=callback.from_user.id)[2]
    await bot.send_message(callback.message.chat.id, "Choose category document",
                           reply_markup=Buttons.categories(acc_id, table_name='users_voice', _type='voice'))


@dp.callback_query_handler(lambda call: "cat_voice" in call.data)
async def get_cat_document(callback: types.CallbackQuery):
    category = callback.data.split('_')[-1]
    await callback.answer(text=f'Documents by Category {category}')
    acc_id = db.get(table_name="users", field="user_id", value=callback.from_user.id)[2]
    voices = db.get(table_name="users_voice", field="user", value=acc_id, fetch="all")
    for voice in voices:
        if voice[-1].lower() == category.lower():
            await bot.send_document(chat_id=callback.message.chat.id, document=voice[3],
                                 caption=f'''
<b>🖼 id</b>: <code>{voice[0]}</code>
<b>🗂 category</b>:  <code>{voice[-1]}</code>
<b>💭 comment</b>: <code>{voice[4]}</code>
<b>🧷 hashtag</b>: <code>{voice[-2]}</code>
<b>🕐 date</b>: <code>{voice[2]}</code>
<b>💾 size</b>: <code>{voice[5]}</code>''',
                                 parse_mode='html',
                                 reply_markup=Buttons.remove_btn(callback.message.chat.id))
