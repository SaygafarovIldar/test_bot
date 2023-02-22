from secure.main import *


@dp.callback_query_handler(lambda c: c.data == 'get_video')
async def query(callback: types.CallbackQuery):
    acc_id = db.get(table_name="users", field="user_id", value=callback.from_user.id)[2]
    await bot.send_message(callback.message.chat.id, "Choose category video",
                           reply_markup=Buttons.categories(acc_id, table_name='users_video', _type="video"))


@dp.callback_query_handler(lambda call: "cat_video" in call.data)
async def get_cat_photo(callback: types.CallbackQuery):
    category = callback.data.split('_')[-1]
    await callback.answer(text=f'Videos by Category {category}')
    acc_id = db.get(table_name="users", field="user_id", value=callback.from_user.id)[2]
    videos = db.get(table_name="users_video", field="user", value=acc_id, fetch="all")
    for video in videos:
        if video[7].lower() == category.lower():
            await bot.send_video(chat_id=callback.message.chat.id, video=video[3],
                             caption=f'<b>🖼 id</b>: <code>{video[0]}</code>\n<b>🗂 category</b>:  <code>{video[7]}</code>\n<b>💭 comment</b>: <code>{video[5]}</code>\n'
                                     f'<b>🧷 hashtag</b>: <code>{video[-2]}</code>\n<b>🕐 date</b>: <code>{video[2]}</code>\n<b>💾 size</b>: <code>{video[4]}</code>',
                             parse_mode='html', reply_markup=Buttons.remove_btn(callback.message.chat.id))
