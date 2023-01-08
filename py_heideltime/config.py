"""This script serves to write the configuration file that depends on the OS in which the script is runnning.
The conf.props file is required to run the Jav implementation of HeidelTime.
"""

import platform
from pathlib import Path

LIBRARY_PATH = Path(__file__).parent


def write_config_props(path: Path) -> None:
    if platform.system() == "Windows":
        tagger_path = path / "Heideltime" / "TreeTaggerWindows"
    else:
        tagger_path = path / "Heideltime" / "TreeTaggerLinux"

    conf_template = (LIBRARY_PATH / "config_props_template").open().read()
    conf_content = conf_template.replace("{path}", str(tagger_path.absolute()))
    (path / "config.props").open("w").write(conf_content)
