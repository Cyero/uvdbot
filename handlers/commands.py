from aiogram import Router
from keyboards import stickers
from keyboards.keyboard import kb_start
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot_init import BotFSM
from aiogram.types import FSInputFile


async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(BotFSM.menu)
    await message.answer_sticker(sticker=stickers.hello)
    await message.answer(f"Hello, <b>{message.from_user.first_name}!</b> I'm <b>UniversalDownloader Bot. </b> I can"
                         f" download media from next sources for now:", reply_markup=kb_start.as_markup())


async def command_donate_handler(message: Message) -> None:
    await message.answer_sticker(sticker=stickers.donate)
    await message.answer("If you wanna support this Bot you can make donation to the USDT(Tether) account")
    await message.answer_photo(photo=FSInputFile('./src/wallet.png'), has_spoiler=True)


def register_command_handlers(router: Router) -> None:
    router.message.register(command_start_handler, Command(commands="start"))
    router.message.register(command_donate_handler, Command(commands="donate"))
