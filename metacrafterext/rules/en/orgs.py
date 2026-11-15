

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

# A legal form after an article is a phrase about an organization, not its name: Supported by a
# trust, Not supported by a trust (TrustSchoolFlag of the GIAS schools register), run by a company.
_ARTICLES = frozenset(("a", "an"))


def is_uk_orgname(s):
    s = s.strip().lower()
    parts = s.split()
    if len(parts) < 2:
        return False
    key = parts[-1]
    return key in UK_ALL_ORG_POSTFIXES and parts[-2] not in _ARTICLES

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
    return key in US_ALL_ORG_POSTFIXES and parts[-2] not in _ARTICLES




if __name__ == "__main__":
    print(is_uk_orgname('LIMITED'))
    print(is_uk_orgname('TARMAC TRADING LIMITED'))