import multiprocessing
import platform
import re
import tempfile
from itertools import repeat
from pathlib import Path
from typing import List

from py_heideltime.config import _write_config_props
from py_heideltime.meta import LANGUAGES, DOC_TYPES
from py_heideltime.utils import process_text, execute_command

LIBRARY_PATH = Path(__file__).parent
if platform.system() == "Windows":
    TAGGER_PATH = LIBRARY_PATH / "Heideltime" / "TreeTaggerWindows"
else:
    TAGGER_PATH = LIBRARY_PATH / "Heideltime" / "TreeTaggerLinux"
HEIDELTIME_JAR_PATH = LIBRARY_PATH / "Heideltime" / "de.unihd.dbs.heideltime.standalone.jar"


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
        filepaths = _create_text_files(processed_text, tempdir)

        processes = multiprocessing.cpu_count()
        with multiprocessing.Pool(processes=processes) as pool:
            inputs_ = zip(filepaths, repeat(language), repeat(document_type), repeat(dct))
            tml_docs = pool.starmap(
                _exec_java_heideltime,
                inputs_
            )

        tml_content = "".join(
            re.findall(r"<TimeML>(.*)</TimeML>", tml_doc, re.DOTALL)[0].strip("\n")
            for tml_doc in tml_docs
        )

        timexs = _get_timexs(tml_content)

    Path("config.props").unlink()
    return timexs


def _create_text_files(text: str, dir_path: Path) -> List:
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
        filename: str,
        language: str,
        document_type: str,
        dct: str
) -> str:
    """Execute Java implementation of HeidelTime."""

    if dct is not None:
        match = re.findall(r"^\d{4}-\d{2}-\d{2}$", dct)
        if not match:
            raise ValueError("Please specify date in the following format: YYYY-MM-DD.")
        java_cmd = f"java -jar {HEIDELTIME_JAR_PATH} -dct {dct} -t {document_type} -l {language} {filename}"
    else:
        java_cmd = f"java -jar {HEIDELTIME_JAR_PATH} {document_type} -l {language} {filename}"

    time_ml = execute_command(java_cmd)  # TimeML text from java output

    return time_ml


def _get_timexs(time_ml):
    # Find tags from java output
    tags = re.findall("<TIMEX3 (.*?)>(.*?)</TIMEX3>", time_ml)

    # Get timexs with attributes.
    timexs = []
    for attribs, text in tags:
        timex = {"text": text}
        for attrib in attribs.split():
            key, value = attrib.split("=")
            value = value.strip("\"")
            timex[key] = value
        timexs.append(timex)

    # Add spans to timexs.
    text_blocks = re.split("<TIMEX3.*?>(.*?)</TIMEX3>", time_ml)
    running_span = 0
    timexs_with_spans = []
    if not timexs:
        return timexs_with_spans

    else:
        timex = timexs.pop(0)
        for block in text_blocks:
            if block == timex["text"]:
                timex["span"] = [running_span, running_span + len(block)]
                timexs_with_spans.append(timex)
                if timexs:
                    timex = timexs.pop(0)
                else:
                    break
            running_span += len(block)

    return timexs_with_spans
