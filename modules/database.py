import redis
import os

db = redis.Redis(encoding='utf-8', decode_responses=True)
cache = redis.StrictRedis()
CHUNK_SIZE = 5000

"""""
# Redis set names
{chat_id}_yt_tasks - Storage for YouTube URLs getting from user
{chat_id}_yt_links - Storage for links to a YouTube videos, after checking for playlist/channel type.
{chat_id}_yt_files - Storage for name of files which need send to user
"""""


def add_to_db(set_name: str, value: str) -> None:
    db.sadd(set_name, value)


def get_url_from_db(set_name: str) -> list:
    urls = db.smembers(set_name)
    return urls


def files_to_send(chat_id, set_name, module, extension: str = ".mp4") -> None:
    files = [file for file in os.listdir(f'./users/{chat_id}/{module}') if file.endswith(extension)]
    for filename in files:
        db.sadd(set_name, filename)


def get_filelist(set_name: str) -> list:
    filelist = db.smembers(set_name)
    return filelist


def clear_user_sets(chat_id: int) -> True:
    cursor = '0'
    ns_keys = str(chat_id) + '*'
    while cursor != 0:
        cursor, keys = cache.scan(cursor=cursor, match=ns_keys, count=CHUNK_SIZE)
        if keys:
            cache.delete(*keys)
    return True
