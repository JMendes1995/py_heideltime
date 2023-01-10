import multiprocessing
import os
import platform
import re
import tempfile
from itertools import repeat
from pathlib import Path
from typing import List, Tuple

from py_heideltime.config import _write_config_props
from py_heideltime.utils import process_text, execute_command

LIBRARY_PATH = Path(__file__).parent
if platform.system() == "Windows":
    TAGGER_PATH = LIBRARY_PATH / "Heideltime" / "TreeTaggerWindows"
else:
    TAGGER_PATH = LIBRARY_PATH / "Heideltime" / "TreeTaggerLinux"
HEIDELTIME_JAR_PATH = LIBRARY_PATH / "Heideltime" / "de.unihd.dbs.heideltime.standalone.jar"

LANGUAGES = [
    "english",
    "portuguese",
    "spanish",
    "german",
    "dutch",
    "italian",
    "french"
]

DOC_TYPES = [
    "news",
    "narrative",
    "colloquial",
    "scientific"
]


def _validate_inputs(
        language: str,
        document_type: str
) -> None:
    """Check if the language and document type are valid. If not, the function will raise a value error."""
    if language.lower() not in LANGUAGES:
        msg = f"Invalid language. Language should be within the following values: {LANGUAGES}"
        raise ValueError(msg)

    if document_type.lower() not in DOC_TYPES:
        msg = f"Invalid document type. Language should be within the following values: {LANGUAGES}"
        raise ValueError(msg)


def heideltime(
        text: str,
        language: str = "english",
        document_type: str = "news",
        dct: str = None
):
    """Run HeidelTime temporal tagger."""
    _validate_inputs(language, document_type)
    _write_config_props()

    with tempfile.TemporaryDirectory(dir=LIBRARY_PATH) as tempdir:
        processed_text = process_text(text)
        filepaths = create_text_files(processed_text, tempdir)

        processes = multiprocessing.cpu_count()
        with multiprocessing.Pool(processes=processes) as pool:
            inputs_ = zip(filepaths, repeat(language), repeat(document_type), repeat(dct))
            annotations = pool.starmap(
                _exec_java_heideltime,
                inputs_
            )

        dates = []
        text_normalized, time_ml_text = "", ""
        for annotation in annotations:
            dates += annotation[0]
            text_normalized += annotation[1]
            time_ml_text += annotation[2]

    os.remove("config.props")  # remove config.props files
    return dates, text_normalized, time_ml_text


def create_text_files(text: str, dir_path: Path) -> List:
    """Writes text files to be annotated by Java implementation of HeidelTime."""
    max_n_characters = 30_000
    n_characters = len(text)
    chunks = [text[i:i + max_n_characters] for i in range(0, n_characters, max_n_characters)]

    filepaths = []
    for chunk in chunks:
        temp = tempfile.NamedTemporaryFile(dir=dir_path, delete=False)
        temp.write(chunk.encode("utf-8"))
        temp.close()
        filepaths.append(Path(temp.name))
    return filepaths


def _exec_java_heideltime(
        filename: Path,
        language: str,
        document_type: str,
        dct: str
) -> Tuple:
    """Execute Java implementation of HeidelTime."""

    dates = []
    if dct is not None:
        match = re.findall(r"^\d{4}-\d{2}-\d{2}$", dct)
        if not match:
            raise ValueError("Please specify date in the following format: YYYY-MM-DD.")
        java_cmd = f"java -jar {HEIDELTIME_JAR_PATH} -dct {dct} -t {document_type} -l {language} {filename}"
    else:
        java_cmd = f"java -jar {HEIDELTIME_JAR_PATH} {document_type} -l {language} {filename}"

    time_ml = execute_command(java_cmd)  # TimeML text from java output

    # Find tags from java output
    time_ml_text = str(time_ml).split("<TimeML>")[1].split("</TimeML>")[0].strip("\n")
    tags = re.findall("<TIMEX3(.*?)</TIMEX3>", str(time_ml))

    normalized_dates = []
    for tag in tags:
        [normalized_date] = re.findall("value=\"(.*?)\"", tag, re.IGNORECASE)
        [original_date] = re.findall(">(.+)", tag)
        normalized_dates.append(normalized_date)
        dates.append((normalized_date, original_date))

    text_normalized = refactor_text(normalized_dates, tags, time_ml_text)
    return dates, text_normalized, time_ml_text


def refactor_text(
        normalized_dates: List[str],
        tags: List[str],
        tagged_text: str
) -> str:
    """Replace the TIMEX3 tags with the normalized dates in the tagged text."""
    for tag_content, date in zip(tags, normalized_dates):
        tagged_text = tagged_text.replace(f"<TIMEX3{tag_content}</TIMEX3>", f"<d>{date}</d>", 1)
    return tagged_text
