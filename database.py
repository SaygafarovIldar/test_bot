import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# userId
cursor.execute('''CREATE TABLE IF NOT EXISTS users
(id	INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
account_id)
''')

# account
cursor.execute('''CREATE TABLE IF NOT EXISTS account
(id	INTEGER PRIMARY KEY AUTOINCREMENT,
account_id TEXT,
date_of_registration TEXT,
username TEXT,
password TEXT,
language TEXT,
user_create INTEGER,
reset_acc TEXT)
''')

# get_settings
cursor.execute('''CREATE TABLE IF NOT EXISTS get_settings
(id	INTEGER PRIMARY KEY AUTOINCREMENT,
account_id TEXT,
categories TEXT,
settings_category TEXT,
settings_comment TEXT,
settings_hashtag TEXT,
settings_date TEXT)
''')

# send_settings
cursor.execute('''CREATE TABLE IF NOT EXISTS get_settings
(id	INTEGER PRIMARY KEY AUTOINCREMENT,
account_id TEXT,
categories TEXT,
settings_category TEXT,
settings_comment TEXT,
settings_hashtag TEXT,
settings_date TEXT)
''')

# users_message / Сообщение отпр ими
cursor.execute('''CREATE TABLE IF NOT EXISTS users_message
(id	INTEGER PRIMARY KEY AUTOINCREMENT,
user INTEGER,
date TEXT,
message_id TEXT,
comment TEXT)
''')

# users_photo
cursor.execute('''CREATE TABLE IF NOT EXISTS users_photo
(id	INTEGER PRIMARY KEY AUTOINCREMENT,
user INTEGER,
date TEXT,
photo_id TEXT,
size TEXT,
comment TEXT,
hashtag TEXT,
category TEXT
)
''')

# users_video
cursor.execute('''CREATE TABLE IF NOT EXISTS users_video
(id	INTEGER PRIMARY KEY AUTOINCREMENT,
user INTEGER,
date TEXT,
video_id TEXT,
file_name TEXT,
duration INTEGER,
size INTEGER,
comment TEXT,
hashtag TEXT,
category TEXT)
''')

# users_video_note
cursor.execute('''CREATE TABLE IF NOT EXISTS users_video_note
(id	INTEGER PRIMARY KEY AUTOINCREMENT,
user INTEGER,
date TEXT,
video_note_id TEXT,
file_name TEXT,
duration INTEGER,
size INTEGER,
comment TEXT,
hashtag TEXT,
category TEXT)
''')

# users_document
cursor.execute('''CREATE TABLE IF NOT EXISTS users_document
(id	INTEGER PRIMARY KEY AUTOINCREMENT,
user INTEGER,
date TEXT,
document_id TEXT,
file_name TEXT,
size INTEGER,
comment TEXT,
hashtag TEXT,
category TEXT)
''')

# users_file
cursor.execute('''CREATE TABLE IF NOT EXISTS users_file
(id	INTEGER PRIMARY KEY AUTOINCREMENT,
user INTEGER,
date TEXT,
file_id TEXT,
file_name TEXT,
size INTEGER,
comment TEXT,
hashtag TEXT,
category TEXT)
''')

# users_audio
cursor.execute('''CREATE TABLE IF NOT EXISTS users_audio
(id	INTEGER PRIMARY KEY AUTOINCREMENT,
user INTEGER,
date TEXT,
audio_id TEXT,
file_name TEXT,
size INTEGER,
comment TEXT,
hashtag TEXT,
category TEXT)
''')

# users_voice
cursor.execute('''CREATE TABLE IF NOT EXISTS users_voice
(id	INTEGER PRIMARY KEY AUTOINCREMENT,
user INTEGER,
date TEXT,
voice_id TEXT,
file_name TEXT,
size INTEGER,
comment TEXT,
hashtag TEXT,
category TEXT)
''')


class Users:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    # ------- Registration ------- #

    def add_user_info(self, username, password, language, date_of_registration, reset_acc, account_id,
                      user_create):
        with self.connection:
            """
            отправляю все введенное данные пользователей в бд 
            """
            result = self.cursor.execute(
                "INSERT INTO account ("
                "username, password, language, date_of_registration, reset_acc, account_id, user_create) "
                "VALUES (?,?,?,?,?,?,?)",
                (username, password, language, date_of_registration, reset_acc, account_id, user_create))
            return result

    def add_settings(self, account_id, categories, settings_category, settings_comment, settings_hashtag,
                     settings_date):
        with self.connection:
            """
            Настройка профилья при получение данных с бд. отправить фото с какими данными (не все готово)
            """
            result = self.cursor.execute(
                "INSERT INTO get_settings ("
                "account_id, categories, settings_category, settings_comment, settings_hashtag, settings_date) "
                "VALUES (?,?,?,?,?,?)",
                (account_id, categories, settings_category, settings_comment, settings_hashtag, settings_date))
            return result

    # ------- Checking User in accounts ------- #
    def check_user(self, username, password):
        with self.connection:
            """
            Log in - проверяет логин и пароль есть ли пользователь и правильность паролья 
            """
            result = self.cursor.execute("SELECT * FROM account WHERE username = ? AND password = ?",
                                         (username, password)).fetchone()
            return True if result else False

    # ------- Add userId in table users ------- #
    def add_user_id(self, user_id):
        with self.connection:
            """
            тут присваивает аккаунт id на user id telegram-a. (Если войти c tg_асс2 то tg_асс1 автоматом выйдет с аккаунта)
            """
            self.cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))

    def check_(self, table, table_name, value):
        with self.connection:
            result = self.cursor.execute(f"SELECT * FROM {table} WHERE {table_name} = ?", (value,)).fetchone()
            return True if result else False

    def check_user_session(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ? ", (user_id,)).fetchall()
            result = list(result)[0][2]
            return True if result else False

    # ------- Set acc_id like login or log out func ------- #
    def set_account_id(self, account_id, user_id):
        with self.connection:
            """
            Если с другого аккаунта (user_id) телеграма войти в аккаунт то обновляется значение acc_id возле user_id
            """
            self.cursor.execute("UPDATE users SET account_id = ? WHERE user_id = ?", (account_id, user_id,))

    # ------- delete same account_id from other id ------- #
    def delete_same(self, account_id):
        with self.connection:
            """
            Удаляет аккаунт айди от юзер аккаунта. Похож на ссесию.
            """
            self.cursor.execute("UPDATE users SET account_id = '' WHERE account_id = ?", (account_id,))

    def add_(self, table_name, field, name_id, date, category, comment, hashtag, size, user):
        with self.connection:
            result = self.cursor.execute(
                f"INSERT INTO {table_name} ({field}, date, category, comment, hashtag, size, user) VALUES (?,?,?,"
                "?,?,?,?)",
                (name_id, date, category, comment, hashtag, size, user,))
            return result

    def get(self, *args, table_name, field, value, fetch="one"):
        """Получаем все из таблицы 'table_name' по полю 'field' [REFACTORED]"""

        table_fields = ",".join(args) if args else "*"

        with self.connection:
            if fetch == "one":
                result = self.cursor.execute(f"SELECT {table_fields} FROM {table_name} WHERE {field} = ?",
                                             (value,)).fetchone()
            elif fetch == "all":
                result = self.cursor.execute(f"SELECT {table_fields} FROM {table_name} WHERE {field} = ?",
                                             (value,)).fetchall()
            return result

    # def change_profile_reset_acc(self, account_id, reset_acc):
    #     with self.connection:
    #         self.cursor.execute("UPDATE account SET reset_acc = ? WHERE account_id = ?",
    #                             (reset_acc, account_id,))

    def update_profile_(self, table, table_name, account_id, table_value):
        with self.connection:
            self.cursor.execute(f"UPDATE account SET {table} = ? WHERE {table_name} = ?",
                                (table_value, account_id,))

        # def update_get_settings_category(self, account_id, category):
        #     with self.connection:
        #         self.cursor.execute("UPDATE get_settings SET settings_category = ? WHERE account_id = ?",
        #                             (category, account_id,))
        #
        # def update_get_settings_comment(self, account_id, comment):
        #     with self.connection:
        #         self.cursor.execute("UPDATE get_settings SET settings_comment = ? WHERE account_id = ?",
        #                             (comment, account_id,))
