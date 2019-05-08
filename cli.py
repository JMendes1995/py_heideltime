import click
from heideltime import heideltime
@click.command()
@click.option("-t", '--text', help='insert text', required=False)
@click.option("-i", '--input_file', help='input text file', required=False)
def keywords(text, input_file):
    def run_time_matters(text_content):
            output = heideltime(text_content)
            print(output)
    if text and input_file:
        print('Select only text or file to be analysed')
        exit(1)
    elif not text and not input_file:
        print('you must insert text or select file with text')
        exit(1)
    else:
        if text:
            run_time_matters(text)
        else:
            with open(input_file) as file:
                text_content = file.read()
                run_time_matters(text_content)


if __name__ == "__main__":
    keywords()