"""Validators of the types found in the WDC Web Tables Corpus 2015 (tables of HTML pages that Web Data Commons
extracted from the Common Crawl of July 2015; six segments, 4 963 794 relational tables of 2 571 606 pages on
98 249 hosts): class standings of college rosters, results and win-loss records of game schedules, clothing
sizes, stock availability and condition of shop items, academic terms of course lists, data types of API and
database documentation, priorities of issue trackers, screen resolutions, currency pairs, Unix file modes of
repository browsers, ordinal numbers of ranks and places, athletics and swimming events, HTTP header names and
DNS record types of website statistics pages.

Each function takes one value and returns True when it has the form of the type. Words are compared folded, as in
the validators of the Many Eyes archive: lower case, without accents, spaces and punctuation (R-Fr. is rfr,
X-Large is xlarge).

A validator named ``..._value`` is the stricter one of a rule that looks at the values alone: it leaves out the
words that are as common in other columns as in the type (Jr. and Sr. are also name suffixes; S, M and L are also
letters of gender, results and sides; 100 m is also a length of cable), so that a column needs the words of the
type itself to reach the share of values that labels it.
"""
import re

from metacrafterext.rules.common.b13 import text
from metacrafterext.rules.common.manyeyes import _words, fold

_PARENS = re.compile(r"\s*[(\[][^)\]]*[)\]]\s*")
_MARKS = re.compile(r"[*†‡#!]+$")


def _clean(value):
    """The value without notes in parentheses and trailing marks: Fr. (RS) is Fr., XS (150/76A) is XS."""
    return _MARKS.sub("", _PARENS.sub(" ", text(value))).strip()


# ------------------------------------------------------------------ class standing
CLASS_STANDINGS = _words(
    "fr,so,jr,sr,gr,fr.,so.,jr.,sr.,gr.,freshman,sophomore,junior,senior,graduate,grad,grad student,"
    "graduate student,5th,5th year,fifth year,6th year,first year,first-year,r-fr,r-so,r-jr,r-sr,rs-fr,rs-so,"
    "rs-jr,rs-sr,rfr,rso,rjr,rsr,r-fr.,r-so.,r-jr.,r-sr.,rs fr,rs so,rs jr,rs sr,redshirt freshman,"
    "redshirt sophomore,redshirt junior,redshirt senior,true freshman,fy,gs,5y,5-sr,6-sr,r-gr,rs-gr,soph,soph.,"
    "fresh."
)
# Jr. and Sr. are also suffixes of names, Junior and Senior also levels of tickets and memberships, FR and SO
# also codes of countries and languages: they count in a field named after the class but do not make one (Fr.
# and So. with their full stop do).
_CLASS_COMMON = _words("jr,sr,jr.,sr.,junior,senior,graduate,grad,gr,gr.,5th,first year,first-year,fy,gs,5y,fr,so")
CLASS_STANDINGS_SPECIFIC = CLASS_STANDINGS - _CLASS_COMMON
_FR_SO_DOT = re.compile(r"(?i)^(?:fr|so)\.$")


def validate_class_standing(value):
    """The class standing of a student or a college athlete: Fr., So., Jr., Sr., Gr., R-Fr., RS-So., Freshman,
    Redshirt Junior, Fr. (RS) (not Jr. Varsity, 2015 or A)."""
    return fold(_clean(value)) in CLASS_STANDINGS


def validate_class_standing_value(value):
    """A class standing that is no other word: Fr., So., Freshman, Sophomore, R-Fr., Redshirt Senior (not Jr.,
    Sr., Junior, Senior, or FR and SO without the full stop, which are also codes of France and Somalia)."""
    v = _clean(value)
    return fold(v) in CLASS_STANDINGS_SPECIFIC or bool(_FR_SO_DOT.match(v))


# ------------------------------------------------------------------ clothing sizes
CLOTHING_SIZES = _words(
    "xxs,xs,s,m,l,xl,xxl,xxxl,xxxxl,2xs,3xs,2xl,3xl,4xl,5xl,6xl,7xl,0x,1x,2x,3x,4x,5x,6x,x-small,x small,"
    "xx-small,extra small,extra-small,x-large,x large,extra large,extra-large,xx-large,xxx-large,xxxx-large,"
    "2x-large,3x-large,small,medium,large,petite,tall,one size,one-size,onesize,os,osfa,osfm,o/s,s/m,m/l,l/xl,"
    "xs/s,xl/xxl,xs-s,s-m,m-l,l-xl,lt,xlt,2xlt,3xlt,4xlt,mt,st,xl tall,2xl tall,l tall,"
    "taglia unica,talla unica,taille unique,einheitsgrosse,einheitsgroesse,one size fits all,unica"
)
CLOTHING_SIZES_SPECIFIC = _words(
    "xxs,xs,xl,xxl,xxxl,xxxxl,2xs,3xs,2xl,3xl,4xl,5xl,6xl,7xl,x-small,xx-small,extra small,extra-small,x-large,"
    "extra large,extra-large,xx-large,xxx-large,xxxx-large,2x-large,3x-large,one size,osfa,s/m,m/l,l/xl,xs/s,"
    "xl/xxl,taglia unica,talla unica,taille unique,einheitsgrosse,one size fits all"
)
# XLT and 2XLT (tall sizes) are also trims of Ford trucks (XL, XLT, Lariat): they count only in a field named
# after the size.


# Small, Medium and Large in words are also sizes of companies, drinks and parcels (Not Sized, Small, Medium, Large
# of a register of corporations): they are no clothing sizes on their own, while X-Small and X-Large are.
_SIZE_WORDS = _words("small,medium,large,petite,tall")


def validate_clothing_size(value):
    """A letter size of clothes: XS, S, M, L, XL, XXL, 3XL, 2X, X-Large, One Size, S/M, XLT, XS (150/76A) (not
    32, 10-12, 72.72 KB, Size, or Small, Medium and Large in words, which are also sizes of companies)."""
    key = fold(_clean(value))
    return key in CLOTHING_SIZES and key not in _SIZE_WORDS


def validate_clothing_size_value(value):
    """A letter size that is no other letter or word: XS, XL, XXL, 3XL, X-Large, One Size, S/M (not S, M, L,
    Small or Large)."""
    return fold(_clean(value)) in CLOTHING_SIZES_SPECIFIC


# ------------------------------------------------------------------ game results and records
_GAME_RESULT = re.compile(
    r"(?i)^[(\[]?(?:w|l|t|d|win|won|loss|lost|tie|tied|draw)[)\]]?\s*[,:]?\s*"
    r"\d{1,3}\s*[-–]\s*\d{1,3}"
    r"(?:\s*,?\s*[(\[]?(?:\d?ot|ot\d?|so|f/\d{1,2}|\d{1,2}\s*inn(?:ings|\.)?|pks?|pens?|aet|et|\d{1,2}\s*-\s*\d{1,2}"
    r"(?:\s*,\s*\d{1,2}\s*-\s*\d{1,2})*)[)\]]?)*\s*\*?$"
)


def validate_game_result(value):
    """The result of a game for one side with its score: W 31-28, L, 10-0, W, 3-2 (OT), Won, 3-2, Loss 104-111,
    T 1-1, W 4-3 (10 inn.) (not 3-2, W, Postponed or 2015-16)."""
    return bool(_GAME_RESULT.match(text(value)))


_RECORD = re.compile(r"^[(\[]?\d{1,3}\s?[-–]\s?\d{1,3}(?:\s?[-–]\s?\d{1,3}){0,2}[)\]]?(?:\s*\([^)]*\))?$")


def validate_win_loss_record(value):
    """A win-loss record of a team or player: 20-5, 9-3-0, (10-0), 3-0-0-0, 16-3-0 (W-L-T), 11-8-13
    (not W 3-2, 20, 2015-2016 or 5-6-7-8-9)."""
    v = text(value)
    if not _RECORD.match(v):
        return False
    # 2015-16 and 2014-2015 are seasons, not records.
    return not re.match(r"^(?:19|20)\d{2}\s?[-–]\s?(?:\d{2}|(?:19|20)\d{2})$", v)


# ------------------------------------------------------------------ data types of programming and databases
DATA_TYPES = _words(
    "int,integer,string,str,boolean,bool,float,double,long,char,character,byte,short,void,object,array,dict,"
    "date,datetime,timestamp,time,text,varchar,varchar2,nvarchar,nchar,ntext,clob,blob,decimal,numeric,"
    "number,bigint,smallint,tinyint,mediumint,bit,binary,varbinary,real,money,serial,bigserial,uuid,json,jsonb,"
    "xml,enum,mixed,callable,null,undefined,tuple,regexp,int8,int16,int32,int64,"
    "uint,uint8,uint16,uint32,uint64,float32,float64,double precision,long long,unsigned,unsigned int,"
    "unsigned long,unsigned char,size_t,logical,complex,interval,boolean[],string[],int[],byte[],char[],object[],"
    "long[],double[],float[],xs:string,xs:int,xs:integer,xs:boolean,xs:date,xs:datetime,xs:decimal,xs:double,"
    "xs:anyuri,xsd:string,xsd:int,xsd:boolean,xsd:date,xsd:datetime,xsd:decimal,cstring,nsstring,nsinteger,"
    "nsnumber,cgfloat,bool?,int?,datetime?,guid,dword,qword,lpstr,short integer,"
    "long integer,unsigned short,signed char,unsigned byte"
)
DATA_TYPES_SPECIFIC = _words(
    "int,integer,string,boolean,bool,void,varchar,varchar2,nvarchar,bigint,smallint,tinyint,mediumint,int8,int16,"
    "int32,int64,uint8,uint16,uint32,uint64,float32,float64,datetime,timestamp,uuid,jsonb,clob,blob,"
    "xs:string,xs:int,xs:integer,xs:boolean,xs:date,xs:datetime,xs:decimal,"
    "xsd:string,xsd:int,xsd:boolean,nsstring,nsinteger,cgfloat,size_t,unsigned int,double precision"
)
_SIZED_TYPE = re.compile(
    r"(?i)^(?:(?:n?var)?char(?:acter)?(?:\s+varying)?|varchar2|nvarchar2|n?text|decimal|numeric|number|float|"
    r"(?:tiny|small|medium|big)?int(?:eger)?|bit|(?:var)?binary|raw|timestamp|time|datetime2|string|enum|set)"
    r"\s?\(\s*(?:\d+|max)(?:\s?,\s?\d+)?\s*\)(?:\s+(?:unsigned|signed|zerofill|not null|null|byte|char))*$"
)
_GENERIC_TYPE = re.compile(r"^[A-Z]?[A-Za-z]+<[A-Za-z0-9_?, <>\[\]]+>$")


def _data_type_key(value):
    # The size in parentheses is part of the type (VARCHAR(64)); only the marks of footnotes go.
    v = _MARKS.sub("", text(value)).strip()
    v = re.sub(r"(?i)^(?:java|javax|system)(?:\.\w+)*\.(?=\w+$)", "", v)  # java.lang.String is String
    return v


def validate_data_type(value):
    """The name of a data type of a programming language, a schema or a database: int, String, boolean, void,
    VARCHAR(64), bigint(20) unsigned, Decimal(39,0), List<String>, java.lang.Integer, xs:date, int[], uint32
    (not Name, 255 or Required)."""
    v = _data_type_key(value)
    if not v:
        return False
    if fold(v) in DATA_TYPES or v.lower() in DATA_TYPES:
        return True
    return bool(_SIZED_TYPE.match(v) or _GENERIC_TYPE.match(v))


def validate_data_type_value(value):
    """A data type name that is no English word: int, String, boolean, void, VARCHAR(64), bigint(20) unsigned,
    uint32, List<String> (not Text, Date, Number, Long, Double or Object, which count only in a field named
    after the type)."""
    v = _data_type_key(value)
    if not v:
        return False
    if v.lower() in DATA_TYPES_SPECIFIC or fold(v) in DATA_TYPES_SPECIFIC:
        return True
    return bool(_SIZED_TYPE.match(v) or _GENERIC_TYPE.match(v))


# ------------------------------------------------------------------ academic terms
_SEASON = r"(?:fall|autumn|spring|summer|winter|michaelmas|lent|hilary|trinity|easter)"
_TERM_WORD = r"(?:semester|term|quarter|session|trimester|intersession|block)"
_YEAR = r"(?:(?:19|20)\d{2}(?:\s?[-/–]\s?(?:\d{2}|(?:19|20)\d{2}))?|['’`]\s?\d{2})"
_ACADEMIC_TERM = re.compile(
    rf"(?i)^(?:{_SEASON}(?:\s+{_TERM_WORD})?(?:\s+(?:[ivx]{{1,3}}|[1-4]|[ab]))?\s*,?\s*{_YEAR}"
    rf"|{_YEAR}\s*,?\s*{_SEASON}\s+{_TERM_WORD}(?:\s+(?:[ivx]{{1,3}}|[1-4]))?"
    rf"|(?:1st|2nd|3rd|first|second|third|[1-3])\s+(?:semester|term|trimester)\s*,?\s*{_YEAR}"
    rf"|{_YEAR}\s*,?\s*(?:1st|2nd|3rd|first|second|third|[1-3])\s+(?:semester|term|trimester))$"
)
_TERM_CODE = re.compile(rf"(?i)^(?:fa|fl|sp|su|sm|wi|wn|au)\s?(?:19|20)?\d{{2}}$|^(?:19|20)\d{{2}}\s?(?:fa|sp|su|wi)$"
                        rf"|^{_YEAR}\s*,?\s*{_SEASON}$")
# First Quarter and Quarter 2 are also quarters of the calendar year (pt_quarter, quarter): numbered terms are
# semesters, terms and trimesters only.
_NUMBERED_TERM = r"(?:semester|term|trimester)"
_TERM_ALONE = re.compile(rf"(?i)^(?:{_SEASON}(?:\s+{_TERM_WORD})?|(?:1st|2nd|3rd|first|second|third)\s+{_NUMBERED_TERM}"
                         rf"|{_NUMBERED_TERM}\s+(?:[ivx]{{1,3}}|[1-4]))$")


def validate_academic_term_value(value):
    """An academic term with its year: Fall 2015, Spring Semester 2016, Summer Term 2015, Fall ’10,
    2013 Fall Semester, Fall II 2014, Michaelmas Term 2014, 2nd Semester 2014-15 (not Fall, SU19, Spring Break,
    2015, or 2004 Summer, which is also a Games of the Olympics and counts only in a field named after the
    term)."""
    return bool(_ACADEMIC_TERM.match(text(value)))


def validate_academic_term(value):
    """An academic term in a field named after it, also as a code, with the year first or without a year:
    Fall 2015, FA14, Sp 2011, 2013 Fall, Spring, Semester 2, 1st Semester (not 2015, Week 3 or Finals)."""
    v = text(value)
    return bool(_ACADEMIC_TERM.match(v) or _TERM_CODE.match(v) or _TERM_ALONE.match(v))


# ------------------------------------------------------------------ priority levels
PRIORITIES = _words(
    "high,medium,low,normal,urgent,critical,highest,lowest,very high,very low,blocker,major,minor,trivial,"
    "immediate,emergency,routine,moderate,medium high,medium-high,medium low,medium-low,med,hi,lo,none,"
    "p0,p1,p2,p3,p4,p5,top,must have,should have,could have,won't have,wont have,nice to have,nice-to-have,"
    "showstopper,asap,elevated,standard,hoch,mittel,niedrig,sehr hoch,dringend,haute,moyenne,basse,urgente,"
    "elevee,alta,media,baja,urgente,critica,alta prioridad,alto,medio,bajo,alta priorita,bassa,hoog,gemiddeld,laag"
)
_PRIORITY_SUFFIX = re.compile(r"(?i)\s+(?:priority|prio(?:rit[äa]t)?|priorit[ée])$")
_PRIORITY_PREFIX = re.compile(r"(?i)^(?:\d\s*[-–:.]\s*|p\d\s*[-–:]\s*)")


def validate_priority_level(value):
    """The priority of a task, ticket, bug or request: High, Medium, Low, Normal, Urgent, Critical, Blocker,
    Trivial, P1, Highest, High Priority, 2 - High, Must Have (not 3, Open or Bug)."""
    v = _PRIORITY_PREFIX.sub("", _PRIORITY_SUFFIX.sub("", text(value)))
    return fold(v) in PRIORITIES


# ------------------------------------------------------------------ screen and image resolutions
_RESOLUTION = re.compile(
    r"(?i)^(\d{2,5})\s?[x×*]\s?(\d{2,5})(?:\s?(?:px|pixels?|pixel|pix|p))?(?:\s?@\s?\d{2,3}\s?hz)?"
    r"(?:\s*\(?(?:[a-z0-9+]{2,8}(?:\s[a-z0-9+]{2,4})?)\)?)?$"
)
STANDARD_RESOLUTIONS = {
    (160, 120), (176, 144), (220, 176), (240, 320), (320, 240), (320, 480), (480, 320), (352, 288), (400, 240),
    (480, 800), (480, 854), (540, 960), (640, 360), (640, 480), (640, 960), (640, 1136), (720, 480), (720, 576),
    (720, 1280), (750, 1334), (768, 1024), (800, 480), (800, 600), (800, 1280), (854, 480), (960, 540),
    (960, 640), (1024, 576), (1024, 600), (1024, 768), (1080, 1920), (1136, 640), (1152, 864), (1200, 1920),
    (1280, 720), (1280, 768), (1280, 800), (1280, 960), (1280, 1024), (1334, 750), (1360, 768), (1366, 768),
    (1400, 1050), (1440, 900), (1440, 2560), (1536, 2048), (1600, 900), (1600, 1200), (1680, 1050), (1920, 1080),
    (1920, 1200), (2048, 1080), (2048, 1152), (2048, 1536), (2160, 3840), (2304, 1440), (2560, 1080),
    (2560, 1440), (2560, 1600), (2732, 2048), (2880, 1800), (3200, 1800), (3440, 1440), (3840, 2160),
    (3840, 2400), (4096, 2160), (5120, 2880), (7680, 4320),
}


def _resolution(value):
    m = _RESOLUTION.match(text(value))
    if not m:
        return None
    w, h = int(m.group(1)), int(m.group(2))
    if not (16 <= w <= 16384 and 16 <= h <= 16384):
        return None
    return w, h


def validate_screen_resolution(value):
    """A resolution in pixels, width by height: 1920x1080, 1024 × 768, 320 × 480 px, 3648x2736, 1280x720p,
    1920x1080 (Full HD) (not 15 X 6, 94.2 x 55.0 or 1920)."""
    return _resolution(value) is not None


def validate_screen_resolution_value(value):
    """A common display resolution: 1920x1080, 1366x768, 1024 x 768, 640 × 960 px, 3840x2160 (not 210x277,
    3648x2736 or 100x100, which count only in a field named after the resolution)."""
    return _resolution(value) in STANDARD_RESOLUTIONS


# ------------------------------------------------------------------ availability and condition of items
_AVAILABILITY = re.compile(
    r"(?i)^(?:(?:currently\s+|temporarily\s+)?(?:in|out\s+of)[ -]?stock(?:\s+(?:now|online|in\s+store))?"
    r"|(?:only\s+)?\d+\s+(?:left|in\s+stock|available|copies\s+available)(?:\s+in\s+stock)?|in\s+stock\s*\(\d+\)"
    r"|sold[ -]?out|pre[ -]?order(?:\s+now)?|back[ -]?order(?:ed)?|on\s+back[ -]?order|on\s+order|(?:currently\s+)?"
    r"(?:not\s+)?(?:un)?available(?:\s+(?:now|soon|to\s+order|on\s+request|online|for\s+order))?|discontinued"
    r"|limited(?:\s+(?:stock|availability|quantities))?|low\s+stock|special\s+order|ordered\s+on\s+request"
    r"|call\s+for\s+(?:availability|stock)|coming\s+soon|ships?\s+(?:now|today|in\s+.{1,20})|usually\s+ships\s+.{1,30}"
    r"|auf\s+lager|(?:sofort\s+|nicht\s+)?lieferbar|ausverkauft|en\s+stock|en\s+rupture(?:\s+de\s+stock)?"
    r"|rupture\s+de\s+stock|disponible|agotado|en\s+existencia|sin\s+stock|disponibile|esaurito|non\s+disponibile"
    r"|op\s+voorraad|uitverkocht|leverbaar|em\s+estoque|esgotado|na\s+sklad(?:e|zie)|w\s+magazynie"
    r"|(?:https?://schema\.org/)?(?:InStock|OutOfStock|PreOrder|BackOrder|Discontinued|InStoreOnly|LimitedAvailability"
    r"|OnlineOnly|PreSale|SoldOut|MadeToOrder|Reserved))$"
)
_STOCK_WORDS = re.compile(
    r"(?i)stock|sold[ -]?out|pre[ -]?order|back[ -]?order|on\s+order|\bleft\b|lager|lieferbar|ausverkauft|"
    r"rupture|agotado|existencia|esaurito|voorraad|uitverkocht|estoque|esgotado|sklad|magazyn|order$|sale$"
)


def validate_item_availability(value):
    """The stock availability of an item for sale: In Stock, Out of Stock, Sold Out, Pre-order, Backordered,
    Only 2 left!, 6 copies available, Available, Discontinued, Special Order, Auf Lager, En stock (not 12,
    $9.99 or Add to Cart)."""
    v = _clean(value)
    return bool(_AVAILABILITY.match(v))


def validate_item_availability_value(value):
    """A stock availability that names the stock or the order: In Stock, Out of Stock, Sold Out, Pre-order,
    Only 3 left, Auf Lager (not Available, Unavailable or Discontinued, which count only in a field named after
    the availability)."""
    v = _clean(value)
    return bool(_AVAILABILITY.match(v)) and bool(_STOCK_WORDS.search(v))


CONDITIONS = _words(
    "new,used,refurbished,like new,pre-owned,pre owned,preowned,open box,open-box,brand new,new with tags,"
    "new without tags,nwt,nwot,new with box,new in box,nib,new old stock,nos,new other,for parts,"
    "for parts or not working,parts only,as is,as-is,manufacturer refurbished,seller refurbished,"
    "certified refurbished,factory refurbished,remanufactured,reconditioned,rebuilt,demo,ex-demo,ex display,"
    "mint,near mint,nm,used - like new,used - very good,used - good,used - acceptable,used like new,"
    "collectible,damaged,neu,neuwertig,gebraucht,generalüberholt,neuf,occasion,reconditionne,nuevo,usado,"
    "reacondicionado,nuovo,usato,ricondizionato,nieuw,gebruikt,novo,seminovo,nowy,uzywany,"
    # the values of schema.org/OfferItemCondition, also as URLs (folded, https://schema.org/UsedCondition is
    # httpsschemaorgusedcondition)
    "newcondition,usedcondition,refurbishedcondition,damagedcondition,httpschemaorgnewcondition,"
    "httpschemaorgusedcondition,httpschemaorgrefurbishedcondition,httpschemaorgdamagedcondition,"
    "httpsschemaorgnewcondition,httpsschemaorgusedcondition,httpsschemaorgrefurbishedcondition,"
    "httpsschemaorgdamagedcondition"
)
# Occasion is also an English word (survey intervals: Most Recent, Occasion).
CONDITIONS_SPECIFIC = CONDITIONS - _words("new,neu,neuf,nuevo,nuovo,nieuw,novo,nowy,demo,mint,nm,nos,damaged,as is,as-is,"
                                          "occasion")


def validate_item_condition(value):
    """The condition of an item for sale: New, Used, Refurbished, Like New, Pre-Owned, Open Box, NOS, Used - Good,
    For parts or not working, Gebraucht, Occasion (not Good, Fair, Poor, In Stock or 2007)."""
    return fold(_clean(value)) in CONDITIONS


def validate_item_condition_value(value):
    """An item condition that is no other word: Used, Refurbished, Pre-Owned, Like New, Open Box, Gebraucht
    (not New, Demo or Mint, which count only in a field named after the condition)."""
    return fold(_clean(value)) in CONDITIONS_SPECIFIC


# ------------------------------------------------------------------ currency pairs
CURRENCIES = set(
    "AED AFN ALL AMD ANG AOA ARS AUD AWG AZN BAM BBD BDT BGN BHD BIF BMD BND BOB BOV BRL BSD BTN BWP BYN BYR BZD "
    "CAD CDF CHE CHF CHW CLF CLP CNH CNY COP COU CRC CUC CUP CVE CZK DJF DKK DOP DZD EEK EGP ERN ETB EUR FJD FKP "
    "GBP GEL GHS GIP GMD GNF GTQ GYD HKD HNL HRK HTG HUF IDR ILS INR IQD IRR ISK JMD JOD JPY KES KGS KHR KMF KPW "
    "KRW KWD KYD KZT LAK LBP LKR LRD LSL LTL LVL LYD MAD MDL MGA MKD MMK MNT MOP MRO MRU MUR MVR MWK MXN MXV MYR "
    "MZN NAD NGN NIO NOK NPR NZD OMR PAB PEN PGK PHP PKR PLN PYG QAR RON RSD RUB RWF SAR SBD SCR SDG SEK SGD SHP "
    "SLE SLL SOS SRD SSP STD STN SVC SYP SZL THB TJS TMT TND TOP TRY TTD TWD TZS UAH UGX USD UYU UZS VED VEF VES "
    "VND VUV WST XAF XAG XAU XCD XCG XDR XOF XPD XPF XPT YER ZAR ZMK ZMW ZWG ZWL BTC".split()
)
_PAIR_SEP = re.compile(r"^([A-Za-z]{3})\s?[/:\-]\s?([A-Za-z]{3})$")
_PAIR_JOINED = re.compile(r"^([A-Z]{3})([A-Z]{3})(?:=X)?$")


def _pair(match):
    return bool(match) and match.group(1).upper() in CURRENCIES and match.group(2).upper() in CURRENCIES and \
        match.group(1).upper() != match.group(2).upper()


def validate_currency_pair_value(value):
    """A pair of currencies of an exchange rate, base currency first: EUR/USD, USD/JPY, GBP-USD, eur/chf
    (not EUR, EURUSD, ABC/DEF or USD/USD)."""
    return _pair(_PAIR_SEP.match(text(value)))


def validate_currency_pair(value):
    """A currency pair in a field named after it, also without a separator: EUR/USD, EURUSD, USDJPY=X
    (not EUR or EURO)."""
    v = text(value)
    return _pair(_PAIR_SEP.match(v)) or _pair(_PAIR_JOINED.match(v))


# ------------------------------------------------------------------ Unix file modes
_SYMBOLIC_MODE = re.compile(r"^[-dlcbpsD][-r][-w][-xsS][-r][-w][-xsS][-r][-w][-xtT][@+.]?$")
_OCTAL_MODE = re.compile(r"^0?[0-7]?[0-7]{3}$")


def validate_unix_file_mode_value(value):
    """A Unix file mode as ls writes it: -rw-r--r--, drwxr-xr-x, lrwxrwxrwx, -rwsr-xr-x, d---------, -rw-r--r--@
    (not rw-r--r--, -rw-r--r-x- or 755)."""
    return bool(_SYMBOLIC_MODE.match(text(value)))


def validate_unix_file_mode(value):
    """A Unix file mode in a field named after it, also in octal: -rw-r--r--, 0644, 755, 4755 (not 8, 999 or
    rw)."""
    v = text(value)
    return bool(_SYMBOLIC_MODE.match(v) or _OCTAL_MODE.match(v))


# ------------------------------------------------------------------ ordinal numbers
_ORDINAL = re.compile(r"(?i)^(?:t-?|=)?(\d{1,4})(st|nd|rd|th)\.?(?:\s+(?:place|pl\.?))?$")


def validate_ordinal_number(value):
    """A number written as an English ordinal: 1st, 2nd, 3rd, 4th, 11th, 22nd, 103rd, 4TH, T-3rd, 1st Place
    (not 1, 2th, 11st, 1º or 1er)."""
    m = _ORDINAL.match(text(value))
    if not m:
        return False
    n, suffix = int(m.group(1)), m.group(2).lower()
    if n % 100 in (11, 12, 13):
        return suffix == "th"
    return suffix == {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


# ------------------------------------------------------------------ athletics and swimming events
_EVENT_PREFIX = re.compile(
    r"(?i)^(?:(?:(?:wo)?men(?:'?s)?|boys'?|girls'?|male|female|m|w|b|g|jr\.?|junior|senior|masters?|"
    r"varsity|jv|open|youth|u\d{2}|\d{1,2}\s?-\s?\d{1,2}|\d{1,2}\s?&\s?(?:under|over|up))\s+)+"
)
_EVENT_SUFFIX = re.compile(r"(?i)(?:\s+(?:finals?|prelims?|preliminaries|semi-?finals?|heats?|trials|section\s+\d+|"
                           r"(?:wo)?men|boys|girls|\(?(?:wind|w)?\s?[-+]?\d\.\d\)?)|(?<=[^\d\s])\s+[mwfbg])$")
_TRACK_DISTANCE = re.compile(
    r"(?i)^(?:\d{2,5}\s?(?:m|meters?|metres?|mtrs?|yards?|yds?|y)\b|\d{1,2}(?:\.\d)?\s?(?:k|km)\b|"
    r"(?:1|one|2|two)\s?miles?\b|mile\b|4\s?[x×]\s?\d{2,4}\s?(?:m|meters?|y)?\b)"
)
_TRACK_EVENT = re.compile(
    r"(?i)^(?:\d{2,5}\s?(?:m|meters?|metres?|yards?|yds?|y)?\s+(?:dash|run|hurdles|steeplechase|race\s?walk|walk|"
    r"sprint|relay)|\d{2,3}\s?(?:m|meters?|metres?|yds?)?\s?h(?:urdles)?|\d{2,3}h|(?:4\s?[x×]\s?\d{2,4}\s?"
    r"(?:m|meters?|metres?|yards?|y)?|sprint\s+medley|distance\s+medley|shuttle\s+hurdle)\s*relay|"
    r"(?:high|long|triple)\s+jump|pole\s+vault|shot\s?put|shot|discus(?:\s+throw)?|javelin(?:\s+throw)?|"
    r"hammer(?:\s+throw)?|weight\s+throw|(?:dec|hept|pent)athlon|(?:half\s+)?marathon|steeplechase|"
    r"\d{3,4}\s?m(?:eters?)?\s+(?:steeplechase|s/c)|cross[ -]country|race\s?walk|\d{2}k\s+(?:race\s?)?walk|"
    r"mile\s+run|(?:1|one|2|two)\s+mile\s+run)$"
)
_SWIM_EVENT = re.compile(
    r"(?i)^(?:\d{2,4}\s?(?:m|meters?|metres?|y|yds?|yards?|scy|scm|lcm|sc|lc)?\s+){1,2}(?:(?:sc[ym]|lcm|yard|meter)\s+)?"
    r"(?:free(?:style)?|back(?:stroke)?|breast(?:stroke)?|fly|butterfly|im|i\.m\.|ind\.?\s+medley|"
    r"individual\s+medley|medley|free(?:style)?\s+relay|medley\s+relay)(?:\s+relay)?$"
)


def _event(value):
    v = _EVENT_SUFFIX.sub("", _EVENT_PREFIX.sub("", _clean(value)))
    return " ".join(v.split())


def validate_athletics_event(value):
    """An event of athletics (track and field, road running): 100m, 200 Meter Dash, 110m Hurdles, 4x400m Relay,
    Long Jump, Shot Put, Javelin Throw, Decathlon, Marathon, 3000m Steeplechase, Men's 100m, 5K, Mile
    (not 100 Free, Saturday or 10.34)."""
    v = _event(value)
    return bool(_TRACK_EVENT.match(v) or (_TRACK_DISTANCE.match(v) and len(v) <= 12 and not _SWIM_EVENT.match(v)))


def validate_athletics_event_value(value):
    """An athletics event named by its discipline: 100 Meter Dash, 110m Hurdles, 4x400 Relay, Long Jump, Shot
    Put, Marathon (not 100m, 5K or Mile alone, which are also lengths and count only in a field named after
    the event)."""
    return bool(_TRACK_EVENT.match(_event(value)))


def validate_swimming_event(value):
    """An event of swimming by distance and stroke: 50 Free, 100 Freestyle, 200 IM, 400 Individual Medley,
    100 Back, 200 Breaststroke, 100 Fly, 200 Medley Relay, 400 Free Relay, Women 50 Yard Freestyle, 100 SCY Free
    (not Freestyle, 100m or Long Jump)."""
    return bool(_SWIM_EVENT.match(_event(value)))


# ------------------------------------------------------------------ HTTP header names and DNS record types
HTTP_HEADERS = _words(
    "date,server,content-type,content-length,connection,location,vary,cache-control,x-powered-by,"
    "transfer-encoding,expires,pragma,last-modified,etag,set-cookie,accept-ranges,content-encoding,keep-alive,"
    "x-frame-options,x-xss-protection,x-content-type-options,strict-transport-security,content-language,age,link,"
    "p3p,x-cache,via,x-varnish,x-aspnet-version,x-aspnetmvc-version,x-pingback,x-ua-compatible,"
    "access-control-allow-origin,access-control-allow-methods,access-control-allow-headers,content-security-policy,"
    "x-mod-pagespeed,x-page-speed,cf-ray,x-cache-hit,x-served-by,x-generator,x-drupal-cache,refresh,www-authenticate,"
    "content-disposition,content-md5,content-range,retry-after,status,x-request-id,x-runtime,x-turbo-charged-by,"
    "x-litespeed-cache,host,user-agent,accept,accept-encoding,accept-language,accept-charset,cookie,referer,"
    "authorization,if-modified-since,if-none-match,if-match,if-range,range,origin,upgrade,te,trailer,"
    "x-forwarded-for,x-forwarded-proto,x-real-ip,dnt,x-requested-with,content-location,allow,expect,from,"
    "max-forwards,proxy-authenticate,proxy-authorization,warning,x-robots-tag,x-cache-lookup,x-backend-server,"
    "x-proxy-cache,x-amz-cf-id,x-amz-request-id,x-iinfo,x-sucuri-id,x-content-security-policy,x-webkit-csp,"
    "public-key-pins,alt-svc,referrer-policy,feature-policy,permissions-policy,x-dns-prefetch-control,"
    "x-download-options,x-permitted-cross-domain-policies,x-hacker,x-ah-environment,x-pass-why,x-cacheable,"
    "x-type,x-host,x-age,x-server,x-proxy,x-node,x-mag-cache,x-magento-cache-debug,x-hits"
)
# Date, Server, Location, Link and Status are as common in other columns: they count only in a field named after
# the header.
_HTTP_COMMON = _words("date,server,location,vary,connection,expires,age,link,status,host,accept,range,origin,from,"
                      "allow,warning,refresh,upgrade,expect,te,trailer,via,cookie,referer,authorization")
# X-01 and X-07 are districts of the Bronx: an X- header has a name of letters after the X-.
_X_HEADER = re.compile(r"^[Xx]-[A-Za-z][A-Za-z0-9]+(?:-[A-Za-z0-9]+)*$")


def validate_http_header_name(value):
    """The name of an HTTP header field: Content-Type, Cache-Control, X-Powered-By, Transfer-Encoding, Server,
    Date, Vary, ETag, set-cookie, X-Varnish (not Content-Type: text/html, Header or nginx)."""
    v = text(value).rstrip(":")
    return fold(v) in HTTP_HEADERS or bool(_X_HEADER.match(v))


def validate_http_header_name_value(value):
    """An HTTP header name that is no ordinary word: Content-Type, Cache-Control, X-Powered-By, Last-Modified,
    ETag, Set-Cookie (not Date, Server, Location or Vary, which count only in a field named after the header)."""
    v = text(value).rstrip(":")
    if "-" not in v and fold(v) not in ("etag", "pragma", "p3p"):
        return False
    return (fold(v) in HTTP_HEADERS - _HTTP_COMMON) or bool(_X_HEADER.match(v))


# The record types of the DNS Parameters registry of IANA that are no other abbreviation or word: A, DS, KEY, LOC
# and URI are left out (A is also a grade and a class), so a column of types needs the other ones.
DNS_RECORD_TYPES = set(
    "AAAA CNAME MX NS SOA TXT PTR SRV SPF CAA NAPTR DNSKEY RRSIG NSEC NSEC3 NSEC3PARAM TLSA SSHFP HINFO DNAME "
    "AFSDB SVCB CDS CDNSKEY OPENPGPKEY SMIMEA IPSECKEY DHCID TKEY TSIG ZONEMD CSYNC HTTPS AXFR IXFR WKS RP".split()
)


def validate_dns_record_type(value):
    """A DNS resource record type in upper case: MX, NS, SOA, TXT, CNAME, AAAA, PTR, SRV, SPF, CAA (not A alone,
    mx, MAIL or Type)."""
    return text(value) in DNS_RECORD_TYPES
