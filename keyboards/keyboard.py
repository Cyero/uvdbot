from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


# List of buttons
youtube = InlineKeyboardButton(text='YouTube', callback_data='youtube')
instagram = InlineKeyboardButton(text='Instagram', callback_data='instagram')
tiktok = InlineKeyboardButton(text='TikTok', callback_data='tiktok')
twitter = InlineKeyboardButton(text='Twitter', callback_data='twitter')
cancel = InlineKeyboardButton(text='Cancel', callback_data='cancel')
download = InlineKeyboardButton(text='Download all', callback_data='download')
send = InlineKeyboardButton(text='Get it', callback_data='send')
done = InlineKeyboardButton(text='Exit', callback_data='cancel')


# Keyboards
kb_start = InlineKeyboardBuilder().add(youtube, instagram, tiktok, twitter)
kb_cancel = InlineKeyboardBuilder().add(cancel)
kb_download = InlineKeyboardBuilder().add(download, cancel)
kb_done = InlineKeyboardBuilder().add(send)
kb_exit = InlineKeyboardBuilder().add(done)
