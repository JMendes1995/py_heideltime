def verify_temporal_tagger(language,date_granularity, document_type, document_creation_time):
    if language == '':
        print('You must select a valid language.\n'
              'options:\n'
              '     full;\n'
              '     year;\n'
              '     month:\n'
              '     day;')
        return exit(1)
    elif date_granularity != 'full' and date_granularity != 'day'and date_granularity != 'month' and date_granularity != 'year' :
        print('You must select a valid date_granularity.\n'
              'options:\n'
              '     full;\n'
              '     year;\n'
              '     month:\n'
              '     day;')
        return exit(1)
    elif document_type.lower() != 'news'and document_type.lower() != 'narrative' and document_type.lower() != 'colloquial' and document_type.lower() != 'scientific' and document_type.lower() != '':
        print('You must select a valid document_type.\n'
              'options:\n'
              '     news;\n'
              '     narrative;\n'
              '     colloquial;\n'
              '     scientific;')
        return exit(1)
