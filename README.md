# py_heideltime
py_heideltime is a python wrapper for the multilingual temporal tagger HeidelTime.

For more information about this temporal tagger, please visit the Heideltime Java standalone version: https://github.com/HeidelTime/heideltime

This wrapper has been developed by Jorge Mendes under the supervision of [Professor Ricardo Campos](http://www.ccc.ipt.pt/~ricardo/) in the scope of the Final Project of the Computer Science degree at the [Polytechnic Institute of Tomar](http://portal2.ipt.pt/), Portugal.

Although there already exist some python models for Heideltime (in particular https://github.com/amineabdaoui/python-heideltime) all of them require a considerable intervention from the user side. In this project, we aim to overcome some of these limitations. Our aim was four-fold:

 - To provide a multi-platform (windows, Linux, Mac Os);
 - To make it user friendly not only in terms of installation but also in its usage;
 - To make it lightweight without compromising its behavior;
 - To give the user the chance to choose the granularity (e.g., year, month, etc) of the dates to be extracted.

## How to install py_heideltime
In order to use py_heideltime you must have [java JDK](https://www.oracle.com/technetwork/java/javase/downloads/index.html) and [perl](https://www.perl.org/get.html) installed in your machine for heideltime dependencies.
```bash
pip install git+https://github.com/JMendes1995/py_heideltime.git
```
##### Linux users
    If your user does not have permission executions on python lib folder, you should execute the following command:
    sudo chmod 111 /usr/local/lib/<YOUR PYTHON VERSION>/dist-packages/py_heideltime/HeidelTime/TreeTaggerLinux/bin/*
    
## How to use py_heideltime
``` bash
from py_heideltime import py_heideltime

text = '''
Thurs August 31st - News today that they are beginning to evacuate the London children tomorrow. Percy is a billeting officer. I can't see that they will be much safer here.
'''
```

#### _With the default parameters_
```` bash
py_heideltime(text, language='English')
````

###### Output
```` bash
[('XXXX-08-31', 'August 31st'), ('PRESENT_REF', 'today'), ('XXXX-XX-XX', 'tomorrow')]
````

#### _With all the parameters_
```` bash
py_heideltime(text, language='English', date_granularity="day", document_type='news', document_creation_time='1939-08-31')
````
###### Output
```` bash
[('1939-08-31', 'August 31st'), ('1939-08-31', 'today'), ('1939-09-01', 'tomorrow')] 
````


### Python CLI -  Command Line Interface
``` bash
py_heideltime --help

Usage_examples (make sure that the input parameters are within quotes):

  Default Parameters: py_heideltime -t "August 31st" -l "English"
  All the Parameters: py_heideltime -t "August 31st" -l "English" -dg "day" -dt "News" -dct "1939-08-31"

  Output: the output will be a list of temporal expressions (TE) in the format [(normalized TE; TE as it is found in the text),….] or an empty list [] if no temporal expression is found in the text.

Options:
  [partilally-required]: either specify a text or an input_file path.
  ----------------------------------------------------------------------------------------------------------------------------------
  -t, --text TEXT                       - Input text.
                                          Example: “August 31st”.

  -i, --input_file TEXT                 - Text file path.
                                          Example: “c:\text.txt”.


  [required]
  ----------------------------------------------------------------------------------------------------------------------------------
  -l, --language TEXT                   - Language of the text.
                                          Options:
                                                  - "English";
                                                  - "Portuguese";
                                                  - "Spanish";
                                                  - "Germany";
                                                  - "Dutch";
                                                  - "Italian";
                                                  - "French".

  [not required]
  -----------------------------------------------------------------------------------------------------------------------------------
  -dg, --date_granularity TEXT          - Date granularity
                                          Options:
                                                - "year" (means that for the date YYYY-MM-DD only the YYYY will be retrieved);
                                                - "month" (means that for the date YYYY-MM-DD only the YYYY-MM will be retrieved);
                                                - "day" - (default param. Means that for the date YYYY-MM-DD it will retrieve YYYY-MM-DD).

  -dt, --document_type TEXT             - Type of the document text.
                                          Options:
                                                - "News" for news-style documents - default param;
                                                - "Narrative" for narrative-style documents (e.g., Wikipedia articles);
                                                - "Colloquial" for English colloquial (e.g., Tweets and SMS);
                                                - "Scientific" for scientific articles (e.g., clinical trails).

  -dct, --document_creation_time TEXT   - Document creation date in the format YYYY-MM-DD. Taken into account when "News" or
                                          "Colloquial" texts are specified.
                                          Example: "2019-05-30".

  --help                                - Show this message and exit.

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
