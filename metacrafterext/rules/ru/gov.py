from pyparsing import oneOf, lineStart, ParseException

RU_NPA_PREFIXES = ['постановление правительства',
                   'распоряжение правительства',
                   'указ президента',
                   'распоряжение президента',
                   'федеральный закон',
                   'федеральный конституционный закон',
                   'конституция рф',
                   'конституция российской федерации',
                   'приказ министерства',
                   'приказ федеральной службы',
                   'приказ федерального агентства',
                   'определение верховного суда',
                   'постановление верховного суда'
                ]

RU_ALL_NPA = RU_NPA_PREFIXES

RU_NPA_RULES = oneOf(RU_ALL_NPA)


def is_ru_law(s):
    try:
        res = RU_NPA_RULES.parseString(s.lower())
        return True
    except ParseException:
        pass
    return False