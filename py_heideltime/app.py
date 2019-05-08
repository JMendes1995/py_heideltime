import os
from dateutil.parser import parse
import xml.etree.ElementTree as ET
from langdetect import detect
from lang import languages
import codecs

if __name__ == "__main__":
     text = '''
O movimento confiou a direção do País à Junta de Salvação Nacional, que assumiu os poderes dos órgãos do Estado.[13] A 15 de maio de 1974, o General António de Spínola foi nomeado Presidente da República. O cargo de primeiro-ministro seria atribuído a Adelino da Palma Carlos.[14] Seguiu-se um período de grande agitação social, política e militar conhecido como o PREC (Processo Revolucionário Em Curso), marcado por manifestações, ocupações, governos provisórios, nacionalizações[15] e confrontos militares que terminaram com o 25 de novembro de 1975.[16][17][18]
Estabilizada a conjuntura política, prosseguiram os trabalhos da Assembleia Constituinte para a nova constituição democrática, que entrou em vigor no dia 25 de abril de 1976, o mesmo dia das primeiras eleições legislativas da nova República. Na sequência destes eventos foi instituído em Portugal um feriado nacional no dia 25 de abril, denominado como "Dia da Liberdade". 
'''
# insert the input text on file

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
     myCmd = os.popen('java -jar HeidelTime/de.unihd.dbs.heideltime.standalone.jar news -l ' + lang_name + ' text.txt').read()

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
     print(list_dates)

     # replace in the text the expression to value
     new_text = text
     for ct in range(len(list_dates)):
          new_text = new_text.replace(list_dates[ct][1], list_dates[ct][0])
     print(text)
     print('\n')
     print(new_text)




