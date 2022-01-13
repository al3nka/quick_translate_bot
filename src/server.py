"""
Main file of the project
Creates and starts bot
"""
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand, ParseMode
from aiogram.utils import executor


logging.basicConfig(level=logging.INFO)
API_TOKEN = os.getenv("BOT_API_TOKEN")

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# import handlers after dispatcher creation
# because handlers use dispatcher
from handlers import *


async def set_commands(dispatcher):
    """
    This method sets commands to display
    """
    commands = [
        BotCommand(command="/help", description="Вывести информацию о боте"),
        BotCommand(command="/lang", description="Изменить язык"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await dispatcher.bot.set_my_commands(commands)


async def on_startup(dispatcher):
    """
    This method sets commands when bot starts
    """
    await set_commands(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
