from secure.main import *


@dp.callback_query_handler(lambda c: c.data == 'get_photo')
async def query(callback: types.CallbackQuery):
    acc_id = db.get(table_name="users", field="user_id", value=callback.from_user.id)[2]
    await bot.send_message(callback.message.chat.id, "Choose category",
                           reply_markup=Buttons.categories(acc_id, table_name='users_photo', _type="photo"))


@dp.callback_query_handler(lambda call: "cat_photo" in call.data)
async def get_cat_photo(callback: types.CallbackQuery):
    category = callback.data.split('_')[-1]

    await callback.answer(text=f'Photos by Category {category}')
    acc_id = db.get(table_name="users", field="user_id", value=callback.from_user.id)[2]
    photos = db.get(table_name="users_photo", field="user", value=acc_id, fetch="all")
    print(photos)
    for photo in photos:
        if photo[7].lower() == category.lower():
            await bot.send_photo(chat_id=callback.message.chat.id, photo=photo[3],
                                 caption=f'''
<b>🖼 id</b>: <code>{photo[0]}</code>
<b>🗂 category</b>:  <code>{photo[7]}</code>
<b>💭 comment</b>: <code>{photo[5]}</code>
<b>🧷 hashtag</b>: <code>{photo[-2]}</code>
<b>🕐 date</b>: <code>{photo[2]}</code>
<b>💾 size</b>: <code>{photo[4]}</code>''',
                                 parse_mode='html',
                                 reply_markup=Buttons.remove_btn(callback.message.chat.id))
