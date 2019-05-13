# py_heideltime
This module has the intention to easily get dates for python.

The project are based in Java standalone Heideltime (https://github.com/HeidelTime/heideltime).

## How install py_heideltime
To use this module you must have java and perl installed.
```bash
pip install git+https://github.com/JMendes1995/py_heideltime.git
```

## How to use py_heideltime
```bash
from py_heideltime import heideltime

text = '''
The coup had two secret signals. The first was the airing at 10:55 p.m. of Paulo de Carvalho's "E Depois do Adeus" (Portugal's entry in the 1974 Eurovision Song Contest) on Emissores Associados de Lisboa, which alerted the rebel captains and soldiers to begin the coup. The second signal came on 25 April 1974 at 12:20 a.m., when Rádio Renascença broadcast "Grândola, Vila Morena" (a song by Zeca Afonso, an influential political folk musician and singer who was banned from Portuguese radio at the time). The MFA gave the signals to take over strategic points of power in the country.
'''
output = heideltime(text)
print(output)
#output
{0: [{'Date': '1974', 'Expression': '1974'}], 1: [{'Date': '1974-04-25', 'Expression': '25 April 1974'}], 2: [{'Date': '1974-04-25T12:20', 'Expression': '12:20 a.m.'}]}
```

### Python CLI -  Command Line Interface
``` bash
python cli.py --help

Options:
  -t, --text TEXT        insert text
  -i, --input_file TEXT  input text file
  --help                 Show this message and exit.
```

## Supported languages

This module are prepared to work with English, Portuguese, Spanish, Germany, Dutch, Italian, French. 


## Publications 
if you use py_heideltime cite the following work
 1. Strötgen, Gertz: Multilingual and Cross-domain Temporal Tagging. Language Resources and Evaluation, 2013
 2. Strötgen, Gertz: A Baseline Temporal Tagger for All Languages. EMNLP'15. pdf bibtex
 3. Kuzey, Strötgen, Setty, Weikum: Temponym Tagging: Temporal Scopes for Textual Phrases. TempWeb'16. 

