# Python HeidelTime
`py_heideltime` is a python wrapper for the multilingual temporal tagger HeidelTime originally developed by [Jorge Mendes](https://github.com/JMendes1995/py_heideltime) and [Ricardo Campos](http://www.ccc.ipt.pt/~ricardo/). This repo is a gross simplification of the original work that reduces the interface and the outputs of the `heideltime` function. Please do checkout the original repo which provides a much more comprehensive overview of the library.   


### Installation

``` bash
pip install git+https://github.com/JMendes1995/py_heideltime.git
```

### Install External Resources
In order to use py_heideltime you must have java JDK and perl installed in your machine for heideltime dependencies.

##### Windows users
To install java JDK begin by downloading it [here](https://www.oracle.com/technetwork/java/javase/downloads/index.html). Once it is installed don't forget to add the path to the environment variables. On `user variables for Administrator` add the `JAVA_HOME` as the `Variable name:`, and the path (e.g., `C:\Program Files\Java\jdk-12.0.2\bin`) as the Variable value. Then on `System variables` edit the `Path` variable and add (e.g., `;C:\Program Files\Java\jdk-12.0.2\bin`) at the end of the `variable value`.

For Perl, we recommend to download and install the following [distribution](http://strawberryperl.com/). Once it is installed don't forget to restart your PC. Note that perl doesn't need to be installed if you are using Anaconda instead of pure Python distribution.

##### Linux users
Perl usually comes with Linux, thus you don't need to install it.

To install `JAVA`:
```bash
sudo apt install default-jdk
```
In addition, if your user does not have permission executions on python lib folder, you should execute the following command:
```bash
sudo chmod 111 /usr/local/lib/<YOUR PYTHON VERSION>/dist-packages/py_heideltime/HeidelTime/TreeTaggerLinux/bin/*
```

#### Python Notebook 
We highly recommend you to use this [python notebook](notebooks/usage.ipynb) if you are interested in playing with `py_heideltime`  when using the standalone version.

## How to use
```python
from py_heideltime import heideltime

text = "Thurs August 31st - News today that they are beginning to evacuate the London children tomorrow. Percy is a billeting officer. I can't see that they will be much safer here."

results = heideltime(
    text,
    language='English',
    document_type='news',
    dct='1939-08-31'
)
````


###### Output
The output will be a list of 4 elements or an empty list [] if no temporal expression is found in the text. The four elements are:

- a list of tuples with two positions (e.g., ('XXXX-08-31', 'August 31st')). The first one is the detected temporal expression normalized by heideltime. The second is the temporal expression as it was found in the text;
- a normalized version of the text, where each temporal expression is replaced by its normalized heideltime counterpart;
- a TimeML-annotated version of the text.

## Supported languages

### Standalone
This GitHub package is prepared to work with the following languages: English, Portuguese, Spanish, German, Dutch, Italian, French.

To use `py_heideltime` with other languages proceed as follows:
  
  - Download from [TreeTagger](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/) the parameter files
  - `gunzip <downloaded_file>`
  - Copy the extracted file to the module folder `/py_heideltime/HeidelTime/TreeTagger<your_system>/lib/`


## Publications 

Please cite the appropriate paper when using `py_heideltime`. In general, this would be:

Strötgen, Gertz: Multilingual and Cross-domain Temporal Tagging. Language Resources and Evaluation, 2013. [pdf](https://link.springer.com/article/10.1007%2Fs10579-012-9179-y) [bibtex](https://dbs.ifi.uni-heidelberg.de/files/Team/jannik/publications/stroetgen_bib.html#LREjournal2013)

Other related papers may be found [here](https://github.com/HeidelTime/heideltime#Publications).


