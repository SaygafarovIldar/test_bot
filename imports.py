import datetime
import logging
import time
from aiogram.types import ReplyKeyboardRemove, Message

import uuid
from states import *
from keyboards import Buttons
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from config import TOKEN
import datetime
from database import Users

# API_TOKEN = TOKEN

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Users('database.db')
