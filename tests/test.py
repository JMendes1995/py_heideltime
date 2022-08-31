# -*- encoding: utf-8 -*-
from py_heideltime import py_heideltime
from tests import texts
from datetime import datetime
import timeit


if __name__ == '__main__':

    def test(doc, lang, date_granularity='full', document_type='news', document_creation_time='yyyy-mm-dd'):
        docInfo = texts.dictTests[doc]
        text = docInfo[0]
        score = docInfo[1]
        textNormalized = docInfo[2]
        timeML = docInfo[3]

        startTime = datetime.now()
        print("\n")
        print(doc)
        print("----------")
        print(startTime)
        print(f"#Total Chars = {len(text)}")
        results = py_heideltime(text, language=lang, date_granularity=date_granularity, document_type=document_type, document_creation_time=document_creation_time)
        Score = results[0]
        print(Score)
        TextNormalized = results[1]
        print(TextNormalized)
        TimeML = results[2]
        print(TimeML)
        print(datetime.now() - startTime)

        assert Score == score
        assert textNormalized in TextNormalized
        assert timeML in TimeML

    test("pt_emoji", "Portuguese")
    test("pt_wikipedia_revolucao_francesa", "Portuguese") #54530 chars
    test("pt_wikipedia_planeta", "Portuguese") # 51668 chars
    test("pt_arquivo_jugular", "Portuguese") # 28746 chars
    test("pt_wikipedia_25_de_abril", "Portuguese") # 18997 chars
    test("pt_wikipedia_operacao_marques", "Portuguese") # 17029 chars
    test("pt_dilma", "Portuguese") # 2835 chars

    test("en_boston_marathon", "English") # 58547 chars
    test("en_neuroscience", "English") # 5647 chars
    #res = timeit.timeit(f'{test("en_neuroscience", "English")}') # 5647 chars, timeit = 0.0107

    test("en_haiti_earthquake", "English") # 781 chars
    #res = timeit.timeit(f'{test("en_haiti_earthquake", "English")}') # 781 chars, timeit = 0.0113

    test("en_london", "English")
    #res = timeit.timeit(f'{test("en_london", "English")}') # 185 chars, timeit = 0.0121913

    test("en_london_options", "English", date_granularity="day", document_type='news', document_creation_time='1939-08-31') # 185 chars

    test("fr_helmut", "French") # 543 chars

