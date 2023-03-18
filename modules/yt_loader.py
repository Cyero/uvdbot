from pytube import YouTube, Playlist, Channel, exceptions
from modules import database as db
from aiogram.types import CallbackQuery
from keyboards import stickers


async def error_msg(callback: CallbackQuery, link: str, err) -> None:
    await callback.message.answer_sticker(sticker=stickers.crit_error)
    await callback.message.answer(f"{link} \n <b>-> {err}</b>")
    pass


async def start_download(link: str, chat_id: int, callback: CallbackQuery) -> None:
    yt = YouTube(link)
    try:
        yt.streams.filter(file_extension='mp4').get_highest_resolution().download(output_path=f'./users/{chat_id}/yt')
    except exceptions.LiveStreamError as exc:
        await error_msg(callback, link, exc)
    except exceptions.AgeRestrictedError as exc:
        await error_msg(callback, link, exc)
    except exceptions.RecordingUnavailable as exc:
        await error_msg(callback, link, exc)
    except exceptions.MembersOnly as exc:
        await error_msg(callback, link, exc)
    except exceptions.VideoUnavailable as exc:
        await error_msg(callback, link, exc)
    except exceptions.PytubeError:
        await error_msg(callback, link, "Internal error")
    except exceptions.RegexMatchError:
        await error_msg(callback, link, "Invalid URL")


def check_link_type(chat_id: int) -> None:
    urls = db.get_url_from_db(f"{chat_id}_yt_tasks")
    for link in urls:
        if "/playlist" in link:
            yt = Playlist(link)
            for url in yt.video_urls:
                db.add_to_db(f"{chat_id}_yt_links", url)
        elif "/@" in link:
            yt = Channel(link)
            for url in yt.video_urls:
                db.add_to_db(f"{chat_id}_yt_links", url)
        else:
            db.add_to_db(f"{chat_id}_yt_links", link)
