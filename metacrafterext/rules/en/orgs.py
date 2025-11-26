

UK_ORG_POSTFIXES = ['ltd',
                    'limited',
                    'plc',
                    'llp',
                    'trust',
                    'partnership',
                    'association'
                    ]


UK_GOVBODIES_POSTFIXES = [
    'council'
]

UK_ALL_ORG_POSTFIXES = UK_ORG_POSTFIXES + UK_GOVBODIES_POSTFIXES

def is_uk_orgname(s):
    s = s.strip().lower()
    parts = s.split()
    if len(parts) < 2:
        return False
    key = parts[-1]
    return key in UK_ALL_ORG_POSTFIXES

US_ORG_POSTFIXES = ['llc', 'inc', 'corp', 'corporate', 'incorporated', 'company',
                    'co-op', 'cooperative', 'association'
                    ]


US_GOVBODIES_POSTFIXES = [
    'council'
]

US_ALL_ORG_POSTFIXES = US_ORG_POSTFIXES + US_GOVBODIES_POSTFIXES

def is_us_orgname(s):
    s = s.strip().lower()
    parts = s.split()
    if len(parts) == 1:
        return False
    key = parts[-1].rstrip('.').rstrip()
    return key in US_ALL_ORG_POSTFIXES




if __name__ == "__main__":
    print(is_uk_orgname('LIMITED'))
    print(is_uk_orgname('TARMAC TRADING LIMITED'))