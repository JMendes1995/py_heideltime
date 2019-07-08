def verify_temporal_tagger(language,date_granularity, document_type):
    from py_heideltime.lang import languages
    if language.lower() not in languages:
        print('Please specify a valid language.\n'
              'Options:\n'
              '      English;\n'
              '      Portuguese;\n'
              '      Spanish;\n'
              '      Germany;\n'
              '      Dutch;\n'
              '      Italian;\n'
              '      French.')
        return {}
    elif date_granularity != 'full' and date_granularity != 'day'and date_granularity != 'month' and date_granularity != 'year':
        print('Please specify a valid date_granularity.\n'
              'options:\n'
              '     full;\n'
              '     year;\n'
              '     month:\n'
              '     day;')
        return {}
    elif document_type.lower() != 'news'and document_type.lower() != 'narrative' and document_type.lower() != 'colloquial' and document_type.lower() != 'scientific' and (document_type.lower() != '' or document_type.lower() == ''):
        print('Please specify a valid document_type.\n'
              'options:\n'
              '     news;\n'
              '     narrative;\n'
              '     colloquial;\n'
              '     scientific;')
        return {}
