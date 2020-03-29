import os
import codecs
import imp
import platform
import subprocess
import re
from py_heideltime.validate_input import verify_temporal_tagger
import time


def py_heideltime(text, language='English', date_granularity='full', document_type='news',
                  document_creation_time='yyyy-mm-dd'):
    full_path = ''
    processed_text=pre_process_text(text)
    result = verify_temporal_tagger(language, date_granularity, document_type)
    if result == {}:
        print([])
        raise SystemExit

    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        path = imp.find_module('py_heideltime')[1]
        full_path = path + "/Heideltime/TreeTaggerLinux"
    else:
        path = imp.find_module('py_heideltime')[1]
        pp = path.replace('\\', '''\\\\''')
        full_path = str(pp) + '''\\\Heideltime\\\TreeTaggerWindows'''
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
    num_files = create_txt_files(processed_text)

    list_dates, new_text, tagged_text, ExecTimeDictionary = exec_java_heideltime(num_files, path, full_path, language, document_type,
                                                             document_creation_time, date_granularity)
    remove_files(num_files)
    return [list_dates, new_text, tagged_text, ExecTimeDictionary]


def create_txt_files(text):
    tests = text.split()
    n = max(1, 15000)
    merge_sentenses = [tests[i:i + n] for i in range(0, len(tests), n)]
    num_files = 0
    for i in range(len(merge_sentenses)):
        te = " ".join(merge_sentenses[i])
        with open('text' + str(i) + '.txt', 'w', encoding="utf8") as text_file:
            text_file.truncate()
            text_file.write(te)
            text_file.close()
        num_files = i
    return num_files


def exec_java_heideltime(file_number, path, full_path, language, document_type, document_creation_time,
                         date_granularity):
    list_dates = []
    nt = ''
    tt = ''
    ExecTimeDictionary = {}
    exec_time_date_extractor = 0
    exec_time_text_labeling = 0
    match = re.findall('^\d{4}[-]\d{2}[-]\d{2}$', document_creation_time)
    if match == [] and document_creation_time != 'yyyy-mm-dd':
        print('Please specify date in the following format: YYYY-MM-DD.')
        return {}
    else:
        n = 0
        while n <= file_number:
            normalized_dates_list = []
            extractor_start_time = time.time()
            if document_creation_time == 'yyyy-mm-dd':
                java_command = 'java -jar ' + path + '/Heideltime/de.unihd.dbs.heideltime.standalone.jar   ' + document_type + ' -l ' + language + ' text' + str(
                    n) + '.txt'
            else:
                java_command = 'java -jar ' + path + '/Heideltime/de.unihd.dbs.heideltime.standalone.jar  -dct ' + \
                               document_creation_time + ' -t ' + document_type + ' -l ' + language + ' text' + str(
                    n) + '.txt'
            # run java heideltime standalone version to get all dates

            from subprocess import check_output
            if platform.system() == 'Windows':
                import subprocess
                myCmd = subprocess.run(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8")
                striped_text = str(myCmd).split('\n')
                ListOfTagContents = re.findall("<TIMEX3(.*?)</TIMEX3>", str(myCmd))
            else:
                myCmd = os.popen(java_command).read()
                # Find tags from java output
                striped_text = str(myCmd).split('\n')
                ListOfTagContents = re.findall("<TIMEX3(.*?)</TIMEX3>", str(myCmd))

            # tagged text from java output
            tagged_text = str(striped_text[3])

            for i in range(len(ListOfTagContents)):
                # normalized date
                normalized_dates = re.findall('value="(.*?)"', ListOfTagContents[i], re.IGNORECASE)
                # original fate
                original_dates = re.findall('>(.+)', ListOfTagContents[i], re.IGNORECASE)
                # insert in list the date value and the expression that originate the date
                normalized_dates_list.append(normalized_dates[0])

                if date_granularity != 'full':
                    try:
                        if date_granularity.lower() == 'year':
                            years = re.findall('\d{4}', normalized_dates[0])
                            list_dates.append((years[0], original_dates[0]))
                            if re.match(years[0] + '(.*?)', normalized_dates[0]):
                                normalized_dates_list[len(normalized_dates_list) - 1] = years[0]

                        elif date_granularity.lower() == 'month':
                            months = re.findall('\d{4}[-]\d{2}', normalized_dates[0])
                            list_dates.append((months[0], original_dates[0]))
                            if re.match(months[0] + '(.*?)', normalized_dates[0]):
                                normalized_dates_list[len(normalized_dates_list) - 1] = months[0]

                        elif date_granularity.lower() == 'day':
                            days = re.findall('\d{4}[-]\d{2}[-]\d{2}', normalized_dates[0])
                            list_dates.append((days[0], original_dates[0]))
                            if re.match(days[0] + '(.*?)', normalized_dates[0]):
                                normalized_dates_list[len(normalized_dates_list) - 1] = days[0]

                    except:
                        pass
                else:
                    try:
                        list_dates.append((normalized_dates[0], original_dates[0]))
                    except:
                        pass
            tt_exec_time = (time.time() - extractor_start_time)
            exec_time_date_extractor += tt_exec_time

            labeling_start_time = time.time()
            n += 1
            new_text = refactor_text(normalized_dates_list, ListOfTagContents, tagged_text)
            nt += new_text
            tt += tagged_text

            label_text_exec_time = (time.time() - labeling_start_time)
            exec_time_text_labeling += label_text_exec_time

    ExecTimeDictionary['heideltime_processing'] = exec_time_date_extractor
    ExecTimeDictionary['py_heideltime_text_normalization'] = exec_time_text_labeling
    return list_dates, nt, tt, ExecTimeDictionary


def refactor_text(normalized_dates, ListOfTagContents, nt):
    for i in range(len(ListOfTagContents)):
        nt = re.sub('<TIMEX3' + ListOfTagContents[i] + '</TIMEX3>', '<d>' + normalized_dates[i] + '</d>', nt,
                    re.IGNORECASE)
    return nt


def remove_files(num_files):
    import os
    os.remove('config.props')
    i_files = 0
    while i_files <= num_files:
        os.remove('text' + str(i_files) + '.txt')
        i_files += 1


import emoji

def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(u'', text)

def text_has_emoji(text):
    for character in text:
        if character in emoji.UNICODE_EMOJI:
            return True
    return False


def pre_process_text(text):
    if text_has_emoji(text):
        return remove_emoji(text)
    else:
        return text

