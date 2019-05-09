import os
from dateutil.parser import parse
import xml.etree.ElementTree as ET
from langdetect import detect
from py_heideltime.lang import languages
import codecs
import imp
import platform


def heideltime(text):
    full_path = ''
    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        path = imp.find_module('py_heideltime')[1]
        full_path = path + "/HeidelTime/TreeTaggerLinux"
        ch_permitions = 'chmod u+x '+full_path + '/bin/*'
        os.system(ch_permitions)

    else:
        path = imp.find_module('py_heideltime')[1]
        pp = path.replace('\\', '''\\\\''')
        full_path = str(pp) + '''\\\HeidelTime\\\TreeTaggerWindows'''
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
    list_dates = {}
    f = codecs.open("config.props", "w+", "utf-8")
    f.truncate()
    f.write(conf)
    f.close()

    text_file = codecs.open("text.txt", "w+", "utf-8")
    text_file.truncate()
    text_file.write(text)
    text_file.close()
    # language code detection
    lang_code = detect(text)

    # find in list of languages (from lang import languages) in order to get the language full name
    lang_name = 'English'
    for n_list_of_lang in range(len(languages)):
        if lang_code in languages[n_list_of_lang]:
            lang_name = languages[n_list_of_lang][1]

    # run java heideltime standalone version to get all dates
    myCmd = os.popen(
        'java -jar '+path+'/HeidelTime/de.unihd.dbs.heideltime.standalone.jar news -l ' + lang_name + ' text.txt').read()

    # parsing the xml to get only the date value and the expression that originate the date
    root = ET.fromstring(myCmd)
    count = 0
    for i in range(len(root)):
        try:
            # verify if the value is a date
            parse(root[i].attrib['value'])
            # insert in list the date value and the expression that originate the date
            list_dates[count] = [{'Date': root[i].attrib['value'], 'Expression' :root[i].text}]
            count += 1
        except:
            pass
    return list_dates
