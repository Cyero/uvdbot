import subprocess


def init_user(module: str, chat_id: int = "callback.from_user.id") -> None:
    subprocess.run(f'mkdir -p ./users/{chat_id}/{module}/', shell=True)


def clear_user_data(chat_id: int = "callback.from_user.id") -> None:
    subprocess.run(f'rm -rf ./users/{chat_id}', shell=True)
