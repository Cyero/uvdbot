from aiogram import Router
from handlers.commands import register_command_handlers
from handlers.callbacks import register_callback_handlers
from handlers.youtube import register_youtube_handlers


def register_handlers(router: Router) -> None:
    register_command_handlers(router)
    register_callback_handlers(router)
    register_youtube_handlers(router)
