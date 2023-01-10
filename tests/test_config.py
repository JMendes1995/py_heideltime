from pathlib import Path

from py_heideltime.config import _write_config_props


def test_write_config_props():
    tagger_path = Path(__file__).parent.parent / "py_heideltime" / "Heideltime" / "TreeTagger"
    _write_config_props()

    content = Path("config.props").open().read()
    assert str(tagger_path.absolute()) in content
    Path("config.props").unlink()
