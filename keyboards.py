from aiogram import types
from googletrans import LANGCODES as LANG_CODES

from database import Users
import constants

db = Users('database.db')


def generate_kb(kb_dict: dict):
    kb = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(text=k, callback_data=v)
        for k, v in kb_dict.items()
    ]
    kb.add(*buttons)
    return kb


class Buttons:

    def log(self):
        inline_login = types.InlineKeyboardButton('log in', callback_data='log_in')
        inline_new_login = types.InlineKeyboardButton('registration', callback_data='registration')
        recover = types.InlineKeyboardButton('reset data', callback_data='recover_acc')
        inline_button = types.InlineKeyboardMarkup(row_width=2).add(inline_login, inline_new_login, recover)
        return inline_button

    def btn_profile(self):
        change_pass = types.InlineKeyboardButton('change password', callback_data='profile_password')
        change_username = types.InlineKeyboardButton('change username', callback_data='profile_username')
        change_recovery = types.InlineKeyboardButton('change reset data', callback_data='recover')
        change_lang = types.InlineKeyboardButton('change lang', callback_data='lang')
        remove = types.InlineKeyboardButton('❌', callback_data='remove')
        btn = types.InlineKeyboardMarkup(row_width=2).add(change_username, change_pass, change_recovery, change_lang,
                                                          remove)
        return btn

    def remove_btn(self):
        remove = types.InlineKeyboardButton('❌', callback_data='remove')
        btn = types.InlineKeyboardMarkup(row_width=1).add(remove)
        return btn

    def verify(self):
        verify_me = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        verify_me.add('Verify')
        return verify_me

    def generate_languages_menu(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        buttons = [types.KeyboardButton(text=lang.title()) for lang in LANG_CODES]
        markup.add(*buttons)
        return markup

    def main_menu(self):
        main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        main_menu.add('Profile', 'Secure', 'Log out')
        return main_menu

    def pass_button(self):
        pass_button = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        pass_button.add('Pass')
        return pass_button

    def secure(self):
        secure = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)
        secure.add('📥 Send', '📤 Get', '📄 Menu')
        return secure

    def send(self):
        return generate_kb(kb_dict=constants.SEND_KEYBOARD_DICT)

    def get(self):
        return generate_kb(kb_dict=constants.GET_KEYBOARD_DICT)

    def send_photo(self, photo, comment, hashtag, category):
        photo = types.InlineKeyboardButton(photo, callback_data='photo_photo')
        comment = types.InlineKeyboardButton(comment, callback_data='photo_comment')
        hashtag = types.InlineKeyboardButton(hashtag, callback_data='photo_hashtag')
        category = types.InlineKeyboardButton(category, callback_data='photo_category')
        back = types.InlineKeyboardButton('⬅Back', callback_data='photo_back')
        finish = types.InlineKeyboardButton('✔', callback_data='photo_finish')
        btn = types.InlineKeyboardMarkup(row_width=2).add(photo, comment, category, hashtag, back, finish)
        return btn

    def settings(self, comment, hashtag, date, category):
        comment = types.InlineKeyboardButton(comment, callback_data='get_comment')
        hashtag = types.InlineKeyboardButton(hashtag, callback_data='get_hashtag')
        date = types.InlineKeyboardButton(date, callback_data='get_date')
        category = types.InlineKeyboardButton(category, callback_data='get_category')
        update = types.InlineKeyboardButton('♻ update', callback_data='get_update')
        btn = types.InlineKeyboardMarkup(row_width=2).add(comment, hashtag, date, category, update)
        return btn

    @staticmethod
    def categories(account_id, table_name, _type):
        kb = types.InlineKeyboardMarkup(row_width=2)
        categories = db.get("category", table_name=table_name, field="user", value=account_id, fetch="all")
        categories = [category[0] for category in categories]
        categories = set([(category, categories.count(category)) for category in categories])

        buttons = []
        for category, _count in categories:
            qty = '(' + str(_count) + ')' if _count > 1 else ''
            if _type == "photo":
                buttons.append(
                    types.InlineKeyboardButton(text=f"{category} {qty}",
                                               callback_data=f"cat_photo_{category}"))
                continue
            elif _type == "video":
                buttons.append(
                    types.InlineKeyboardButton(text=f"{category} {qty}",
                                               callback_data=f"cat_video_{category}"))
                continue
            elif _type == "video_note":
                buttons.append(
                    types.InlineKeyboardButton(text=f"{category} {qty}",
                                               callback_data=f"get_videoNote_{category}"))
                continue
            elif _type == "voice":
                buttons.append(
                    types.InlineKeyboardButton(text=f"{category} {qty}",
                                               callback_data=f"cat_voice_{category}"))
                continue
            elif _type == "audio":
                buttons.append(
                    types.InlineKeyboardButton(text=f"{category} {qty}",
                                               callback_data=f"cat_audio_{category}"))
                continue
        kb.add(*buttons)
        return kb
