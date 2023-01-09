from py_heideltime import heideltime

CLI_MSG = '''
Usage_examples (make sure that the input parameters are within quotes):

  Default Parameters: py_heideltime -t "August 31st" -l "English"
    
  All the Parameters: py_heideltime -t "August 31st" -l "English" -dg "day" -dt "News" -dct "1939-08-31"
    
  Output: the output will be a list of temporal expressions (TE) in the format [(normalized TE; TE as it is found in the text),….] or an empty list [] if no temporal expression is found in the text.

Options:
  [partilally-required]: either specify a text or an input_file path.
  ----------------------------------------------------------------------------------------------------------------------------------
  -t, --text TEXT                       Input text.
                                        Example: “August 31st”.

  -i, --input_file TEXT                 Text path.
                                        Example: “C:\\text.txt


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
                                        Default: "full"
                                        Options:
                                                "full" - (means that all types of granularity will be retrieved, from the coarsest to the finest-granularity).
                                                "day" - (means that for the date YYYY-MM-DD-HH:MM:SS it will retrieve YYYY-MM-DD).
                                                "month" (means that for the date YYYY-MM-DD-HH:MM:SS only the YYYY-MM will be retrieved);
                                                "year" (means that for the date YYYY-MM-DD-HH:MM:SS only the YYYY will be retrieved);

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


def dates():
    import sys
    arg = []
    for i in range(len(sys.argv)):
        opt = sys.argv[i].lower()
        arg.append(opt)

    def run_py_heideltime(text):
        lang = get_arguments_values(arg, '-l', '--language', 'English')
        date_granularity = get_arguments_values(arg, '-dg', '--date_granularity', 'full')
        document_type = get_arguments_values(arg, '-dt', '--document_type', 'news')
        document_creation_time = get_arguments_values(arg, '-dct', '--document_creation_time', 'yyyy-mm-dd')
        result = heideltime(text, lang, date_granularity, document_type, document_creation_time)
        print(result)

    if '--help' in arg:
        print(CLI_MSG)
        exit(1)

    elif '-t' in arg or '--text' in arg:  # make sure if was input text argument
        position = verify_argument_pos(arg, '-t', '--text')
        text = arg[position + 1]

    elif '-i' in arg or '--input_file' in arg:
        position = verify_argument_pos(arg, '-i', '--input_file')
        path = arg[position + 1]

        file = open(path)
        text = file.read()

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
