import argparse

from py_heideltime import heideltime
from py_heideltime.meta import LANGUAGES, DOC_TYPES


def cli():
    parser = argparse.ArgumentParser(
        prog="py_heideltime",
        description="CLI for the HeidelTime temporal tagger.",
    )

    parser.add_argument(
        "text",
        type=str,
        help="Input text.\nExample: “In the day I was born, August 31st, it was raining”."
    )

    parser.add_argument(
        "-l",
        "--language",
        default="english",
        type=str,
        help="Language of the text.",
        choices=LANGUAGES,
        metavar="LANG"
    )

    parser.add_argument(
        "-dt",
        "--document_type",
        default="news",
        type=str,
        help="Type of the document text.",
        choices=DOC_TYPES,
        metavar="DOC_TYPE"
    )

    parser.add_argument(
        "-dct",
        "--document_creation_time",
        default=None,
        type=str,
        help="Document creation time in the format YYYY-MM-DD.\n"
             "Taken into account when \"News\" or \"Colloquial\" texts are specified.\n"
             "Example: \"2019-05-30\".",
        metavar="DCT"
    )

    args = parser.parse_args()

    heideltime(
        text=args.text,
        language=args.language,
        document_type=args.doc_type,
        dct=args.dct
    )


if __name__ == "__main__":
    cli()
