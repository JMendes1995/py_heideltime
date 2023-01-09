import itertools
import os
import platform
import re
import tempfile
from pathlib import Path
from typing import List

import emoji

from py_heideltime.config import write_config_props

LIBRARY_PATH = Path(__file__).parent
HEIDELTIME_PATH = LIBRARY_PATH / "Heideltime" / "de.unihd.dbs.heideltime.standalone.jar"

# if not (LIBRARY_PATH / "config.props").exists():
#     write_config_props(LIBRARY_PATH)

LANGUAGES = [
    "english",
    "portuguese",
    "spanish",
    "german",
    "dutch",
    "italian",
    "french"
]

DATE_TYPES = [
    "full",
    "day",
    "month",
    "year"
]

DOC_TYPES = [
    "news",
    "narrative",
    "colloquial",
    "scientific"
]


def _validate_inputs(
        language: str,
        date_type: str,
        document_type: str
) -> None:
    """Check if the language, date, and document type are valid. If not, the function will raise a value error."""
    if language.lower() not in LANGUAGES:
        msg = f"Invalid language. Language should be within the following values: {LANGUAGES}"
        raise ValueError(msg)

    if date_type.lower() not in DATE_TYPES:
        msg = f"Invalid language. Language should be within the following values: {LANGUAGES}"
        raise ValueError(msg)

    if document_type.lower() not in DOC_TYPES:
        msg = f"Invalid document type. Language should be within the following values: {LANGUAGES}"
        raise ValueError(msg)


def py_heideltime(
        text: str,
        language: str,
        date_type: str = "full",
        document_type: str = "news",
        dct: str = None
):
    """HeidelTime temporal tagger."""
    write_config_props(Path())

    _validate_inputs(language, date_type, document_type)

    processed_text = process_text(text)

    # list with the files path to be processed by heideltime
    filepaths = create_text_files(processed_text, LIBRARY_PATH)

    dates_list = []
    new_text_list = []
    tagged_text_list = []
    heideltime_processing_list = []
    py_heideltime_text_normalization = []
    for filepath in filepaths:
        xml = exec_java_heideltime(
            filepath=filepath,
            language=language,
            document_type=document_type,
            dct=dct,
        )

        result = process_xml_document(xml, date_type)

        for d in result:
            dates_list.append(d[0])
            new_text_list.append(d[1])
            tagged_text_list.append(d[2])
            heideltime_processing_list.append(d[3]["heideltime_processing"])
            py_heideltime_text_normalization.append(d[3]["py_heideltime_text_normalization"])

    dates_results = list(itertools.chain.from_iterable(dates_list))
    new_text = "".join(new_text_list)
    tagged_text = "".join(tagged_text_list)

    # TODO: remove folder and files that were processed by heideltime
    return [dates_results, new_text, tagged_text]


def create_text_files(text: str, directory: Path) -> List:
    """Writes text files to be annotated by Java implementation of HeidelTime."""
    max_n_characters = 30_000
    n_characters = len(text)
    chunks = [text[i:i + max_n_characters] for i in range(0, n_characters, max_n_characters)]
    filepaths = []
    for chunk in chunks:
        temp_path = Path(tempfile.mkstemp(dir=directory)[1])
        temp_path.open("w").write(chunk)
        filepaths.append(temp_path)
    return filepaths


def exec_java_heideltime(
        filepath,
        language,
        document_type,
        dct=None,
):
    if dct is not None:
        match = re.findall(r"^\d{4}-\d{2}-\d{2}$", dct)
        if not match:
            raise ValueError("Please specify date in the following format: YYYY-MM-DD.")
        cmd = f"java -jar {HEIDELTIME_PATH} -dct {dct} -t {document_type} -l {language} {filepath}"
    else:
        cmd = f"java -jar {HEIDELTIME_PATH} -t {document_type} -l {language} {filepath}"

    if platform.system() == "Windows":
        import subprocess
        xml_doc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8")
    else:
        xml_doc = os.popen(cmd).read()

    return xml_doc


def process_xml_document(xml: str, date_type: str):
    # Find tags from java output
    # [time_ml_text] = re.findall(r"<TimeML>.*</TimeML>", xml_doc, re.DOTALL)
    time_ml_text = xml.split("<TimeML>")[1].split("</TimeML>")[0].strip("\n")
    list_of_tag_contents = re.findall("<TIMEX3(.*?)</TIMEX3>", str(xml))

    list_dates = []
    normalized_dates_list = []
    for i in range(len(list_of_tag_contents)):
        # normalized date
        normalized_dates = re.findall("value=\"(. *?)\"", list_of_tag_contents[i], re.IGNORECASE)
        # original fate
        original_dates = re.findall(">(.+)", list_of_tag_contents[i], re.IGNORECASE)
        # insert in list the date value and the expression that originate the date
        normalized_dates_list.append(normalized_dates[0])

        if date_type is not None:
            if date_type.lower() == "year":
                years = re.findall(r"\d{4}", normalized_dates[0])
                list_dates.append((years[0], original_dates[0]))
                if re.match(years[0] + "(.*?)", normalized_dates[0]):
                    normalized_dates_list[len(normalized_dates_list) - 1] = years[0]

            elif date_type.lower() == "month":
                months = re.findall(r"\d{4}-\d{2}", normalized_dates[0])
                list_dates.append((months[0], original_dates[0]))
                if re.match(months[0] + "(.*?)", normalized_dates[0]):
                    normalized_dates_list[len(normalized_dates_list) - 1] = months[0]

            elif date_type.lower() == "day":
                days = re.findall(r"\d{4}-\d{2}-\d{2}", normalized_dates[0])
                list_dates.append((days[0], original_dates[0]))
                if re.match(days[0] + "(.*?)", normalized_dates[0]):
                    normalized_dates_list[len(normalized_dates_list) - 1] = days[0]
        else:
            try:
                list_dates.append((normalized_dates[0], original_dates[0]))
            except:
                pass

    text_normalized = refactor_text(normalized_dates_list, list_of_tag_contents, time_ml_text)
    return list_dates, text_normalized, time_ml_text


def refactor_text(normalized_dates, ListOfTagContents, tagged_text):
    """Replace the TIMEX3 tags with the normalized dates in the tagged text."""
    for tag_content, date in zip(ListOfTagContents, normalized_dates):
        tagged_text = tagged_text.replace(f"<TIMEX3{tag_content}</TIMEX3>", f"<d>{date}</d>", 1)
    return tagged_text


def remove_emoji(text):
    return emoji.replace_emoji(text, replace="")


def text_has_emoji(text):
    if emoji.distinct_emoji_list(text):
        return True
    return False


def process_text(text):
    if text_has_emoji(text):
        return remove_emoji(text)
    else:
        return text
