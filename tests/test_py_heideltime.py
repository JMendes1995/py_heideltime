import json
from pathlib import Path

from py_heideltime import heideltime

RESOURCES_PATH = Path(__file__).parent / "resources"


def _test_json(
        filepath: Path,
        **kwargs
):
    content = json.load(filepath.open())
    timexs, normalized_text, time_ml = heideltime(text=content["text"], **kwargs)
    timexs = list(map(list, timexs))

    assert content["normalized_text"] in normalized_text
    assert content["time_ml"] in time_ml
    assert timexs == content["timexs"]


def test_heideltime_emoji():
    text = 'texto com emoji 😀'
    expected_score = []
    expected_time_ml = expected_normalized_text = 'texto com emoji '

    score, normalized_text, time_ml = heideltime(text=text, language="Portuguese")

    assert normalized_text == expected_normalized_text
    assert time_ml == expected_time_ml
    assert score == expected_score


def test_heideltime_long_text():
    filepath = RESOURCES_PATH / "long_text.json"
    _test_json(filepath, language="Portuguese")


def test_heideltime_pt_wikipedia_planeta():
    filepath = RESOURCES_PATH / "pt_wikipedia_planeta.json"
    _test_json(filepath, language="Portuguese")


def test_heideltime_pt_arquivo_jugular():
    filepath = RESOURCES_PATH / "pt_arquivo_jugular.json"
    _test_json(filepath, language="Portuguese")


def test_heideltime_pt_wikipedia_25_de_abril():
    filepath = RESOURCES_PATH / "pt_wikipedia_25_de_abril.json"
    _test_json(filepath, language="Portuguese")


def test_heideltime_pt_wikipedia_operacao_marques():
    filepath = RESOURCES_PATH / "pt_wikipedia_operacao_marques.json"
    _test_json(filepath, language="Portuguese")


def test_heideltime_pt_dilma():
    filepath = RESOURCES_PATH / "pt_dilma.json"
    _test_json(filepath, language="Portuguese")


def test_heideltime_en_boston_marathon():
    filepath = RESOURCES_PATH / "en_boston_marathon.json"
    _test_json(filepath, language="English")


def test_heideltime_en_neuroscience():
    filepath = RESOURCES_PATH / "en_neuroscience.json"
    _test_json(filepath, language="English")


def test_heideltime_en_haiti_earthquake():
    filepath = RESOURCES_PATH / "en_haiti_earthquake.json"
    _test_json(filepath, language="English")


def test_heideltime_en_london():
    filepath = RESOURCES_PATH / "en_london.json"
    _test_json(filepath, language="English")


def test_heideltime_en_london_options():
    filepath = RESOURCES_PATH / "en_london_options.json"
    _test_json(
        filepath,
        language="English",
        date_type="day",
        document_type='news',
        dct='1939-08-31'
    )


def test_heideltime_fr_helmut():
    filepath = RESOURCES_PATH / "fr_helmut.json"
    _test_json(filepath, language="French")
