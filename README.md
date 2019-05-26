# py_heideltime
py_heideltime is a python wrapper for the multilingual temporal tagger HeidelTime.

For more information about this temporal tagger, please visit the Heideltime Java standalone version: https://github.com/HeidelTime/heideltime

This wrapper has been developed by Jorge Mendes under the supervision of [Professor Ricardo Campos](http://www.ccc.ipt.pt/~ricardo/) in the scope of the Final Project of the Computer Science degree at the [Polytechnic Institute of Tomar](http://portal2.ipt.pt/), Portugal.

Although there already exist some python models for Heideltime (in particular https://github.com/amineabdaoui/python-heideltime) all of them require a considerable intervention from the user side. In this project, we aim to overcome some of these limitations. Our aim was four-fold:

 - To provide a multi-platform (windows, Linux, Mac Os);
 - To make it user friendly not only in terms of installation but also in its usage;
 - To make it lightweight without compromising its behavior;

## How to install py_heideltime
In order to use py_heideltime you must have [java JDK](https://www.oracle.com/technetwork/java/javase/downloads/index.html) and [perl](https://www.perl.org/get.html) installed in your machine for heideltime dependencies.
```bash
pip install git+https://github.com/JMendes1995/py_heideltime.git
```
##### Linux users
    If your user doesn’t has execution permitions on python lib folder, you should execute the following command:
    sudo chmod 111 /usr/local/lib/<YOUR PYTHON VERSION>/dist-packages/py_heideltime/HeidelTime/TreeTaggerLinux/bin/*
    
## How to use py_heideltime
``` bash
from py_heideltime import heideltime

text = '''
The coup had two secret signals. The first was the airing at 10:55 p.m. of Paulo de Carvalho's "E Depois do Adeus" (Portugal's entry in the 1974 Eurovision Song Contest) on Emissores Associados de Lisboa, which alerted the rebel captains and soldiers to begin the coup. The second signal came on 25 April 1974 at 12:20 a.m., when Rádio Renascença broadcast "Grândola, Vila Morena" (a song by Zeca Afonso, an influential political folk musician and singer who was banned from Portuguese radio at the time). The MFA gave the signals to take over strategic points of power in the country.
'''
# assuming default parameters
heideltime(text, language='English')

# with all the parameters
heideltime(text, language='English', document_type='news', document_creation_time='2019-05-24')
```
## Output
````bash
[('XXXX-XX-XXT22:55', '10:55 p.m.'), ('1974', '1974'), ('1974-04-25', '25 April 1974'), ('1974-04-25T12:20', '12:20 a.m.')]  
````
### Python CLI -  Command Line Interface
``` bash
py_heideltime --help

Options:
  -t, --text TEXT                 insert text
  -l, --language TEXT             insert language name  [required]
  -td, --document_type TEXT       Type of the document specified by <file>
                                  (options: News, Narrative, Colloquial,
                                  Scientific).
  -dct, --document_creation_time TEXT
                                  Creation date of document only valid format
                                  (YYYY-MM-DD).only will be considered if
                                  document type are News or colloquial.
  -i, --input_file TEXT           input text file
  --help                          Show this message and exit.
```

## Supported languages

This module is prepared to work with the following languages: English, Portuguese, Spanish, Germany, Dutch, Italian, French.

To use py_heideltime with other languages proceed as follows:
  
  - Download from [TreeTagger](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/) the parameter files
  - gunzip < Downloaded file >
  - Copy the extracted file to the module folder /py_heideltime/HeidelTime/TreeTagger< your system >/lib/


## Publications 

If you use HeidelTime (either through this package or another one) please cite the appropriate paper. In general, this would be:

Strötgen, Gertz: Multilingual and Cross-domain Temporal Tagging. Language Resources and Evaluation, 2013. [pdf](https://link.springer.com/article/10.1007%2Fs10579-012-9179-y) [bibtex](https://dbs.ifi.uni-heidelberg.de/files/Team/jannik/publications/stroetgen_bib.html#LREjournal2013)

 
Other related papers may be found here:

https://github.com/HeidelTime/heideltime#Publications

Please check [Time-Matters](https://github.com/LIAAD/Time-Matters) if you are interested in detecting the relevance (score) of dates in a text.
