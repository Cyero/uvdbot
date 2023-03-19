import asyncio
import logging
from bot_init import (bot, rt, dp)
from handlers import (register_handlers)


async def start() -> None:
    register_handlers(rt)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN, filename='./src/log.txt')
    asyncio.run(start())
