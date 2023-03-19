from bot_init import (bot, dp, rt)
from aiogram import Bot
import logging
from os import getenv
from aiohttp.web import run_app
from aiohttp.web_app import Application
from aiogram.webhook.aiohttp_server import (SimpleRequestHandler, setup_application)
from handlers import register_handlers


async def on_startup(bot: Bot) -> None:
    register_handlers(rt)
    await bot.set_webhook(f"{getenv('SITEURL')}/{getenv('TOKEN')}")


def run_bot() -> None:
    dp["base_url"] = getenv('SITEURL')
    dp.startup.register(on_startup)
    app = Application()
    app["bot"] = bot
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=f"/{getenv('TOKEN')}")
    setup_application(app, dp, bot=bot)
    run_app(app, host=f"{getenv('APPHOST'), '127.0.0.1'}", port=int(f"{getenv('APPPORT', 8081)}"))


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN, filename='./src/log.txt')
    run_bot()
