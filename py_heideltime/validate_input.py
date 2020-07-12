def verify_temporal_tagger(language,date_granularity, document_type):
    from py_heideltime.lang import languages
    document_type_list = ['news', 'narrative', 'colloquial', 'scientific']
    if not isinstance(language, str) and language not in languages or language.lower() not in languages:
        print('Please specify a valid language.\n'
              'Options:\n'
              '      English;\n'
              '      Portuguese;\n'
              '      Spanish;\n'
              '      German;\n'
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
    elif not isinstance(document_type, str) and document_type not in document_type_list or document_type.lower() not in document_type_list:
        print('Please specify a valid document_type.\n'
              'options:\n'
              '     news;\n'
              '     narrative;\n'
              '     colloquial;\n'
              '     scientific;')
        return {}
