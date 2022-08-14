import os
import codecs
import imp
import platform
import subprocess
import re
from py_heideltime.validate_input import verify_temporal_tagger
import time
from multiprocessing import Pool
from itertools import repeat
import multiprocessing
from itertools import chain
import tempfile
import shutil

def py_heideltime(text, language='English', date_granularity='full', document_type='news', document_creation_time='yyyy-mm-dd'):
    try:
        processed_text=pre_process_text(text)
        result = verify_temporal_tagger(language, date_granularity, document_type)
        if result == {}:
            print([])
            raise SystemExit

        path, full_path = get_Path()
        configProps(full_path)

        directory_name = tempfile.mkdtemp(dir = path) #folder where the text to be passed to heideltime will be stored
        listOfFiles = create_txt_files(processed_text, directory_name) #list with the files path to be processed by heideltime

        start_time = time.time( )

        result = []
        if len(listOfFiles) == 1:
            result_temp = exec_java_heideltime(listOfFiles[0], path, language, document_type, document_creation_time, date_granularity)
            result.append(result_temp)
        else:
            with Pool(processes=multiprocessing.cpu_count( )) as pool:
                result = pool.starmap(exec_java_heideltime,
                                                  zip(listOfFiles, repeat(path), repeat(language),
                                                      repeat(document_type), repeat(document_creation_time),repeat(date_granularity)))

        heideltime_processing_time = time.time( ) - start_time

        dates_list=[]
        new_text_list=[]
        tagged_text_list=[]
        heideltime_processing_list=[]
        py_heideltime_text_normalization=[]

        for d in result:
            dates_list.append(d[0])
            new_text_list.append(d[1])
            tagged_text_list.append(d[2])
            heideltime_processing_list.append(d[3]['heideltime_processing'])
            py_heideltime_text_normalization.append(d[3]['py_heideltime_text_normalization'])

        dates_results = list(chain.from_iterable(dates_list))
        new_text = ''.join(new_text_list)
        tagged_text = ''.join(tagged_text_list)
        ExecTimeDictionary={'heideltime_processing': heideltime_processing_time-sum(py_heideltime_text_normalization), 'py_heideltime_text_normalization': sum(py_heideltime_text_normalization)}
        if os.path.exists(directory_name):
            shutil.rmtree(directory_name) #remove folder and files that were processed by heideltime
        os.remove('config.props')   #remove config.props files
        return [dates_results, new_text, tagged_text, ExecTimeDictionary]
    except Exception as e:
        print("Error: " + str(e))

def create_txt_files(text, directory_name):
    chunkSize = 30000 #30000 chars
    listOfFiles = []

    if len(text) < chunkSize:
        temp = tempfile.NamedTemporaryFile(prefix="text_", dir = directory_name, delete=False)
        temp.write(text.encode('utf-8'))
        temp.close()
        listOfFiles.append(temp.name.replace(os.sep, '/'))
    else:   
        listOfChuncks = [text[i:i + chunkSize] for i in range(0, len(text), chunkSize)]
        for i in range(len(listOfChuncks)):
            temp = tempfile.NamedTemporaryFile(prefix="text_", dir = directory_name, delete=False)
            temp.write(listOfChuncks[i].encode('utf-8'))
            temp.close()
            listOfFiles.append(temp.name.replace(os.sep, '/'))

    return listOfFiles


def exec_java_heideltime(filename, path, language, document_type, document_creation_time, date_granularity):
    list_dates = []
    ExecTimeDictionary = {}
    match = re.findall('^\d{4}[-]\d{2}[-]\d{2}$', document_creation_time)
    if match == [] and document_creation_time != 'yyyy-mm-dd':
        print('Please specify date in the following format: YYYY-MM-DD.')
        return {}
    else:

        normalized_dates_list = []
        extractor_start_time = time.time()
        if document_creation_time == 'yyyy-mm-dd':
            java_command = 'java -jar ' + path + '/Heideltime/de.unihd.dbs.heideltime.standalone.jar ' + document_type + ' -l ' + language + ' ' + filename
        else:
            java_command = 'java -jar ' + path + '/Heideltime/de.unihd.dbs.heideltime.standalone.jar  -dct ' + \
                               document_creation_time + ' -t ' + document_type + ' -l ' + language + ' ' + filename
            # run java heideltime standalone version to get all dates

        # TimeML text from java output
        timeML_text = ""

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
        heideltime_processing_time = (time.time() - extractor_start_time)

        labeling_start_time = time.time()
        text_normalized = refactor_text(normalized_dates_list, ListOfTagContents, timeML_text)

        py_heideltime_text_normalization_time = (time.time() - labeling_start_time)

    ExecTimeDictionary['heideltime_processing'] = heideltime_processing_time
    ExecTimeDictionary['py_heideltime_text_normalization'] = py_heideltime_text_normalization_time

    return list_dates, text_normalized, timeML_text, ExecTimeDictionary


def refactor_text(normalized_dates, ListOfTagContents, tagged_text):
    for i in range(len(ListOfTagContents)):
        tagged_text = re.sub('<TIMEX3' + ListOfTagContents[i] + '</TIMEX3>', '<d>' + normalized_dates[i] + '</d>', tagged_text,
                             re.IGNORECASE)
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

import emoji
def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(u'', text)

def text_has_emoji(text):
    if  emoji.distinct_emoji_list(text):
            return True
    return False

def pre_process_text(text):
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