import os
import platform

import emoji


def has_emoji(text: str) -> bool:
    if emoji.distinct_emoji_list(text):
        return True
    return False


def process_text(text: str) -> str:
    if has_emoji(text):
        return emoji.replace_emoji(text, replace="")
    else:
        return text


def execute_command(cmd: str) -> str:
    if platform.system() == "Windows":
        import subprocess
        return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8")
    else:
        return os.popen(cmd).read()
