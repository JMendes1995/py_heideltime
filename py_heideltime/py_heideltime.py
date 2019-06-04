import os
import xml.etree.ElementTree as ET
import codecs
import imp
import platform
import subprocess
import re

import time
import multiprocessing

def heideltime(text, language, document_type='news', document_creation_time='', date_granularity=''):
    full_path = ''
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
# Path to TreeTaggerLinux home directory
###################################
# Ensure there is no white space in path (try to escape white spaces)
treeTaggerHome = '''+full_path+'''
# This one is only necessary if you want to process chinese documents.
chineseTokenizerPath = SET ME IN CONFIG.PROPS! (e.g., /home/jannik/treetagger/chinese-tokenizer)
##################################
# paths to JVnTextPro model paths:
##################################
sent_model_path = SET ME IN CONFIG.PROPS! (e.g., /home/jannik/jvntextpro/models/jvnsensegmenter)
word_model_path = SET ME IN CONFIG.PROPS! (e.g., /home/jannik/jvntextpro/models/jvnsegmenter)
pos_model_path = SET ME IN CONFIG.PROPS! (e.g., /home/jannik/jvntextpro/models/jvnpostag/maxent)
#####################################################
# paths to Stanford POS Tagger model or config files:
#####################################################
model_path = SET ME IN CONFIG.PROPS! (e.g., /home/jannik/stanford-postagger-full-2014-01-04/models/arabic.tagger)
# leave this unset if you do not need one (e.g., /home/jannik/stanford-postagger-full-2014-01-04/tagger.config)
config_path =
########################################
## paths to hunpos and its tagger files:
########################################
hunpos_path = SET ME IN CONFIG.PROPS! (e.g., /home/jannik/hunpos)
hunpos_model_name = SET ME IN CONFIG.PROPS! (e.g., model.hunpos.mte5.defnpout)
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

    f = codecs.open("config.props", "w+", "utf-8")
    f.truncate()
    f.write(conf)
    f.close()
    num_files = create_txt_files(text)
    list_dates = exec_java_heideltime(num_files, path, full_path, language, document_type, document_creation_time, date_granularity)
    return list_dates


def create_txt_files(text):
    tests = text.split(". ")
    n = max(1, 100)
    merge_sentenses = [tests[i:i + n] for i in range(0, len(tests), n)]
    num_files = 0
    for i in range(len(merge_sentenses)):
        te = " ".join(merge_sentenses[i])
        text_file = codecs.open('text'+str(i)+'.txt', "w+", "utf-8")
        text_file.truncate()
        text_file.write(te)
        text_file.close()
        num_files = i
    return num_files


def exec_java_heideltime(file_number, path, full_path,language, document_type, document_creation_time, date_granularity):
    list_dates=[]
    match = re.findall('\d{4}[-]\d{2}[-]\d{2}', document_creation_time)

    if match == [] and document_creation_time != '':
        print('Bad document_creation_time format you must specify da date in YYYY-MM-DD format.')
    else:
        n=0
        while n <= file_number:
            if document_creation_time == '':
                java_command = 'java -jar ' + path + '/Heideltime/de.unihd.dbs.heideltime.standalone.jar  ' + document_type + ' -l ' + language + ' text'+str(n)+'.txt'
            else:
                java_command = 'java -jar ' + path + '/Heideltime/de.unihd.dbs.heideltime.standalone.jar  -dct ' +\
                               document_creation_time + ' -t ' + document_type + ' -l ' + language + ' text'+str(n)+'.txt'
            # run java heideltime standalone version to get all dates
            if platform.system() == 'Windows':
                myCmd = subprocess.check_output(java_command)
            else:
                myCmd = os.popen(java_command).read()

            # parsing the xml to get only the date value and the expression that originate the date

            from lxml import etree
            parser = etree.XMLParser(recover=True)
            root = etree.fromstring(myCmd, parser=parser)
            for i in range(len(root)):
                # insert in list the date value and the expression that originate the date
                if date_granularity != '':
                    if re.match('\w{4}[-]\w{2}[-]\w{2}', root[i].attrib['value']):
                        if date_granularity.lower() == 'year':
                            years = re.findall('\w{4}', root[i].attrib['value'])
                            list_dates.append((years[0], root[i].text))
                        elif date_granularity.lower() == 'month':
                            months = re.findall('\w{4}[-]\w{2}', root[i].attrib['value'])
                            list_dates.append((months[0], root[i].text))
                        elif date_granularity.lower() == 'day':
                            days = re.findall('\w{4}[-]\w{2}[-]\w{2}', root[i].attrib['value'])
                            list_dates.append((days[0], root[i].text))
                else:
                    list_dates.append((root[i].attrib['value'], root[i].text))
            n += 1
        # write error message for linux users to advertise that should give execute java heideltime
        if list_dates == [] and platform.system() == 'Linux':
            print('Sorry, maybe something went wrong.')
            print('Please check if the format of values of variables are like the documentation or')
            print('run this command to give execution privileges to execute java heideltime')
            print('sudo chmod 111 ' + full_path + '/bin/*')

    return list_dates
