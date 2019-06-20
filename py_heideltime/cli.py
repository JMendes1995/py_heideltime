import click
from py_heideltime import py_heideltime

def dates():
    import sys
    arg = []
    for i in range(len(sys.argv)):
        opt = sys.argv[i].lower()
        arg.append(opt)
    t = '''
  Usage_examples (make sure that the input parameters should be within quotes):
  Default Parameters: py_heideltime -t "August 31st" -l "English"
  All the Parameters: py_heideltime -t "August 31st" -l "English" -dg "day" -dt "News" -dct "1939-08-31"

Options:
  [partilally-required]: that is, need to specify one of the two options (text or input_file).
  ----------------------------------------------------------------------------------------------------------------------------------
  -t, --text TEXT                       Input text.
                                        Example: “August 31st”.

  -i, --input_file TEXT                 Text path.
                                        Example: "text.txt"


  [required]
  ----------------------------------------------------------------------------------------------------------------------------------
  -l, --language TEXT                   Language of the text.
                                        Options:
                                                "English";
                                                "Portuguese";
                                                "Spanish";
                                                "Germany";
                                                "Dutch";
                                                "Italian";
                                                "French".

  [not required]
  -----------------------------------------------------------------------------------------------------------------------------------
  -dg, --date_granularity TEXT          Date granularity
                                        Options:
                                                "year" (means that for the date YYYY-MM-DD only the YYYY will be retrieved);
                                                "month" (means that for the date YYYY-MM-DD only the YYYY-MM will be retrieved);
                                                "day" - (default param. Means that for the date YYYY-MM-DD it will retrieve YYYY-MM-DD).

  -dt, --document_type TEXT             Type of the document text.
                                        Options:
                                                "News" for news-style documents - default param;
                                                "Narrative" for narrative-style documents (e.g., Wikipedia articles);
                                                "Colloquial" for English colloquial (e.g., Tweets and SMS);
                                                "Scientific" for scientific articles (e.g., clinical trails).

  -dct, --document_creation_time TEXT   Document creation date in the format YYYY-MM-DD. Taken into account when "News" or "Colloquial"
                                        texts are specified.
                                        Example: "2019-05-30".

  --help                                Show this message and exit.
    '''

    def run_py_heideltime(text):
        lang = get_arguments_values(arg, '-l', '--language', 'English')
        date_granularity = get_arguments_values(arg, '-dg', '--date_granularity', '')
        document_type = get_arguments_values(arg, '-dt', '--document_type', 'news')
        document_creation_time = get_arguments_values(arg, '-dct', '--document_creation_time', '')
        output = py_heideltime(text, lang, date_granularity, document_type, document_creation_time)

        print(output)

    if '--help' in arg:
        print(t)
        exit(1)

    # make sure if was input text arugument
    elif '-t' in arg or '--text' in arg:
        position = verify_argument_pos(arg, '-t', '--text')
        text = arg[position+1]
    elif '-i' in arg or '--input_file' in arg:
        position = verify_argument_pos(arg, '-i', '--input_file')
        path = arg[position+1]
        import codecs
        text = codecs.open(path, "r+", "utf-8").read()
    else:
        print('Bad arguments [--help]')
        exit(1)
    run_py_heideltime(text)


def get_arguments_values(arg_list, argument, extense_argument, defaut_value):
    value = ''
    try:
        try:
            position = arg_list.index(argument)
        except:
            position = arg_list.index(extense_argument)

        if argument in arg_list or extense_argument in arg_list:
            value = arg_list[position + 1]
    except:
        value = defaut_value
    return str(value)


def verify_argument_pos(arg_list, argument, extense_argument):
    try:
        position = arg_list.index(argument)
    except:
        position = arg_list.index(extense_argument)
    return position


if __name__ == "__main__":
    dates()
