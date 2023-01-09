import multiprocessing
import os
import platform
import re
import shutil
import tempfile
from itertools import repeat
from multiprocessing import Pool
from pathlib import Path

import emoji

LIBRARY_PATH = Path(__file__).parent
if platform.system() == "Windows":
    TAGGER_PATH = LIBRARY_PATH / "Heideltime" / "TreeTaggerWindows"
else:
    TAGGER_PATH = LIBRARY_PATH / "Heideltime" / "TreeTaggerLinux"
HEIDELTIME_PATH = LIBRARY_PATH / "Heideltime" / "de.unihd.dbs.heideltime.standalone.jar"


def heideltime(
        text,
        language="English",
        document_type="news",
        dct=None
):
    processed_text = process_text(text)

    config_props()

    directory_name = tempfile.mkdtemp(dir=LIBRARY_PATH)
    list_of_files = create_txt_files(processed_text, directory_name)

    if len(list_of_files) == 1:
        result = [exec_java_heideltime(
            list_of_files[0],
            language,
            document_type,
            dct,
        )]
    else:
        with Pool(processes=multiprocessing.cpu_count()) as pool:
            result = pool.starmap(
                exec_java_heideltime,
                zip(list_of_files, repeat(language), repeat(document_type), repeat(dct))
            )

    dates_list = []
    new_text_list = []
    tagged_text_list = []

    for d in result:
        dates_list += d[0]
        new_text_list.append(d[1])
        tagged_text_list.append(d[2])

    new_text = "".join(new_text_list)
    tagged_text = "".join(tagged_text_list)
    if os.path.exists(directory_name):
        shutil.rmtree(directory_name)  # remove folder and files that were processed by heideltime
    os.remove("config.props")  # remove config.props files
    return dates_list, new_text, tagged_text


def create_txt_files(text, directory_name):
    chunk_size = 30_000  # 30000 chars
    list_of_files = []

    if len(text) < chunk_size:
        temp = tempfile.NamedTemporaryFile(prefix="text_", dir=directory_name, delete=False)
        temp.write(text.encode("utf-8"))
        temp.close()
        list_of_files.append(temp.name.replace(os.sep, "/"))
    else:
        list_of_chuncks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        for i in range(len(list_of_chuncks)):
            temp = tempfile.NamedTemporaryFile(prefix="text_", dir=directory_name, delete=False)
            temp.write(list_of_chuncks[i].encode("utf-8"))
            temp.close()
            list_of_files.append(temp.name.replace(os.sep, "/"))

    return list_of_files


def exec_java_heideltime(filename, language, document_type, dct):
    dates = []
    if dct is not None:
        match = re.findall(r"^\d{4}-\d{2}-\d{2}$", dct)
        if not match:
            raise ValueError("Please specify date in the following format: YYYY-MM-DD.")
        java_cmd = f"java -jar {HEIDELTIME_PATH} -dct {dct} -t {document_type} -l {language} {filename}"
    else:
        java_cmd = f"java -jar {HEIDELTIME_PATH} {document_type} -l {language} {filename}"

    # TimeML text from java output
    if platform.system() == "Windows":
        import subprocess
        xml_doc = subprocess.run(java_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8")
    else:
        xml_doc = os.popen(java_cmd).read()

    # Find tags from java output
    time_ml_text = str(xml_doc).split("<TimeML>")[1].split("</TimeML>")[0].strip("\n")
    tags = re.findall("<TIMEX3(.*?)</TIMEX3>", str(xml_doc))

    normalized_dates = []
    for tag in tags:
        [normalized_date] = re.findall("value=\"(.*?)\"", tag, re.IGNORECASE)
        [original_date] = re.findall(">(.+)", tag)
        normalized_dates.append(normalized_date)
        dates.append((normalized_date, original_date))

    text_normalized = refactor_text(normalized_dates, tags, time_ml_text)
    return dates, text_normalized, time_ml_text


def refactor_text(normalized_dates, tags, tagged_text):
    """Replace the TIMEX3 tags with the normalized dates in the tagged text."""
    for tag_content, date in zip(tags, normalized_dates):
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


def config_props():
    conf = f"""
        ################################
        ##           MAIN             ##
        ################################
        # Consideration of different timex3-types
        # Date
        considerDate = true
        # Duration
        considerDuration = true
        # Set
        considerSet = true
        # Time
        considerTime = true
        # Temponyms (make sure you know what you do if you set this to "true")
        considerTemponym = false
        ###################################
        # Path to TreeTagger home directory
        ###################################
        # Ensure there is no white space in path (try to escape white spaces)
        treeTaggerHome = {str(TAGGER_PATH.absolute())}
        # This one is only necessary if you want to process chinese documents.
        chineseTokenizerPath = SET ME IN CONFIG.PROPS! (e.g., /home/jannik/treetagger/chinese-tokenizer)
        config_path =
        # DO NOT CHANGE THE FOLLOWING
        ################################
        # Relative path of type system in HeidelTime home directory
        typeSystemHome = desc/type/HeidelTime_TypeSystem.xml
        # Relative path of dkpro type system in HeidelTime home directory
        typeSystemHome_DKPro = desc/type/DKPro_TypeSystem.xml
        # Name of uima-context variables...
        # ...for date-consideration
        uimaVarDate = Date
        # ...for duration-consideration
        uimaVarDuration = Duration
        # ...for language
        uimaVarLanguage = Language
        # ...for set-consideration
        uimaVarSet = Set
        # ...for time-consideration
        uimaVarTime = Time
        # ...for temponym-consideration
        uimaVarTemponym = Temponym
        # ...for type to process
        uimaVarTypeToProcess = Type
        """
    with open("config.props", "w+") as f:
        f.truncate()
        f.write(conf)
        f.close()
