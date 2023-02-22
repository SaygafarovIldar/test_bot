from imports import *
import message_texts


@dp.callback_query_handler(lambda c: c.data == 'log_in')
async def process_log(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Write your username')
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await LogIn.username.set()


@dp.message_handler(state=LogIn.username)
async def check_password(message: types.Message, state: FSMContext):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'put your password')
    async with state.proxy() as logIn:
        logIn['username'] = message.text
    await LogIn.password.set()


@dp.message_handler(state=LogIn.password)
async def check_password(message: types.Message, state: FSMContext):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    chat_id = message.chat.id
    async with state.proxy() as logIn:
        logIn['password'] = message.text

    is_exists = db.check_user(username=logIn['username'], password=logIn['password'])
    if is_exists:
        get_acc = db.get(table_name="account", field="username", value=logIn['username'])[1]
        db.delete_same(account_id=get_acc)
        db.set_account_id(user_id=message.from_user.id, account_id=get_acc)
        await bot.send_message(chat_id, 'hooray🎉', reply_markup=Buttons.main_menu(message.chat.id))
        await state.finish()
    else:
        await state.finish()
        await bot.send_message(chat_id, 'you entered incorrect data', reply_markup=Buttons.log(chat_id))


@dp.callback_query_handler(lambda c: c.data == 'recover_acc')
async def process_recover(callback: types.CallbackQuery):
    await bot.answer_callback_query(callback.id)
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, 'Put your recovery code')
    await Reset.reset_acc.set()


@dp.message_handler(state=Reset.reset_acc)
async def check_recovery_code(message: types.Message, state: FSMContext):
    text = message.text
    is_exists = db.check_(value=text, table_name='reset_acc', table='account')
    if is_exists:
        async with state.proxy() as reset_acc:
            reset_acc['reset_data'] = text
        await bot.delete_message(message.from_user.id, message.message_id)
        await bot.send_message(message.chat.id, 'Now set your new username')
        await Reset.username.set()
    else:
        await bot.delete_message(message.from_user.id, message.message_id)
        await bot.delete_message(message.from_user.id, message.message_id - 1)
        await bot.send_message(message.chat.id, 'sorry you entered incorrect reset code',
                               reply_markup=Buttons.log(message.chat.id))
        await state.finish()


@dp.message_handler(state=Reset.username)
async def check_recovery_code(message: types.Message, state: FSMContext):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    text = message.text
    if not db.check_(value=text, table_name='username', table='account'):
        async with state.proxy() as reset_acc:
            reset_acc['reset_username'] = text
            db.update_profile_(table='username', table_value=text, table_name='reset_acc',
                               account_id=reset_acc['reset_data'])
            await bot.send_message(message.chat.id, 'I get your username Now add password !')
            await Reset.password.set()
    else:
        await bot.send_message(message.chat.id, 'Sorry, this username is taken. Write your another username')
        await Reset.username.set()


@dp.message_handler(state=Reset.password)
async def check_recovery_code(message: types.Message, state: FSMContext):
    text = message.text
    async with state.proxy() as reset_acc:
        get_acc = db.get(table_name="account", field="username", value=reset_acc['reset_username'])[1]
        db.update_profile_(table='password', table_value=text, table_name='reset_acc',
                           account_id=reset_acc['reset_data'])
        db.delete_same(account_id=get_acc)
        db.set_account_id(user_id=message.from_user.id, account_id=get_acc)
    await bot.send_message(message.chat.id, 'Hooray you log in to your account',
                           reply_markup=Buttons.main_menu(message.chat.id))
    await state.finish()


# ----- answer to registration - inline button ----- #
@dp.callback_query_handler(lambda c: c.data == 'registration')
async def process_log(callback: types.CallbackQuery):
    await bot.answer_callback_query(callback.id)
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, 'Write your username')
    await Registration.username.set()


@dp.message_handler(state=Registration.username)
async def check_password(message: types.Message, state: FSMContext):
    text = message.text
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    chat_id = message.chat.id
    if not db.check_(value=text, table_name='username', table='account'):
        async with state.proxy() as data:
            data['username'] = message.text
        await bot.send_message(chat_id, 'put your password')
        await Registration.password.set()
    else:
        await bot.send_message(chat_id, 'sorry this username we have')
        await Registration.username.set()


@dp.message_handler(state=Registration.password)
async def check_password(message: types.Message, state: FSMContext):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    chat_id = message.chat.id
    async with state.proxy() as data:
        data['password'] = message.text
    await bot.send_message(chat_id, 'Cool choose your lang',
                           reply_markup=Buttons.generate_languages_menu(message.chat.id))
    await Registration.lang.set()


@dp.message_handler(state=Registration.lang)
async def check_password(message: types.Message, state: FSMContext):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    chat_id = message.chat.id
    async with state.proxy() as data:
        data['lang'] = message.text
        await bot.send_message(chat_id,
                               f'username: {data["username"]}\npassword: {data["password"]}\nlanguage: {data["lang"]}',
                               reply_markup=Buttons.verify(message.chat.id))
    await Registration.verify.set()


@dp.message_handler(state=Registration.verify)
async def check_password(message: types.Message, state: FSMContext):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    chat_id = message.chat.id
    acc = uuid.uuid4().hex
    async with state.proxy() as data:
        db.add_user_info(username=data['username'],
                         password=data['password'],
                         date_of_registration=datetime.date.today(),
                         language=data['lang'],
                         user_create=message.from_user.id,
                         account_id=acc,
                         reset_acc='reset_' + uuid.uuid4().hex)

        db.add_settings(account_id=acc, categories='✔', settings_category='✔', settings_comment='✔',
                        settings_hashtag='✔', settings_date='✔')
    db.set_account_id(user_id=message.from_user.id, account_id=acc)
    await state.finish()
    await bot.send_message(chat_id, 'You have finished', reply_markup=Buttons.main_menu(message.chat.id))


"""
после регистрации 
"""


@dp.message_handler(text="Profile")
@dp.message_handler(state=Profile.main)
async def handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if not db.check_user_session(message.from_user.id):
        await bot.send_message(chat_id, 'Hello choose one of them', reply_markup=Buttons.log(chat_id))
    else:
        acc_id = db.get(table_name="users", field="user_id", value=message.from_user.id)[2]
        profile = db.get(table_name="account", field="account_id", value=acc_id)
        await bot.send_message(chat_id,
                               message_texts.USER_PROFILE_TEXT.format(profile[3], profile[4], profile[7], profile[5],
                                                                      profile[2]), parse_mode='html',
                               reply_markup=Buttons.btn_profile(chat_id))


@dp.callback_query_handler(lambda c: c.data == 'recover')
async def process_log(callback: types.CallbackQuery):
    await callback.answer(text='recovered')
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    acc_id = db.get(table_name="users", field="user_id", value=callback.from_user.id)[2]
    # db.change_profile_reset_acc(account_id=acc_id, reset_acc='reset_' + uuid.uuid4().hex)
    db.update_profile_(account_id=acc_id, table_value='reset_' + uuid.uuid4().hex, table='reset_acc',
                       table_name='account_id')
    profile = db.get(table_name="account", field="account_id", value=acc_id)
    await bot.send_message(callback.message.chat.id,
                           message_texts.USER_PROFILE_TEXT.format(profile[3], profile[4], profile[7], profile[5],
                                                                  profile[2]),
                           parse_mode='html',
                           reply_markup=Buttons.btn_profile(callback.message.chat.id))


@dp.callback_query_handler(lambda c: c.data == 'profile_username')
async def process_log(callback: types.CallbackQuery):
    await callback.answer(text='Changing username')
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await bot.send_message(callback.message.chat.id, 'Send your new username', )
    await Reset.profile_username.set()


@dp.message_handler(state=Reset.profile_username)
async def check_password(message: types.Message, state: FSMContext):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    text = message.text
    acc_id = db.get(table_name="users", field="user_id", value=message.from_user.id)[2]
    if not db.check_(value=text, table_name='username', table='account'):
        db.update_profile_(table='username', table_value=text, table_name='account_id', account_id=acc_id)
        profile = db.get(table_name="account", field="account_id", value=acc_id)
        await bot.send_message(message.chat.id,
                               message_texts.USER_PROFILE_TEXT.format(profile[3], profile[4], profile[7], profile[5],
                                                                      profile[2]),
                               parse_mode='html',
                               reply_markup=Buttons.btn_profile(message.chat.id))
        await state.finish()
    else:
        await bot.send_message(message.chat.id, 'Sorry, this username is taken. Write your another username')
        await Reset.profile_username.set()


@dp.callback_query_handler(lambda c: c.data == 'profile_password')
async def process_log(callback: types.CallbackQuery):
    await callback.answer(text='Changing username')
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await bot.send_message(callback.message.chat.id, 'Send your new password')
    await Reset.profile_password.set()


@dp.message_handler(state=Reset.profile_password)
async def check_password(message: types.Message, state: FSMContext):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    text = message.text
    acc_id = db.get(table_name="users", field="user_id", value=message.from_user.id)[2]
    db.update_profile_(table='password', table_value=text, table_name='account_id', account_id=acc_id)
    profile = db.get(table_name="account", field="account_id", value=acc_id)
    await bot.send_message(message.chat.id,
                           message_texts.USER_PROFILE_TEXT.format(profile[3], profile[4], profile[7], profile[5],
                                                                  profile[2]),
                           parse_mode='html',
                           reply_markup=Buttons.btn_profile(message.chat.id))
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'lang')
async def process_log(callback: types.CallbackQuery):
    await callback.answer(text='Coming soon')
