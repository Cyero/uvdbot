from aiogram import Router
from keyboards import stickers
from keyboards.keyboard import kb_cancel
from aiogram.filters import Text
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from bot_init import BotFSM
from modules.fsworker import (init_user, clear_user_data)
from modules.database import clear_user_sets


async def menu_start_answer_handler(msg: str, callback: CallbackQuery) -> None:
    await callback.message.answer_sticker(sticker=stickers.waiting)
    await callback.message.answer(f"{msg}  To cancel click the button below", reply_markup=kb_cancel.as_markup())


async def youtube_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(BotFSM.youtube)
    init_user('yt', callback.from_user.id)
    await menu_start_answer_handler("To continue send me a link to a YouTube video.", callback)


async def instagram_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(BotFSM.instagram)
    await menu_start_answer_handler("In development", callback)


async def tiktok_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(BotFSM.tiktok)
    await menu_start_answer_handler("In development", callback)


async def twitter_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(BotFSM.twitter)
    await menu_start_answer_handler("In development", callback)


async def cancel_handler(callback: CallbackQuery, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    clear_user_data(callback.from_user.id)
    clear_user_sets(callback.from_user.id)
    await callback.message.answer_sticker(sticker=stickers.lull)
    await callback.message.answer(f"OK, i'm gonna take a little break. Type <b>/start</b> to run Bot again")


def register_callback_handlers(router: Router) -> None:
    router.callback_query.register(youtube_handler, Text('youtube'), BotFSM.menu)
    router.callback_query.register(instagram_handler, Text('instagram'), BotFSM.menu)
    router.callback_query.register(tiktok_handler, Text('tiktok'), BotFSM.menu)
    router.callback_query.register(twitter_handler, Text('twitter'), BotFSM.menu)
    router.callback_query.register(cancel_handler, Text('cancel'))
    