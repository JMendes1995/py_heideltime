"""This script serves to write the configuration file that depends on the OS in which the script is runnning.
The conf.props file is required to run the Jav implementation of HeidelTime.
"""

import platform
from pathlib import Path


def write_config_props(library_path: Path) -> None:
    if platform.system() == "Windows":
        tagger_path = library_path / "Heideltime" / "TreeTaggerWindows"
    else:
        tagger_path = library_path / "Heideltime" / "TreeTaggerLinux"

    conf_template = (library_path / "config_props_template").open().read()
    conf_content = conf_template.replace("{path}", str(tagger_path))
    (library_path / "config.props").open("w").write(conf_content)
