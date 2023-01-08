import json
from pathlib import Path

from py_heideltime import py_heideltime

RESOURCES_PATH = Path(__file__).parent / "resources"


def test_py_heideltime_emoji():
    text = 'texto com emoji 😀'
    expected_score = []
    expected_time_ml = expected_text_normalized = 'texto com emoji'

    score, text_normalized, time_ml = py_heideltime(text=text, language="Portuguese")

    assert text_normalized == expected_text_normalized
    assert time_ml == expected_time_ml
    assert score == expected_score


def _test_json(
        filepath: Path,
        **kwargs
):
    content = json.load(filepath.open())
    score, text_normalized, time_ml = py_heideltime(text=content["text"], **kwargs)

    assert text_normalized == content["text_normalized"]
    assert time_ml == content["time_ml"]
    assert score == content["score"]


def test_py_heideltime_long_text():
    filepath = RESOURCES_PATH / "long_text.json"
    _test_json(filepath, language="Portuguese")


def test_py_heideltime_pt_wikipedia_planeta():
    filepath = RESOURCES_PATH / "pt_wikipedia_planeta.json"
    _test_json(filepath, language="Portuguese")


def test_py_heideltime_pt_arquivo_jugular():
    filepath = RESOURCES_PATH / "pt_arquivo_jugular.json"
    _test_json(filepath, language="Portuguese")


def test_py_heideltime_pt_wikipedia_25_de_abril():
    filepath = RESOURCES_PATH / "pt_wikipedia_25_de_abril.json"
    _test_json(filepath, language="Portuguese")


def test_py_heideltime_pt_wikipedia_operacao_marques():
    filepath = RESOURCES_PATH / "pt_wikipedia_operacao_marques.json"
    _test_json(filepath, language="Portuguese")


def test_py_heideltime_pt_dilma():
    filepath = RESOURCES_PATH / "pt_dilma.json"
    _test_json(filepath, language="Portuguese")


def test_py_heideltime_en_boston_marathon():
    filepath = RESOURCES_PATH / "en_boston_marathon.json"
    _test_json(filepath, language="English")


def test_py_heideltime_en_neuroscience():
    filepath = RESOURCES_PATH / "en_neuroscience.json"
    _test_json(filepath, language="English")


def test_py_heideltime_en_haiti_earthquake():
    filepath = RESOURCES_PATH / "en_haiti_earthquake.json"
    _test_json(filepath, language="English")


def test_py_heideltime_en_london():
    filepath = RESOURCES_PATH / "en_london.json"
    _test_json(filepath, language="English")


def test_py_heideltime_en_london_options():
    filepath = RESOURCES_PATH / "en_london_options.json"
    _test_json(
        filepath,
        language="English",
        date_type="day",
        document_type='news',
        dct='1939-08-31'
    )


def test_py_heideltime_fr_helmut():
    filepath = RESOURCES_PATH / "fr_helmut.json"
    _test_json(filepath, language="French")
