from pathlib import Path

from py_heideltime.config import write_config_props


def test_write_config_props():
    path = Path(__file__).parent
    write_config_props(path)

    content = (path / "config.props").open().read()
    assert str(path.absolute()) in content
    (path / "config.props").unlink()
