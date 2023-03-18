from os import getenv
from aiogram import (Bot, Dispatcher, Router)
from aiogram.fsm.state import State, StatesGroup


class BotFSM(StatesGroup):
    menu = State()
    youtube = State()
    instagram = State()
    tiktok = State()
    twitter = State()
    download = State()


bot = Bot(token=getenv('TOKEN'), parse_mode='HTML')
rt = Router()
dp = Dispatcher()
dp.include_router(rt)
