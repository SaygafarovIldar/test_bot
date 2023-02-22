from aiogram.dispatcher.filters.state import State, StatesGroup


class LogIn(StatesGroup):
    username = State()
    password = State()


class Profile(StatesGroup):
    main = State()


class Registration(StatesGroup):
    username = State()
    password = State()
    lang = State()
    verify = State()


class Reset(StatesGroup):
    reset_acc = State()
    username = State()
    password = State()
    profile_username = State()
    profile_password = State()


class Secure(StatesGroup):
    send = State()
    open = State()


class Photo(StatesGroup):
    photo = State()
    category = State()
    finish_continue = State()
    comment = State()
    hashtag = State()


class Video(StatesGroup):
    video = State()
    category = State()
    finish_continue = State()
    comment = State()
    hashtag = State()


class Document(StatesGroup):
    document = State()
    category = State()
    finish_continue = State()
    comment = State()
    hashtag = State()


class Voice(StatesGroup):
    voice = State()
    category = State()
    finish_continue = State()
    comment = State()
    hashtag = State()


class Audio(StatesGroup):
    audio = State()
    category = State()
    finish_continue = State()
    comment = State()
    hashtag = State()


class VideoNote(StatesGroup):
    videoNote = State()
    category = State()
    finish_continue = State()
    comment = State()
    hashtag = State()
