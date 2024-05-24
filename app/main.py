# Python imports
from typing import Dict, Any
from os import getenv

# Fastapi imports
from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

# import custom foos, classes, etc
from routing import base_router

# config data
TOKEN = getenv("TELEGRAM_TOKEN")

# declare fastapi app
app = FastAPI()

@app.on_event("startup")
async def run_bot_webhook():
    ''' run Telegram pooling on start of app '''
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(base_router)
    await dp.start_polling(bot)
