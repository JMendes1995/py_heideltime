def verify_temporal_tagger(language,date_granularity, document_type, document_creation_time):
    if language == '':
        print('You must select a valid language.\n')
        return {}
    elif date_granularity != 'full' and date_granularity != 'day'and date_granularity != 'month' and date_granularity != 'year' and date_granularity !='':
        print('You must select a valid date_granularity.\n'
              'options:\n'
              '     full;\n'
              '     year;\n'
              '     month:\n'
              '     day;')
        return {}
    elif document_type.lower() != 'news'and document_type.lower() != 'narrative' and document_type.lower() != 'colloquial' and document_type.lower() != 'scientific':
        print('You must select a valid document_type.\n'
              'options:\n'
              '     news;\n'
              '     narrative;\n'
              '     colloquial;\n'
              '     scientific;')
        return {}
