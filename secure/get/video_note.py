from secure.main import *


@dp.callback_query_handler(lambda c: c.data == 'get_video_note')
async def query(callback: types.CallbackQuery):
    acc_id = db.get(table_name="users", field="user_id", value=callback.from_user.id)[2]
    await bot.send_message(callback.message.chat.id, "Choose category video note",
                           reply_markup=Buttons.categories(acc_id, table_name='users_video_note', _type="video_note"))


@dp.callback_query_handler(lambda call: "get_videoNote" in call.data)
async def get_cat_photo(callback: types.CallbackQuery):
    category = callback.data.split('_')[-1]
    await callback.answer(text=f'Video notes by Category {category}')
    acc_id = db.get(table_name="users", field="user_id", value=callback.from_user.id)[2]
    video_notes = db.get(table_name="users_video_note", field="user", value=acc_id, fetch="all")
    for video_note in video_notes:
        if video_note[7].lower() == category.lower():
            await bot.send_video_note(chat_id=callback.message.chat.id, video_note=video_note[3], reply_markup=Buttons.remove_btn(callback.message.chat.id))
            await bot.send_message(callback.message.chat.id,
                                   text=f'<b>🖼 id</b>: <code>{video_note[0]}</code>\n<b>🗂 category</b>:  <code>{video_note[7]}</code>\n<b>💭 comment</b>: <code>{video_note[5]}</code>\n'
                                        f'<b>🧷 hashtag</b>: <code>{video_note[-2]}</code>\n<b>🕐 date</b>: <code>{video_note[2]}</code>\n<b>💾 size</b>: <code>{video_note[4]}</code>',
                                   parse_mode='html', reply_markup=Buttons.remove_btn(callback.message.chat.id))
