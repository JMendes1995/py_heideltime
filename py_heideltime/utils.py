import os
import platform

import emoji


def _replace_emojis(text: str, replace: str = " ") -> str:
    """Replaces the emojis from the texts without changing the size of the original text.
    The replacement is made so that the entire span taken by the emoji is replaced by the `replace` string."""
    ltext = list(text)
    matches = emoji.emoji_list(text)
    for match in matches:
        s, e = match["match_start"], match["match_end"]
        ltext[s: e] = [replace] * (e - s)
    return "".join(ltext)


def process_text(text: str) -> str:
    ptext = _replace_emojis(text)
    return ptext


def execute_command(cmd: str) -> str:
    if platform.system() == "Windows":
        import subprocess
        return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8")
    else:
        return os.popen(cmd).read()
