from aiogram import Router, F
from keyboards import stickers
from keyboards.keyboard import (kb_download, kb_cancel, kb_done, kb_exit)
from aiogram.types import (CallbackQuery, Message, FSInputFile)
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from bot_init import BotFSM
from modules import database as db
from modules.yt_loader import (check_link_type, start_download)


async def error_msg(callback: CallbackQuery, link: str, err) -> None:
    await callback.message.answer_sticker(sticker=stickers.crit_error)
    await callback.message.answer(f"{link} -> {err}")
    pass


async def get_url(message: Message) -> None:
    db.add_to_db(f"{message.from_user.id}_yt_tasks", message.text)
    await message.reply("This video has been added to the download queue. "
                        "To add more videos - send me a link", reply_markup=kb_download.as_markup())


async def unknown_format(message: Message) -> None:
    await message.answer_sticker(sticker=stickers.unknown_link)
    await message.answer("It doesn't look like a YouTube link. Are you sure you entered everything "
                         "correctly? Send me a valid link to continue. To cancel, click the "
                         "button below:", reply_markup=kb_cancel.as_markup())


async def download_all(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(BotFSM.download)
    check_link_type(callback.from_user.id)
    queue = db.get_url_from_db(f"{callback.from_user.id}_yt_links")
    await callback.message.answer_sticker(sticker=stickers.starting)
    await callback.message.answer("I start downloading videos. I'll let you know when I'm done, "
                                  "but for now you need to wait a bit")
    error = False
    for link in queue:
        try:
            await start_download(link, callback.from_user.id, callback)
        except AttributeError:
            await callback.message.answer_sticker(sticker=stickers.unavailable)
            await callback.message.answer("Sorry, the service is temporarily unavailable. Please try later",
                                          reply_markup=kb_cancel.as_markup())
            error = True
            break
    if not error:
        await callback.message.answer("All links have been processed. Downloaded videos are ready to be sent. "
                                      " Click the button below to continue:", reply_markup=kb_done.as_markup())


async def send_files(callback: CallbackQuery) -> None:
    db.files_to_send(callback.from_user.id, f"{callback.from_user.id}_yt_files", "yt")
    files = db.get_filelist(f"{callback.from_user.id}_yt_files")
    for file in files:
        await callback.message.answer_video(video=FSInputFile(f"./users/{callback.from_user.id}/yt/{file}"))
    await callback.message.answer_sticker(sticker=stickers.thanks)
    await callback.message.answer("All videos have been submitted. Thank you for using the Bot",
                                  reply_markup=kb_exit.as_markup())


def register_youtube_handlers(router: Router) -> None:
    router.message.register(get_url, F.text.lower().contains("youtu"), BotFSM.youtube)
    router.message.register(unknown_format, BotFSM.youtube)
    router.callback_query.register(download_all, Text('download'), BotFSM.youtube)
    router.callback_query.register(send_files, Text('send'), BotFSM.download)
