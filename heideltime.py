import os
from dateutil.parser import parse
import xml.etree.ElementTree as ET
from langdetect import detect
from py_heideltime.lang import languages
import codecs


def heideltime(text):

    list_dates = {}
    f = codecs.open("text.txt", "w+", "utf-8")
    f.truncate()
    f.write(text)
    f.close()

    # language code detection
    lang_code = detect(text)

    # find in list of languages (from lang import languages) in order to get the language full name
    lang_name = 'English'
    for n_list_of_lang in range(len(languages)):
        if lang_code in languages[n_list_of_lang]:
            lang_name = languages[n_list_of_lang][1]

    # run java heideltime standalone version to get all dates
    myCmd = os.popen(
        'java -jar py_heideltime/HeidelTime/de.unihd.dbs.heideltime.standalone.jar news -l ' + lang_name + ' text.txt').read()

    # parsing the xml to get only the date value and the expression that originate the date
    root = ET.fromstring(myCmd)
    count = 0
    for i in range(len(root)):
        try:
            # verify if the value is a date
            parse(root[i].attrib['value'])
            # insert in list the date value and the expression that originate the date
            list_dates[count] = [root[i].attrib['value'], root[i].text]
            count += 1
        except:
            pass
    return list_dates
