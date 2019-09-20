# py_heideltime
py_heideltime is a python wrapper for the multilingual temporal tagger HeidelTime.

For more information about this temporal tagger, please visit the Heideltime Java standalone version: https://github.com/HeidelTime/heideltime

This wrapper has been developed by Jorge Mendes under the supervision of [Professor Ricardo Campos](http://www.ccc.ipt.pt/~ricardo/) in the scope of the Final Project of the Computer Science degree at the [Polytechnic Institute of Tomar](http://portal2.ipt.pt/), Portugal.

Although there already exist some python packages for Heideltime (in particular https://github.com/amineabdaoui/python-heideltime) all of them require a considerable intervention from the user side. In this project, we aim to overcome some of these limitations. Our aim was six-fold:

 - To provide a multi-platform (windows, Linux, Mac Os);
 - To make it user-friendly not only in terms of installation but also in its usage;
 - To make it lightweight without compromising its behavior;
 - To give the user the chance to choose the granularity (e.g., year, month, etc) of the dates to be extracted;
 - To retrieve to the user a normalized version of the text (where each temporal expression is replaced by the normalized Heideltime version); and
 - To retrieve a Time-ML annotated version of the text (as done in the Heideltime demo).

## How to install py_heideltime
```bash
pip install git+https://github.com/JMendes1995/py_heideltime.git
```
In order to use py_heideltime you must have java JDK and perl installed in your machine for heideltime dependencies.

##### Windows users
To install java JDK begin by downloading it [here](https://www.oracle.com/technetwork/java/javase/downloads/index.html). Once it is installed don't forget to add the path to the environment variables. On `user variables for Administrator` add the `JAVA_HOME` as the `Variable name:`, and the path (e.g., `C:\Program Files\Java\jdk-12.0.2\bin`) as the Variable value. Then on `System variables` edit the `Path` variable and add (e.g., `;C:\Program Files\Java\jdk-12.0.2\bin`) at the end of the `variable value`.

For Perl we recomment you to download and install the following [distribution](http://strawberryperl.com/). Once it is installed don't forget to restart your PC.

Note that perl doesn't need to be installed if you are using Anaconda instead of pure Python distribution.

##### Linux users
Perl usually comes with Linux, thus you don't need to install it.

To install JAVA:
sudo apt install default-jdk

In addition, if your user does not have permission executions on python lib folder, you should execute the following command:
sudo chmod 111 /usr/local/lib/<YOUR PYTHON VERSION>/dist-packages/py_heideltime/HeidelTime/TreeTaggerLinux/bin/*
    
## How to use py_heideltime
``` bash
from py_heideltime import py_heideltime

text = '''
Thurs August 31st - News today that they are beginning to evacuate the London children tomorrow. Percy is a billeting officer. I can't see that they will be much safer here.
'''
```

#### _With the default parameters_
Default language is "English" and document_type is "news" which means that having:

```` bash
results = py_heideltime(text)
````

or:

```` bash
results = py_heideltime(text, language='English',  document_type='news')
````
is exactly the same thing and produces the same results.

###### Output
The output will be a list of 4 elements or an empty list [] if no temporal expression is found in the text. The four elements are:

- a list of tuples with two positions (e.g., ('XXXX-08-31', 'August 31st')). The first one is the detected temporal expression normalized by heideltime. The second is the temporal expression as it was found in the text;
- a normalized version of the text, where each temporal expression is replaced by its normalized heideltime counterpart;
- a TimeML-annotated version of the text.
- the execution time of the algorithm, divided into `heideltime_processing` (i.e., the time spent by the heideltime algorithm in extracting temporal expressions) and `text_normalization` (the time spent by the program in labelling the temporal expressions found in the text with a tag <d>).

```` bash
TempExpressions = results[0]
TempExpressions
````
```` bash
[('XXXX-08-31', 'August 31st'),
 ('PRESENT_REF', 'today'),
 ('XXXX-XX-XX', 'tomorrow')]
````

```` bash
TextNormalized = results[1]
TextNormalized
````
```` bash
'Thurs XXXX-08-31 - News PRESENT_REF that they are beginning to evacuate the London children XXXX-XX-XX. Percy is a billeting officer. I can't see that they will be much safer here.'
````

```` bash
TimeML = results[2]
TimeML
````
```` bash
'Thurs <TIMEX3 tid="t2" type="DATE" value="XXXX-08-31">August 31st</TIMEX3> - News <TIMEX3 tid="t3" type="DATE" value="PRESENT_REF">today</TIMEX3> that they are beginning to evacuate the London children <TIMEX3 tid="t4" type="DATE" value="XXXX-XX-XX">tomorrow</TIMEX3>. Percy is a billeting officer. I can\'t see that they will be much safer here.'
````

```` bash
ExecutionTime = results[3]
ExecutionTime
````
```` bash
{'heideltime_processing': 4.341801404953003, 'py_heideltime_text_normalization': 0.0}
````

#### _Optional parameters_
Besides running py_heideltime with the default parameters, users can also specify more advanced options. These are:  
- `date granularity`: <b>"full"</b> (Highest possible granularity detected will be retrieved); <b>"year"</b> (YYYY will be retrieved); <b>"month"</b> (YYYY-MM will be retrieved); <b>"day"</b> (YYYY-MM-DD will be retrieved)
- `document type` <b>"news"</b> (news-style documents); <b>"narrative"</b> (narrative-style documents (e.g., Wikipedia articles)); <b>"colloquial"</b> (English colloquial (e.g., Tweets and SMS)); <b>"scientific"</b> (scientific articles (e.g., clinical trails))
- `document creation time`: in the format <b>YYYY-MM-DD</b>

```` bash
results = py_heideltime(text, language='English', date_granularity="day", document_type='news', document_creation_time='1939-08-31')
````

###### Output
The output follows the same patterns as described above.


```` bash
TempExpressions = results[0]
TempExpressions
````
```` bash
[('1939-08-31', 'August 31st'),
 ('1939-08-31', 'today'),
 ('1939-09-01', 'tomorrow')]
````

```` bash
TextNormalized = results[1]
TextNormalized
````
```` bash
'Thurs 1939-08-31 - News 1939-08-31 that they are beginning to evacuate the London children 1939-09-01. Percy is a billeting officer. I can't see that they will be much safer here.'
````

```` bash
TimeML = results[2]
TimeML
````
```` bash
'Thurs <TIMEX3 tid="t2" type="DATE" value="1939-08-31">August 31st</TIMEX3> - News <TIMEX3 tid="t3" type="DATE" value="1939-08-31">today</TIMEX3> that they are beginning to evacuate the London children <TIMEX3 tid="t4" type="DATE" value="1939-09-01">tomorrow</TIMEX3>. Percy is a billeting officer. I can\'t see that they will be much safer here.'
````

```` bash
ExecutionTime = results[3]
ExecutionTime
````
```` bash
{'heideltime_processing': 4.341801404953003, 'text_normalization': 0.0}
````

### Python_CLI
#### Help
``` bash
py_heideltime --help
```
#### Usage Examples
Make sure that the input parameters are within quotes.

Default Parameters:
``` bash
py_heideltime -t "August 31st"
```

All the Parameters:
``` bash
py_heideltime -t "August 31st" -l "English" -dg "full" -dt "News" -dct "1939-08-31"
```

#### Options
``` bash
  [required]: either specify a text or an input_file path.
  ----------------------------------------------------------------------------------------------------------------------------------
  -t, --text                        - Input text.
                                      Example: “August 31st”.

  -i, --input_file                  - Text file path.
                                      Example: “c:\text.txt”.

```

``` bash
  [required]
  ----------------------------------------------------------------------------------------------------------------------------------
  -l, --language                    - Language of the text.
                                      Default: "English"
                                      Options:
                                              "English";
                                              "Portuguese";
                                              "Spanish";
                                              "Germany";
                                              "Dutch";
                                              "Italian";
                                              "French".
```

``` bash
  [not required]
  -----------------------------------------------------------------------------------------------------------------------------------
  -dg, --date_granularity           - Date granularity
                                      Default: "full" 
                                      Options:
                                              "full": means that all types of granularity will be retrieved, from the coarsest to 
                                                      the finest-granularity.
                                              "day": means that for the date YYYY-MM-DD-HH:MM:SS it will retrieve YYYY-MM-DD;
                                              "month": means that for the date YYYY-MM-DD-HH:MM:SS only the YYYY-MM will be retrieved;
                                              "year": means that for the date YYYY-MM-DD-HH:MM:SS only the YYYY will be retrieved;

  -dt, --document_type             - Type of the document text.
                                     Default: "News", 
                                     Options:
                                             "News": for news-style documents - default param;
                                             "Narrative": for narrative-style documents (e.g., Wikipedia articles);
                                             "Colloquial": for English colloquial (e.g., Tweets and SMS);
                                             "Scientific": for scientific articles (e.g., clinical trails).

  -dct, --document_creation_time   - Document creation date in the format YYYY-MM-DD. Taken into account when "News" or
                                     "Colloquial" texts are specified.
                                      Example: "2019-05-30".

  --help                           - Show this message and exit.

```

## Supported languages

This module is prepared to work with the following languages: English, Portuguese, Spanish, Germany, Dutch, Italian, French.

To use py_heideltime with other languages proceed as follows:
  
  - Download from [TreeTagger](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/) the parameter files
  - gunzip < Downloaded file >
  - Copy the extracted file to the module folder /py_heideltime/HeidelTime/TreeTagger< your system >/lib/

## Python Notebook 
We highly recommend you to use this [python notebook](notebook-py-heldeltime.ipynb) if you are interested in playing with py_heideltime.

## Related Projects

Please check [py_rule_based](https://github.com/JMendes1995/py_rule_based) if you are interested in extracting dates by means of a rule-based model solution.

Please check [Time-Matters](https://github.com/LIAAD/Time-Matters) if you are interested in detecting the relevance (score) of dates in a text.

## Publications 

If you use HeidelTime (either through this package or another one) please cite the appropriate paper. In general, this would be:

Strötgen, Gertz: Multilingual and Cross-domain Temporal Tagging. Language Resources and Evaluation, 2013. [pdf](https://link.springer.com/article/10.1007%2Fs10579-012-9179-y) [bibtex](https://dbs.ifi.uni-heidelberg.de/files/Team/jannik/publications/stroetgen_bib.html#LREjournal2013)

 
Other related papers may be found here:

https://github.com/HeidelTime/heideltime#Publications
