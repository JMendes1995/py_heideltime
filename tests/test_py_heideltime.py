import json
from pathlib import Path

from py_heideltime import heideltime

RESOURCES_PATH = Path(__file__).parent / "resources"


def _test_json(
        filepath: Path,
        **kwargs
):
    content = json.load(filepath.open())
    timexs = heideltime(text=content["text"], **kwargs)
    assert timexs == content["timexs"]


def test_heideltime_emoji():
    text = 'texto com emoji 😀 escrito ontem.'
    expected_timexs = [
        {'text': 'ontem', 'tid': 't1', 'type': 'DATE', 'value': 'XXXX-XX-XX', 'span': [26, 31]}
    ]
    timexs = heideltime(text=text, language="Portuguese")
    assert timexs == expected_timexs


def test_heideltime_long_text():
    filepath = RESOURCES_PATH / "long_text.json"
    _test_json(filepath, language="Portuguese")


def test_heideltime_pt_arquivo():
    filepath = RESOURCES_PATH / "pt_arquivo.json"
    _test_json(filepath, language="Portuguese")


def test_heideltime_pt_wikipedia():
    filepath = RESOURCES_PATH / "pt_wikipedia.json"
    _test_json(filepath, language="Portuguese")


def test_heideltime_en_options():
    filepath = RESOURCES_PATH / "en_options.json"
    _test_json(filepath, language="English", dct='1939-08-31')


def test_heideltime_fr():
    filepath = RESOURCES_PATH / "fr.json"
    _test_json(filepath, language="French")


def test_heideltime_empty_results():
    filepath = RESOURCES_PATH / "no_timexs.txt"
    text = filepath.open(encoding="utf-8").read()
    timexs = heideltime(text=text)
    assert not timexs


def test_heideltime_empty_input():
    timexs = heideltime(text="")
    assert not timexs
