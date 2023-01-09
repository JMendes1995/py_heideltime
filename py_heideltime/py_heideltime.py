import imp
import multiprocessing
import os
import platform
import re
import shutil
import tempfile
import time
from itertools import repeat
from multiprocessing import Pool

import emoji


def heideltime(
        text,
        language="English",
        document_type="news",
        dct="yyyy-mm-dd"
):
    processed_text = process_text(text)

    library_path, tagger_path = get_Path()
    configProps(tagger_path)

    directory_name = tempfile.mkdtemp(dir=library_path)
    listOfFiles = create_txt_files(processed_text, directory_name)

    result = []
    if len(listOfFiles) == 1:
        result_temp = exec_java_heideltime(
            listOfFiles[0],
            library_path,
            language,
            document_type,
            dct,
        )
        result.append(result_temp)
    else:
        with Pool(processes=multiprocessing.cpu_count()) as pool:
            result = pool.starmap(exec_java_heideltime,
                                  zip(list_of_files, repeat(library_path), repeat(language),
                                      repeat(document_type), repeat(dct)))

    dates_list = []
    new_text_list = []
    tagged_text_list = []

    for d in result:
        dates_list += d[0]
        new_text_list.append(d[1])
        tagged_text_list.append(d[2])

    new_text = ''.join(new_text_list)
    tagged_text = ''.join(tagged_text_list)
    if os.path.exists(directory_name):
        shutil.rmtree(directory_name)  # remove folder and files that were processed by heideltime
    os.remove('config.props')  # remove config.props files
    return dates_list, new_text, tagged_text


def create_txt_files(text, directory_name):
    chunkSize = 30_000  # 30000 chars
    listOfFiles = []

    if len(text) < chunkSize:
        temp = tempfile.NamedTemporaryFile(prefix="text_", dir=directory_name, delete=False)
        temp.write(text.encode('utf-8'))
        temp.close()
        listOfFiles.append(temp.name.replace(os.sep, '/'))
    else:
        listOfChuncks = [text[i:i + chunkSize] for i in range(0, len(text), chunkSize)]
        for i in range(len(listOfChuncks)):
            temp = tempfile.NamedTemporaryFile(prefix="text_", dir=directory_name, delete=False)
            temp.write(listOfChuncks[i].encode('utf-8'))
            temp.close()
            listOfFiles.append(temp.name.replace(os.sep, '/'))

    return listOfFiles


def exec_java_heideltime(filename, path, language, document_type, dct):
    dates = []
    match = re.findall(r"^\d{4}-\d{2}-\d{2}$", dct)
    if match == [] and dct != "yyyy-mm-dd":
        print("Please specify date in the following format: YYYY-MM-DD.")
        return {}
    else:

        normalized_dates_list = []
        if dct == 'yyyy-mm-dd':
            java_command = 'java -jar ' + path + '/Heideltime/de.unihd.dbs.heideltime.standalone.jar ' + document_type + ' -l ' + language + ' ' + filename
        else:
            java_command = 'java -jar ' + path + '/Heideltime/de.unihd.dbs.heideltime.standalone.jar  -dct ' + \
                           dct + ' -t ' + document_type + ' -l ' + language + ' ' + filename
            # run java heideltime standalone version to get all dates

        # TimeML text from java output
        if platform.system() == 'Windows':
            import subprocess
            myCmd = subprocess.run(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8")
            timeML_text = str(myCmd).split('<TimeML>')[1].split("</TimeML>")[0].lstrip("\n").rstrip("\n")
            ListOfTagContents = re.findall("<TIMEX3(.*?)</TIMEX3>", str(myCmd))
        else:
            myCmd = os.popen(java_command).read()
            # Find tags from java output
            timeML_text = str(myCmd).split('<TimeML>')[1].split("</TimeML>")[0].lstrip("\n").rstrip("\n")
            ListOfTagContents = re.findall("<TIMEX3(.*?)</TIMEX3>", str(myCmd))

        for i in range(len(ListOfTagContents)):
            # normalized date
            normalized_dates = re.findall('value="(.*?)"', ListOfTagContents[i], re.IGNORECASE)
            # original fate
            original_dates = re.findall('>(.+)', ListOfTagContents[i], re.IGNORECASE)
            # insert in list the date value and the expression that originate the date
            normalized_dates_list.append(normalized_dates[0])

        normalized_dates = []
        for tag in tags:
            [normalized_date] = re.findall("value=\"(.*?)\"", tag, re.IGNORECASE)
            [original_date] = re.findall(">(.+)", tag)
            normalized_dates.append(normalized_date)
            dates.append((normalized_date, original_date))

        text_normalized = refactor_text(normalized_dates, tags, time_ml_text)
    return dates, text_normalized, time_ml_text


                except:
                    pass
            else:
                try:
                    list_dates.append((normalized_dates[0], original_dates[0]))
                except:
                    pass

        labeling_start_time = time.time()
        text_normalized = refactor_text(normalized_dates_list, ListOfTagContents, timeML_text)

    return list_dates, text_normalized, timeML_text


def refactor_text(normalized_dates, ListOfTagContents, tagged_text):
    """Replace the TIMEX3 tags with the normalized dates in the tagged text."""
    for tag_content, date in zip(ListOfTagContents, normalized_dates):
        tagged_text = tagged_text.replace(f"<TIMEX3{tag_content}</TIMEX3>", f"<d>{date}</d>", 1)
    return tagged_text


def get_Path():
    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        path = imp.find_module('py_heideltime')[1]
        full_path = path + "/Heideltime/TreeTaggerLinux"
    else:
        path = imp.find_module('py_heideltime')[1]
        pp = path.replace('\\', '''\\\\''')
        full_path = str(pp) + '''\\\Heideltime\\\TreeTaggerWindows'''
    return path, full_path


def remove_emoji(text):
    return emoji.replace_emoji(text, replace='')


def text_has_emoji(text):
    if emoji.distinct_emoji_list(text):
        return True
    return False


def process_text(text):
    if text_has_emoji(text):
        return remove_emoji(text)
    else:
        return text


def configProps(full_path):
    conf = '''
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
        treeTaggerHome = ''' + full_path + '''
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
        '''
    with open("config.props", "w+") as f:
        f.truncate()
        f.write(conf)
        f.close()
