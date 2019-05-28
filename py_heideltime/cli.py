import click
from py_heideltime import heideltime
@click.command()
@click.option("-t", '--text', help='insert text, text should be surrounded by quotes “” (e.g., “Thurs August 31st”)', required=False)
@click.option("-l", '--language', help='[required] Language text is required and should be surrounded by quotes “”. Options: English, Portuguese, Spanish, Germany, Dutch, Italian, French (e.g., “English”).', required=True)
@click.option("-dg", '--date_granularity', help='Value of granularity should be surrounded by quotes “”. Options: Year, Month, day (e.g., “Year”).', default="", required=False)
@click.option("-dt", '--document_type', help='Type of the document text should be surrounded by quotes “”. Options: “News” : news-style documents; “Narrative” : narrative-style documents (e.g., Wikipedia articles); “Colloquial” : English colloquial (e.g., Tweets and SMS);  “Scientific” : scientific articles (e.g., clinical trails)', default='News', required=False)
@click.option("-dct", '--document_creation_time', help='Document creation date in the format YYYY-MM-DD should be surrounded by quotes (e.g., “2019-05-30”). Note that this date will only be taken into account when News or Colloquial texts are specified.', default='', required=False)
@click.option("-i", '--input_file', help=' text path should be surrounded by quotes (e.g., “text.txt”)', required=False)
def dates(text, language, date_granularity, input_file, document_type, document_creation_time):
    '''
    Usage_examples:
    py_heideltime -t "August 31st" -l "English" or
    py_heideltime -t "August 31st" -l "English" -td "News" -dct "1939-08-31"
    '''
    def run_py_heideltime(text_content):
            output = heideltime(text_content, language, date_granularity, document_type, document_creation_time)
            print(output)
    if text and input_file:
        print('Select only text or file to be analysed')
        exit(1)
    elif not text and not input_file:
        print('you must insert text or select file with text')
        exit(1)
    else:
        if text:
            run_py_heideltime(text)
        else:
            with open(input_file) as file:
                text_content = file.read()
                run_py_heideltime(text_content)


if __name__ == "__main__":
    dates()
