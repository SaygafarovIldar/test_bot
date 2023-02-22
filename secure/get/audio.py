from secure.main import *


@dp.callback_query_handler(lambda c: c.data == 'get_audio')
async def query(callback: types.CallbackQuery):
    acc_id = db.get(table_name="users", field="user_id", value=callback.from_user.id)[2]
    await bot.send_message(callback.message.chat.id, "Choose category audio",
                           reply_markup=Buttons.categories(acc_id, table_name='users_audio', _type='audio'))


@dp.callback_query_handler(lambda call: "cat_audio" in call.data)
async def get_cat_document(callback: types.CallbackQuery):
    category = callback.data.split('_')[-1]
    await callback.answer(text=f'Documents by Category {category}')
    acc_id = db.get(table_name="users", field="user_id", value=callback.from_user.id)[2]
    audios = db.get(table_name="users_voice", field="user", value=acc_id, fetch="all")
    for audio in audios:
        if audio[-1].lower() == category.lower():
            await bot.send_audio(chat_id=callback.message.chat.id, audio=audio[3],
                                 caption=f'''
<b>🖼 id</b>: <code>{audio[0]}</code>
<b>🗂 category</b>:  <code>{audio[-1]}</code>
<b>💭 comment</b>: <code>{audio[4]}</code>
<b>🧷 hashtag</b>: <code>{audio[-2]}</code>
<b>🕐 date</b>: <code>{audio[2]}</code>
<b>💾 size</b>: <code>{audio[5]}</code>''',
                                 parse_mode='html',
                                 reply_markup=Buttons.remove_btn(callback.message.chat.id))
