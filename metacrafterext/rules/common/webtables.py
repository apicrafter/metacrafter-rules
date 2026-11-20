"""Validators of the types found in the WDC Web Tables Corpus 2015 (tables of HTML pages that Web Data Commons
extracted from the Common Crawl of July 2015; six segments, 4 963 794 relational tables of 2 571 606 pages on
98 249 hosts): class standings of college rosters, results and win-loss records of game schedules, clothing
sizes, stock availability and condition of shop items, academic terms of course lists, data types of API and
database documentation, priorities of issue trackers, screen resolutions, currency pairs, Unix file modes of
repository browsers, ordinal numbers of ranks and places, athletics and swimming events, HTTP header names and
DNS record types of website statistics pages.

Six more segments of the same crawl (4 978 140 tables of 2 555 031 pages on 98 133 hosts) added the venue of
games (home, away, neutral), how players bat and throw (R/R, L/R), winning and losing streaks, penalties of ice
hockey, lacrosse and football, conferences of US college sports, television networks, heights of players in feet
and inches (6-2), time ranges of schedules (9:00am - 5:00pm), times relative to now (2 days ago), the nutrients
of nutrition labels, holidays, relationships to the head of a household in census transcriptions, grade spans of
schools (K-5, PK-8), meeting days of classes (MWF, TR), IOC country codes and POSIX errno names.

Seven more segments (5 778 000 tables of 2 963 718 pages on 109 005 hosts) added the seasons of sports leagues
(2013-14), types of dwellings (Semi-detached, Condo), age groups of youth sports (U12, 12U), the names of Dublin
Core elements in repository records (dc.date.issued), keyboard shortcuts (Ctrl+C), the Exif tags of photos,
branches of the armed forces, stock market indexes, stock exchanges, betting odds (9-2, 5/1), types of crimes and
crops.

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


# ================================================================== second six segments of the crawl
# ------------------------------------------------------------------ home or away
HOME_AWAY = _words("home,away,neutral,neutral site,road,h,a,n,vs,v,at,heim,auswarts,domicile,exterieur,casa,fuera,"
                   "visitante,visitor,visiting")
HOME_AWAY_SPECIFIC = _words("home,away,neutral,neutral site")
_VS = re.compile(r"(?i)^(?:@|vs\.?|v\.?|at)$")


def validate_home_away(value):
    """Where a team plays a game: Home, Away, Neutral, H, A, N, @, vs., at, Road, Heim, Domicile (H (9) is H; not
    Home Run, Chicago or 3-2)."""
    v = _clean(value)
    return bool(_VS.match(v)) or fold(v) in HOME_AWAY


def validate_home_away_value(value):
    """Home, Away or Neutral in words (not H, A, N, @ or at, which count only in a field named after the venue)."""
    return fold(_clean(value)) in HOME_AWAY_SPECIFIC


# ------------------------------------------------------------------ bats and throws
_BATS_THROWS = re.compile(r"^([LRSB])\s?[/-]\s?([LR])$")
_BATS_THROWS_WORDS = re.compile(r"(?i)^(left|right|switch|both)\s?[/-]\s?(left|right)$")
_BATS_THROWS_SLASH = re.compile(r"^[LRSB]\s?/\s?[LR]$")


def validate_bats_throws(value):
    """How a baseball or softball player bats and throws: R/R, L/R, S/R (switch hitter), B/L, R-R, Left/Right (not
    R, 6-2 or L/XL)."""
    v = _clean(value)
    return bool(_BATS_THROWS.match(v) or _BATS_THROWS_WORDS.match(v))


def validate_bats_throws_value(value):
    """Bats and throws as two capital letters with a slash: R/R, L/R, S/R, B/R (R-R and Left/Right count only in a
    field named B/T or Bats/Throws)."""
    return bool(_BATS_THROWS_SLASH.match(_clean(value)))


# ------------------------------------------------------------------ winning and losing streaks
_STREAK = re.compile(r"(?i)^(?:[WLTD]\s?-?\s?\d{1,3}|\d{1,3}\s?[WLTD]|(?:won|lost|tied|drew|win|loss|lose)\s+\d{1,3})$")


def validate_win_loss_streak(value):
    """The current run of wins or losses of a team in a standings table: W3, L1, W 2, 1L, Won 4, Lost 2, T1 (not
    W, 3-2 or L/R)."""
    return bool(_STREAK.match(_clean(value)))


# ------------------------------------------------------------------ penalties of games
PENALTIES = _words(
    "slashing,tripping,hooking,holding,interference,roughing,cross-checking,cross-check,high sticking,high-sticking,"
    "boarding,charging,elbowing,spearing,butt-ending,kneeing,clipping,head-butting,unsportsmanlike conduct,"
    "unsportsmanlike,too many men,too many men on the ice,too many players,too many players on ice,"
    "too many players on the field,delay of game,illegal body check,illegal body checking,body checking,checking,"
    "checking from behind,hitting from behind,hitting after whistle,hitting after the whistle,contact to the head,"
    "head contact,illegal check to the head,illegal hit,illegal equipment,illegal stick,illegal crosse,"
    "illegal procedure,illegal substitution,illegal screen,illegal formation,illegal use of hands,illegal motion,"
    "unnecessary roughness,pushing,warding off,offside,offsides,holding the stick,crease violation,"
    "goaltender interference,goalie interference,embellishment,diving,fighting,instigator,game misconduct,"
    "misconduct,10-minute misconduct,10 minute misconduct,gross misconduct,match penalty,bench minor,double minor,"
    "conduct foul,technical foul,personal foul,flagrant foul,yellow card,red card,green card,false start,"
    "pass interference,face mask,facemask,encroachment,neutral zone infraction,intentional grounding,"
    "roughing the passer,roughing the kicker,running into the kicker,horse collar,targeting,disqualification,"
    "dangerous play,obstruction,handball,hand ball,time wasting,dissent,simulation,abuse of officials,"
    "crosse in face,roughing atw,interference with the goalkeeper"
)
# Holding, Interference, Pushing, Charging, Boarding, Fighting, Diving and Checking are also ordinary words (a
# holding company, boarding of a flight, a checking account): they count only in a field named after the penalty.
PENALTIES_SPECIFIC = PENALTIES - _words(
    "holding,interference,pushing,offside,offsides,fighting,charging,boarding,clipping,diving,checking,misconduct,"
    "obstruction,handball,hand ball,dissent,simulation,targeting,disqualification,encroachment,instigator,"
    "time wasting,dangerous play,unsportsmanlike"
)
_PENALTY_PREFIX = re.compile(r"(?i)^(?:[OD]\s?-\s?|(?:minor|major|double minor|bench minor)\s*[-–:]\s*|"
                             r"\d{1,2}\s?(?:min\.?|mins\.?|minutes?|:00)\s*[-–:]?\s*)")
_PENALTY_SUFFIX = re.compile(r"(?i)\s*[-–,]\s*(?:\d{1,2}(?::\d{2})?\s?(?:min\.?|mins\.?|minutes?)?|minor|major)$")


def _penalty(value):
    return fold(_PENALTY_SUFFIX.sub("", _PENALTY_PREFIX.sub("", _clean(value))))


def validate_sports_penalty(value):
    """A penalty or foul of a game: Slashing, Tripping, Hooking, Holding, Cross-Checking, High Sticking, Delay of
    Game, Unsportsmanlike Conduct, Yellow Card, Offside, Pass Interference, Slashing (2 min), O-HOOKING (not 2:00,
    Robbery or Penalty)."""
    return _penalty(value) in PENALTIES


def validate_sports_penalty_value(value):
    """A penalty that is no ordinary word: Slashing, Tripping, Hooking, Cross-Checking, Yellow Card, Delay of Game
    (not Holding, Interference, Boarding or Fighting, which count only in a field named after the penalty)."""
    return _penalty(value) in PENALTIES_SPECIFIC


# ------------------------------------------------------------------ conferences of US college sports
CONFERENCES = _words(
    "acc,atlantic coast,atlantic coast conference,sec,southeastern,southeastern conference,big 12,big xii,"
    "big twelve,big ten,big 10,b1g,big east,pac-12,pac 12,pac-10,pac-8,pacific-10,conference usa,c-usa,cusa,wac,"
    "western athletic,mac,mid-american,mountain west,mwc,sun belt,american,aac,the american,american athletic,"
    "missouri valley,mvc,mvfc,missouri valley football,atlantic 10,a-10,colonial,caa,colonial athletic,horizon,"
    "horizon league,ivy,ivy league,patriot,patriot league,southern,socon,southern conference,southland,swac,"
    "southwestern athletic,meac,mid-eastern athletic,big sky,big south,big west,summit,summit league,america east,"
    "atlantic sun,a-sun,asun,maac,metro atlantic,nec,northeast,northeast conference,ovc,ohio valley,west coast,"
    "wcc,independent,ind,independents,big eight,big 8,southwest,swc,pioneer,pioneer league,metro,great west,"
    "great midwest,midwestern collegiate,trans america,ecac,ecac hockey,hockey east,nchc,wcha,ccha,"
    "atlantic hockey,big ten hockey,gnac,gliac,glvc,psac,ne-10,northeast-10,ciaa,siac,sac,south atlantic,"
    "gulf south,gsc,lone star,lsc,rmac,miaa,nsic,pacwest,ccaa,gac,great american,mec,nescac,uaa,centennial,"
    "liberty league,ncac,odac,oac,miac,wiac,cciw,sciac,nwc,hcac,iiac,american southwest,asc,naia,"
    "heartland,usa south,capital athletic,cac,empire 8,sunyac,njac,mascac,little east,cunyac,skyline,"
    "landmark,mac commonwealth,mac freedom,presidents' athletic,pac,sliac,umac,nacc,cconf,mid-south,kcac,"
    "sooner athletic,golden state,cal pac,frontier,crossroads,wolverine-hoosier,gpac,red river,sun conference,"
    "appalachian,ssac,river states,chicagoland"
)
# ACC, SEC, MAC and WAC are also abbreviations of other things (the SEC of the stock market, a MAC address, the
# ticker WAC), and American, Southern, Independent, Ivy, Summit and Metro are also words: they count only in a
# field named after the conference.
# The acronyms of conferences are codes of other things too (PSAC is a participant status of the directory of
# the Bank of Russia): only names in words count by value.
CONFERENCES_SPECIFIC = _words(
    "atlantic coast conference,southeastern conference,big 12,big xii,big ten,big east,pac-12,pac-10,"
    "conference usa,mountain west,sun belt,american athletic,missouri valley,atlantic 10,colonial athletic,"
    "horizon league,ivy league,patriot league,southern conference,southland,big sky,big south,big west,"
    "summit league,america east,atlantic sun,big eight,pioneer league,hockey east,ecac hockey,atlantic hockey,"
    "northeast-10,gulf south,lone star,pacwest,liberty league"
)


def validate_athletic_conference(value):
    """An athletic conference of US college sports: SEC, ACC, Big Ten, Big 12, Pac-12, Big East, Conference USA,
    Mountain West, Sun Belt, Ivy, MAC, WAC, Independent, NESCAC, GLIAC (not 6-2, Conference or NFC)."""
    v = re.sub(r"(?i)\s+conference$", "", _clean(value)) or _clean(value)
    return fold(v) in CONFERENCES or fold(value) in CONFERENCES


def validate_athletic_conference_value(value):
    """A conference that is no other abbreviation or word: Big Ten, Big 12, Pac-12, Big East, Mountain West, Sun
    Belt, Ivy League, WAC (not SEC, ACC, MAC, American or Independent alone)."""
    return fold(_clean(value)) in CONFERENCES_SPECIFIC


# ------------------------------------------------------------------ television networks
TV_NETWORKS = _words(
    "abc,nbc,cbs,fox,cw,the cw,pbs,upn,wb,the wb,mynetworktv,ion,espn,espn2,espnu,espn3,espnews,espn classic,"
    "espn deportes,espn+,espn plus,espn-fc,espnfc,longhorn network,lhn,sec network,secn,secn+,acc network,accn,"
    "acc network extra,big ten network,btn,btn2go,btn plus,pac-12 network,pac-12 networks,p12n,cbs sports network,"
    "cbssn,cbs sports,cbss,nbc sports,nbcsn,nbc sports network,versus,fox sports 1,fs1,fox sports 2,fs2,fsn,"
    "fox sports net,fox college sports,fox sports,root sports,root,csn,comcast sportsnet,mlb network,mlbn,"
    "nfl network,nfln,nba tv,nhl network,golf channel,golf,tennis channel,tnt,tbs,trutv,usa,usa network,hbo,"
    "showtime,cinemax,starz,amc,fx,fxx,a&e,history,history channel,discovery,discovery channel,tlc,bravo,e!,syfy,"
    "lifetime,hallmark channel,comedy central,mtv,vh1,bet,nickelodeon,nick,disney channel,abc family,freeform,"
    "cartoon network,adult swim,food network,hgtv,travel channel,animal planet,national geographic,nat geo,ifc,"
    "sundance,oxygen,we tv,own,spike,tv land,cmt,cnn,hln,msnbc,cnbc,fox news,fox business,c-span,univision,"
    "telemundo,unimas,galavision,wgn,wgn america,tsn,tsn2,sportsnet,cbc,ctv,bbc one,bbc two,bbc three,bbc four,"
    "itv,itv2,channel 4,channel 5,e4,sky sports,sky one,sky atlantic,bt sport,eurosport,rte one,tg4,bein sport,"
    "bein sports,nesn,masn,sny,yes,csn chicago,prime ticket,altitude,sun sports,fox sports net north"
)
# Words, countries and the letters of other things (USA, YES, History, Discovery, Golf, Root, Own, ION) count only
# in a field named after the network, and so do ABC, CBS, NBC, TBS and TNT, which are also stock tickers
# (AmerisourceBergen is ABC in the insider trades of a stock site), and short codes such as FXX (the code of
# metropolitan France in French commune tables) and BTN (Bhutan).
TV_NETWORKS_SPECIFIC = TV_NETWORKS - _words(
    "fox,cw,the cw,wb,the wb,ion,usa,root,history,discovery,golf,own,nick,oxygen,spike,bravo,lifetime,starz,"
    "versus,sundance,yes,altitude,e!,amc,bet,tlc,ifc,cmt,fx,itv,e4,sac,csn,global,abc,cbs,nbc,pbs,tbs,tnt,upn,"
    "cbc,ctv,bbc,fxx,btn,secn,accn,lhn,p12n,mlbn,nfln,hln,tsn,tsn2,sny,nesn,masn,wgn,fsn,cbss"
)
_NETWORK_SPLIT = re.compile(r"\s*(?:/|,|;|\bor\b|\band\b|\+(?=\s))\s*")


def _networks(value):
    v = re.sub(r"(?i)\.com$", "", _clean(value))
    # A&E folds to ae: AE without the ampersand is a code of other things (sections AE and BE of a course)
    return [fold(p) if fold(p) != "ae" or "&" in p else p for p in _NETWORK_SPLIT.split(v) if p.strip()]


def validate_tv_network(value):
    """A television network or channel that carries a game or a show: ESPN, ABC, NBC, CBS, ESPN2, FOX, NBCSN, TNT,
    FS1, BTN, SEC Network, HBO, ESPN2/ESPN3, ESPN or ESPN2 (not 8, TBA or Channel 9)."""
    parts = _networks(value)
    return bool(parts) and all(p in TV_NETWORKS for p in parts)


def validate_tv_network_value(value):
    """A network that is no word, country or ticker: ESPN, ESPN2, ESPNU, NBCSN, CBSSN, FS1, HBO, ESPN2/ESPN3 (not
    USA, YES, History, FOX, ABC or CBS alone, which count only in a field named after the network)."""
    parts = _networks(value)
    return bool(parts) and all(p in TV_NETWORKS_SPECIFIC for p in parts)


# ------------------------------------------------------------------ heights of persons in feet and inches
_FEET_INCHES = re.compile(
    r"""^([3-8])\s?(?:-|'|’|′|ft\.?|feet|foot)\s?(?:(\d|1[01])(?:\.\d{1,2}|\s?[¼½¾])?\s?(?:"|''|”|″|in\.?|inch(?:es)?)?)?$"""
)
_FEET_INCHES_MARKED = re.compile(r"""^[3-8]\s?(?:'|’|′|ft\.?)\s?(?:(?:\d|1[01])(?:\.\d{1,2}|\s?[¼½¾])?\s?(?:"|''|”|″|in\.?)?)?$""")


def validate_height_feet_inches(value):
    """The height of a person in feet and inches: 6-2, 5-11, 6'2", 5' 10", 6'1, 6 ft 2 in, 6' (not 2-1, 6-12, 72
    or 180 cm)."""
    v = _clean(value)
    return bool(_FEET_INCHES.match(v)) and v[-1] != "-"


def validate_height_feet_inches_value(value):
    """A height in feet and inches with the foot mark: 6'2", 5' 10", 6'1, 6 ft 2 in (6-2 counts only in a field
    named Ht. or Hgt, since it is also a score, a record and a range of metres: the height classes 3-6 and 6-10 of
    a tree register are no feet and inches, so a field named Height alone takes the marked forms only)."""
    return bool(_FEET_INCHES_MARKED.match(_clean(value)))


# ------------------------------------------------------------------ time ranges
_CLOCK = r"(?:(?:[01]?\d|2[0-4])(?::[0-5]\d)?\s?(?:[ap]\.?\s?m\.?)?|noon|midnight)"
_TIME_RANGE = re.compile(rf"(?i)^({_CLOCK})\s*(?:[-–—~]|to|until|till|thru|bis)\s*({_CLOCK})"
                         r"(?:\s*\(?(?:[ecmp][sd]?t|gmt|utc|local time)\)?)?$")
_MERIDIEM = re.compile(r"(?i)[ap]\.?\s?m\.?$|noon|midnight")


def validate_time_range(value):
    """A range of clock times: 10:00 - 11:00, 9:00am - 5:00pm, 8:30 a.m. - 4:30 p.m., 12–4:00 pm, 17:00-18:30, 9am to
    noon (not 9-5, 1-1:00, 2015-2016 or Mon-Fri 9-5): both times have minutes, or one says am, pm or noon."""
    m = _TIME_RANGE.match(_clean(value))
    if not m:
        return False
    start, end = m.group(1).strip(), m.group(2).strip()
    if _MERIDIEM.search(start) or _MERIDIEM.search(end):
        return True
    return ":" in start and ":" in end


# ------------------------------------------------------------------ times relative to now
_REL_UNIT = r"(?:seconds?|secs?|s|minutes?|mins?|m|hours?|hrs?|h|days?|d|weeks?|wks?|w|months?|mos?|years?|yrs?|y)"
_RELATIVE_TIME = re.compile(
    rf"(?i)^(?:(?:posted|updated|added|joined|modified|edited|active)\s+)?(?:about |over |almost |nearly |"
    rf"less than |more than |just )?(?:(?:\d+|an?|one)\s?{_REL_UNIT}\.?,?\s+(?:and\s+)?)*(?:\d+|an?|one|few)\s?"
    rf"{_REL_UNIT}\.?\s+ago$|^(?:a\s+)?(?:few\s+)?(?:moments?|seconds?)\s+ago$"
)


def validate_relative_time(value):
    """A time given as the span back from now: 2 days ago, 1 hour ago, an hour ago, 2 years 38 weeks ago, 1h 35min
    ago, about 3 months ago, 5 mins ago, posted 3 days ago (not 2 days, Jul 22, 2015 or ago)."""
    return bool(_RELATIVE_TIME.match(_clean(value)))


# ------------------------------------------------------------------ nutrients
NUTRIENTS = _words(
    "energy,calories,calorie,kcal,kilocalories,kilojoules,protein,proteins,fat,fats,total fat,lipids,total lipid,"
    "saturated fat,saturated fats,saturates,saturated fatty acids,trans fat,trans fatty acids,fatty acids,"
    "monounsaturated fat,monounsaturates,polyunsaturated fat,polyunsaturates,omega-3,omega-6,cholesterol,"
    "carbohydrate,carbohydrates,total carbohydrate,total carbohydrates,carbs,net carbs,sugar,sugars,total sugars,"
    "added sugars,starch,polyols,fibre,fiber,dietary fiber,dietary fibre,total dietary fiber,crude fiber,crude fibre,"
    "crude protein,crude fat,sodium,salt,potassium,calcium,iron,magnesium,phosphorus,zinc,copper,manganese,selenium,"
    "iodine,chloride,fluoride,chromium,molybdenum,vitamin a,vitamin b1,vitamin b2,vitamin b3,vitamin b5,"
    "vitamin b6,vitamin b7,vitamin b9,vitamin b12,vitamin c,vitamin d,vitamin d2,vitamin d3,vitamin e,vitamin k,"
    "vitamin k1,vitamin k2,thiamin,thiamine,riboflavin,niacin,pantothenic acid,biotin,folate,folic acid,folacin,"
    "choline,lactose,water,moisture,ash,caffeine,calories from fat,of which saturates,of which sugars,"
    "of which sugar,of which polyols,of which starch,salt equivalent,beta carotene,retinol,lycopene,lutein,"
    "proximates,eiweiss,fett,kohlenhydrate,ballaststoffe,zucker,salz,brennwert,glucides,lipides,proteines,"
    "fibres,sucres,matieres grasses,valeur energetique,grassi,carboidrati,proteine,zuccheri,grasas,"
    "hidratos de carbono,proteinas,azucares,"
    # the components of the USDA food composition tables (National Nutrient Database for Standard Reference)
    "sucrose,glucose,dextrose,fructose,maltose,galactose,minerals,vitamins,lipids,amino acids,betaine,carotene,"
    "cryptoxanthin,lutein + zeaxanthin,lutein zeaxanthin,tocopherol,tocotrienol,phytosterols,stigmasterol,"
    "campesterol,beta-sitosterol,menaquinone-4,dihydrophylloquinone,phylloquinone,tryptophan,threonine,isoleucine,"
    "leucine,lysine,methionine,cystine,phenylalanine,tyrosine,valine,arginine,histidine,alanine,aspartic acid,"
    "glutamic acid,glycine,proline,serine,hydroxyproline,alcohol,theobromine,folate dfe,food folate,"
    "retinol activity equivalents"
)
# Minerals and elements (Sodium, Calcium, Iron, Zinc) are also the analytes of water and soil samples, sugars and
# amino acids (Glucose, Glycine) the compounds of chemistry tables, Fibre a shape of microplastics, and Energy,
# Water, Salt and Fat are words of other columns: a column needs the names of the label itself (Protein, Total Fat, Sugars, Vitamin C) to be one of
# nutrients by its values.
NUTRIENTS_SPECIFIC = NUTRIENTS - _words(
    "energy,fat,fats,lipids,sugar,starch,sodium,salt,potassium,calcium,iron,magnesium,phosphorus,zinc,copper,"
    "manganese,selenium,iodine,chloride,fluoride,chromium,molybdenum,lactose,water,moisture,ash,caffeine,"
    "proximates,fett,zucker,salz,grassi,kcal,sucrose,glucose,dextrose,fructose,maltose,galactose,minerals,"
    "vitamins,amino acids,betaine,carotene,tocopherol,tryptophan,threonine,isoleucine,leucine,lysine,methionine,"
    "cystine,phenylalanine,tyrosine,valine,arginine,histidine,alanine,aspartic acid,glutamic acid,glycine,"
    "proline,serine,hydroxyproline,alcohol,theobromine,phytosterols,stigmasterol,campesterol,fibre,fiber,fibres"
)
# A fatty acid in the shorthand of food composition tables: carbons and double bonds (16:0, 18:1 undifferentiated,
# 20:5 n-3 (EPA)); it counts only in a field named after the nutrient.
_FATTY_ACID = re.compile(r"(?i)^(?:[4-9]|1\d|2[0-6]):[0-6](?:\s?(?:n-\d{1,2}|[ct]|undifferentiated))*$")
_NUTRIENT_LEAD = re.compile(r"^[-–—•·\s]+")


def _nutrient(value):
    v = _NUTRIENT_LEAD.sub("", _clean(value)).rstrip(":*").strip()
    return fold(v), fold(v.split(",")[0])


def validate_nutrient(value):
    """A nutrient of a nutrition facts label or a food composition table: Protein, Total Fat, Saturated Fat,
    Sodium, Total Carbohydrate, Dietary Fiber, Sugars, Vitamin C, Calcium, Iron, of which saturates, Iron, Fe,
    Carbohydrate, by difference, Riboflavin (B2), Ballaststoffe, Glucose (dextrose), Leucine, 18:1 undifferentiated
    (not 5 g, Apple or Nutrition Facts)."""
    full, head = _nutrient(value)
    return full in NUTRIENTS or head in NUTRIENTS or bool(_FATTY_ACID.match(_clean(value)))


def validate_nutrient_value(value):
    """A nutrient named on nutrition labels and nowhere else as often: Protein, Total Fat, Saturated Fat,
    Cholesterol, Dietary Fiber, Sugars, Vitamin C, Niacin (not Sodium, Iron, Calcium, Energy or Water alone)."""
    full, head = _nutrient(value)
    return full in NUTRIENTS_SPECIFIC or head in NUTRIENTS_SPECIFIC


# ------------------------------------------------------------------ holidays
HOLIDAYS = _words(
    "new year's day,new years day,new year's eve,new years eve,martin luther king jr. day,martin luther king day,"
    "martin luther king, jr. day,martin luther king jr. birthday,mlk day,inauguration day,lincoln's birthday,"
    "presidents' day,presidents day,president's day,washington's birthday,mardi gras,ash wednesday,"
    "st. patrick's day,saint patrick's day,good friday,holy thursday,maundy thursday,holy saturday,easter,"
    "easter sunday,easter monday,passover,patriots' day,cesar chavez day,memorial day,juneteenth,"
    "independence day,fourth of july,4th of july,july 4th,july fourth,canada day,civic holiday,labor day,"
    "labour day,columbus day,indigenous peoples' day,thanksgiving,thanksgiving day,day after thanksgiving,"
    "black friday,veterans day,veterans' day,remembrance day,armistice day,election day,christmas,christmas day,"
    "christmas eve,boxing day,st. stephen's day,kwanzaa,hanukkah,chanukah,rosh hashanah,yom kippur,eid al-fitr,"
    "eid al-adha,diwali,chinese new year,lunar new year,victoria day,family day,islander day,louis riel day,"
    "saint-jean-baptiste day,st. jean baptiste day,national aboriginal day,australia day,anzac day,"
    "queen's birthday,king's birthday,melbourne cup day,waitangi day,bank holiday,early may bank holiday,"
    "spring bank holiday,summer bank holiday,august bank holiday,may day,whit monday,whitsun,pentecost,"
    "whit sunday,ascension day,corpus christi,assumption day,assumption of mary,all saints' day,all souls' day,"
    "immaculate conception,epiphany,three kings day,valentine's day,mother's day,father's day,halloween,"
    "groundhog day,earth day,flag day,arbor day,emancipation day,constitution day,national day,reformation day,"
    "german unity day,bastille day,shrove tuesday,international women's day,women's day,workers' day,"
    "children's day,teachers' day,st. andrew's day,st. david's day,st. george's day,burns night,guy fawkes night,"
    "neujahr,karfreitag,ostermontag,pfingstmontag,christi himmelfahrt,tag der arbeit,tag der deutschen einheit,"
    "fronleichnam,allerheiligen,weihnachten,heiligabend,silvester,jour de l'an,lundi de paques,fete du travail,"
    "fete nationale,toussaint,noel,armistice,ano nuevo,viernes santo,dia del trabajo,navidad,capodanno,"
    "pasquetta,ferragosto,natale,santo stefano,epifania"
)
# Halloween, Christmas, Easter and Epiphany are also titles of films, songs and books, and Assumption, Corpus
# Christi and Armistice are places and treaties: they count only in a field named after the holiday.
HOLIDAYS_SPECIFIC = HOLIDAYS - _words(
    "halloween,christmas,easter,epiphany,pentecost,passover,assumption,corpus christi,armistice,noel,natale,"
    "navidad,weihnachten,toussaint,silvester,may day,national day,family day,women's day,children's day,"
    "teachers' day,mardi gras,black friday,earth day,kwanzaa,diwali,whitsun"
)
_OBSERVED = re.compile(r"(?i)\s*[-–(]?\s*(?:observed|obs\.?|\(observed\))\s*\)?$")


def _holiday(value):
    v = _OBSERVED.sub("", _clean(value))
    return fold(v.replace("’", "'"))


def validate_holiday(value):
    """The name of a public holiday or an observance: New Year's Day, Martin Luther King, Jr. Day, Memorial Day,
    Independence Day, Labor Day, Thanksgiving Day, Christmas Day, Good Friday, Boxing Day, Victoria Day, Easter
    Monday, Labor Day (observed), Tag der Arbeit (not Monday, July 4 or Spring Break)."""
    return _holiday(value) in HOLIDAYS


def validate_holiday_value(value):
    """A holiday that is no title or place: Labor Day, Memorial Day, Thanksgiving Day, Christmas Day, Good Friday
    (not Christmas, Easter or Halloween alone, which count only in a field named after the holiday)."""
    return _holiday(value) in HOLIDAYS_SPECIFIC


# ------------------------------------------------------------------ relationship to the head of a household
HOUSEHOLD_RELATIONS = _words(
    "head,head of household,householder,self,wife,husband,spouse,partner,unmarried partner,son,daughter,dau,"
    "child,stepson,step-son,step son,stepdaughter,step-daughter,step daughter,stepchild,adopted son,"
    "adopted daughter,adopted child,foster son,foster daughter,foster child,son-in-law,son in law,"
    "daughter-in-law,daughter in law,father,mother,father-in-law,father in law,mother-in-law,mother in law,"
    "stepfather,stepmother,brother,sister,brother-in-law,brother in law,bro-in-law,sister-in-law,sister in law,"
    "grandson,granddaughter,granddau,grandchild,grandfather,grandmother,grandparent,great grandson,"
    "great granddaughter,uncle,aunt,nephew,niece,cousin,servant,boarder,lodger,visitor,roomer,inmate,patient,"
    "employee,apprentice,hired man,hired girl,hired hand,housekeeper,nurse,companion,ward,roommate,"
    "other relative,nonrelative,stepbrother,stepsister,half brother,half sister,gr son,gr dau,niece-in-law,"
    "nephew-in-law,step grandson,step granddaughter,parent,"
    # abbreviations and spellings of census takers and transcribers
    "daur,hus,husb,gdau,gson,grandau,granddaur,stepdau,step dau,dau-in-law,dau in law,s-in-law,d-in-law,neice,"
    "serv,servt,svt,sis,bro,bdr,brdr"
)
# Head, Self, Partner, Patient, Employee and Nurse are as common in other columns as in a household, and
# Brother is a brand of printers: they count only in a field named after the relationship.
HOUSEHOLD_RELATIONS_SPECIFIC = HOUSEHOLD_RELATIONS - _words(
    "head,self,partner,child,visitor,patient,employee,nurse,companion,ward,inmate,apprentice,housekeeper,roommate,"
    "head of household,brother,parent,hus,serv,sis,bro,bdr"
)


def validate_household_relationship(value):
    """The relationship of a person to the head of the household, as census records and their transcriptions give
    it: Head, Wife, Son, Daughter, Dau, Servant, Boarder, Lodger, Son-in-law, Granddaughter, Nephew (not Director,
    Friendship or 32)."""
    return fold(_clean(value).rstrip(".")) in HOUSEHOLD_RELATIONS


def validate_household_relationship_value(value):
    """A relationship that is a word of kinship or of a household: Wife, Son, Daughter, Servant, Boarder, Lodger,
    Mother-in-law (not Head, Self or Partner, which count only in a field named after the relationship)."""
    return fold(_clean(value).rstrip(".")) in HOUSEHOLD_RELATIONS_SPECIFIC


# ------------------------------------------------------------------ grade spans of schools
_GRADE = r"(?:pk|p-?k|pre-?k|pre-?kindergarten|prek|tk|ee|k|kg|kn|k4|k5|kindergarten|0?[1-9]|1[0-3])"
_GRADE_SPAN = re.compile(rf"(?i)^(?:grades?\s+|gr\.?\s*)?({_GRADE})\s*(?:[-–—]|to|through|thru)\s*({_GRADE})$")
_GRADE_LETTER = re.compile(r"(?i)[a-z]")


def _grade_rank(grade):
    g = grade.lower().replace("-", "")
    return -1 if g in ("pk", "prek", "prekindergarten", "tk", "ee", "k4") else 0 if g.startswith("k") else int(g)


def validate_grade_span(value):
    """The grades a school teaches, from the lowest to the highest: K-5, 6-8, 9-12, PK-8, KG - 05, K-12, Pre-K to
    5, Grades 7-12 (not 12-9, 5-6-7 or A-F)."""
    m = _GRADE_SPAN.match(_clean(value))
    return bool(m) and _grade_rank(m.group(1)) <= _grade_rank(m.group(2))


def validate_grade_span_value(value):
    """A grade span that starts or ends with a kindergarten grade: K-5, PK-8, KG - 12, Pre-K - 5 (9-12 and 6-8
    count only in a field named Grades, since they are also scores and ranges)."""
    m = _GRADE_SPAN.match(_clean(value))
    return bool(m) and validate_grade_span(value) and bool(
        _GRADE_LETTER.search(m.group(1)) or _GRADE_LETTER.search(m.group(2)))


# ------------------------------------------------------------------ meeting days of classes
_DAY_LETTER = r"(?:M|Tu|TU|T|W|R|Th|TH|F|Sa|SA|Su|SU|S|U)"
_MEETING_DAYS = re.compile(rf"^{_DAY_LETTER}(?:[\s,/&-]*{_DAY_LETTER}){{0,6}}$")


def validate_class_meeting_days(value):
    """The days of the week a class meets, in the letters of US college schedules: MWF, TR, TTh, MW, MTWRF, M W F,
    Tu, Th, M, T (not Monday, Mon, TBA or 13)."""
    v = _clean(value)
    return bool(_MEETING_DAYS.match(v))


# ------------------------------------------------------------------ IOC country codes
IOC_CODES = set(
    "AFG ALB ALG AND ANG ANT ARG ARM ARU ASA AUS AUT AZE BAH BAN BAR BDI BEL BEN BER BHU BIH BIZ BLR BOL BOT BRA BRN "
    "BRU BUL BUR CAF CAM CAN CAY CGO CHA CHI CHN CIV CMR COD COK COL COM CPV CRC CRO CUB CYP CZE DEN DJI DMA DOM ECU "
    "EGY ERI ESA ESP EST ETH FIJ FIN FRA FSM GAB GAM GBR GBS GEO GEQ GER GHA GRE GRN GUA GUI GUM GUY HAI HKG HON HUN "
    "INA IND IRI IRL IRQ ISL ISR ISV ITA IVB JAM JOR JPN KAZ KEN KGZ KIR KOR KOS KSA KUW LAO LAT LBA LBN LBR LCA LES "
    "LIE LTU LUX MAD MAR MAS MAW MDA MDV MEX MGL MHL MKD MLI MLT MNE MON MOZ MRI MTN MYA NAM NCA NED NEP NGR NIG NOR "
    "NRU NZL OMA PAK PAN PAR PER PHI PLE PLW PNG POL POR PRK PUR QAT ROU RSA RUS RWA SAM SEN SEY SGP SKN SLE SLO SMR "
    "SOL SOM SRB SRI SSD STP SUD SUI SUR SVK SWE SWZ SYR TAN TGA THA TJK TKM TLS TOG TPE TTO TUN TUR TUV UAE UGA UKR "
    "URU USA UZB VAN VEN VIE VIN YEM ZAM ZIM "
    # codes of former and of special teams: the Soviet Union, the Unified Team, East and West Germany,
    # Czechoslovakia, Yugoslavia, Serbia and Montenegro, Romania and Singapore before 2006 and 2016, the Netherlands
    # Antilles, Lebanon before 2016, independent and refugee athletes
    "URS EUN GDR FRG TCH YUG SCG ROM SIN AHO LIB IOA EOR ROC OAR AIN ZAI BIR CEY RHO ANZ BOH TMP".split()
)


def validate_ioc_country_code(value):
    """The three-letter code of a National Olympic Committee: USA, GER, NED, SUI, RSA, CRO, TPE, INA, URS (not Ger,
    DEU, NLD or USSR)."""
    return text(value) in IOC_CODES


# ------------------------------------------------------------------ errno names
ERRNO_NAMES = set(
    "E2BIG EACCES EADDRINUSE EADDRNOTAVAIL EAFNOSUPPORT EAGAIN EALREADY EBADF EBADMSG EBUSY ECANCELED ECHILD "
    "ECONNABORTED ECONNREFUSED ECONNRESET EDEADLK EDESTADDRREQ EDOM EDQUOT EEXIST EFAULT EFBIG EHOSTUNREACH EIDRM "
    "EILSEQ EINPROGRESS EINTR EINVAL EIO EISCONN EISDIR ELOOP EMFILE EMLINK EMSGSIZE EMULTIHOP ENAMETOOLONG ENETDOWN "
    "ENETRESET ENETUNREACH ENFILE ENOBUFS ENODATA ENODEV ENOENT ENOEXEC ENOLCK ENOLINK ENOMEM ENOMSG ENOPROTOOPT "
    "ENOSPC ENOSR ENOSTR ENOSYS ENOTCONN ENOTDIR ENOTEMPTY ENOTRECOVERABLE ENOTSOCK ENOTSUP ENOTTY ENXIO EOPNOTSUPP "
    "EOVERFLOW EOWNERDEAD EPERM EPIPE EPROTO EPROTONOSUPPORT EPROTOTYPE ERANGE EROFS ESPIPE ESRCH ESTALE ETIME "
    "ETIMEDOUT ETXTBSY EWOULDBLOCK EXDEV "
    # Linux and BSD
    "ENOTBLK ECHRNG EL2NSYNC EL3HLT EL3RST ELNRNG EUNATCH ENOCSI EL2HLT EBADE EBADR EXFULL ENOANO EBADRQC EBADSLT "
    "EBFONT ENONET ENOPKG EREMOTE EADV ESRMNT ECOMM EDOTDOT ENOTUNIQ EBADFD EREMCHG ELIBACC ELIBBAD ELIBSCN ELIBMAX "
    "ELIBEXEC ERESTART ESTRPIPE EUSERS ESOCKTNOSUPPORT EPFNOSUPPORT ESHUTDOWN ETOOMANYREFS EHOSTDOWN EUCLEAN ENOTNAM "
    "ENAVAIL EISNAM EREMOTEIO ENOMEDIUM EMEDIUMTYPE ENOKEY EKEYEXPIRED EKEYREVOKED EKEYREJECTED ERFKILL EHWPOISON "
    "EDEADLOCK EPROCLIM EBADRPC ERPCMISMATCH EPROGUNAVAIL EPROGMISMATCH EPROCUNAVAIL EFTYPE EAUTH ENEEDAUTH ENOATTR "
    "EDOOFUS ENOTCAPABLE ECAPMODE EINTEGRITY".split()
)


def validate_errno_name(value):
    """A symbolic name of errno.h: ENOENT, EACCES, EAGAIN, EINVAL, ETIMEDOUT, E2BIG, ECONNREFUSED (not enoent,
    ERROR or EOF)."""
    return text(value).rstrip(":") in ERRNO_NAMES


# ================================================================== seven more segments of the corpus
# Seven more segments of the crawl (5 778 000 tables of pages on 109 005 hosts): seasons of sports leagues (2013-14),
# types of dwellings, age groups of youth sports (U12), names of Dublin Core elements (dc.date.issued), keyboard
# shortcuts (Ctrl+C), Exif tags of photos, branches of the armed forces, stock market indexes, stock exchanges,
# betting odds (9-2, 5/1), types of crimes and crops.

# The word lists are split at commas, so no entry holds one ("coffee, green" would add green), and an entry folds to
# its letters and digits (b&e would be be, a code of Belgium).

# ------------------------------------------------------------------ seasons of sports leagues
_SEASON = re.compile(r"^((?:18|19|20)\d{2})(?:\s?[-–—/]\s?((?:18|19|20)?\d{2}))?$")


def validate_sports_season(value):
    """The season of a league or a competition: 2013-14, 1999-00, 2014–15, 2013/2014, 2013/14, or one year, 2015
    (not 2013-15, 2015-14, Summer, Career or 13-14)."""
    m = _SEASON.match(_clean(value))
    if not m:
        return False
    start, end = int(m.group(1)), m.group(2)
    if end is None:
        return True
    if len(end) == 2:
        return int(end) == (start + 1) % 100
    return int(end) == start + 1


# ------------------------------------------------------------------ types of dwellings
DWELLING_TYPES = _words(
    "detached,semi-detached,semi detached,semidetached,semi,terraced,terrace,terraced house,terrace house,"
    "mid terrace,mid-terrace,mid terraced,end terrace,end-terrace,end of terrace,end terraced,link detached,"
    "link-detached,flat,flats,flat/maisonette,maisonette,flat/apartment,apartment,apartments,apartment/condo,"
    "bungalow,detached bungalow,semi-detached bungalow,detached house,semi-detached house,house,houses,"
    "townhouse,townhouses,town house,townhome,townhomes,condo,condos,condominium,condominiums,condo/townhouse,"
    "condo/townhome,townhouse/condo,co-op,coop,cooperative,single family,single-family,single family home,"
    "single-family home,single family residence,single family residential,single family detached,"
    "single-family detached,single family attached,sfr,sfh,multi-family,multifamily,multi family,multi-family home,"
    "duplex,triplex,fourplex,quadplex,mobile home,mobile homes,manufactured home,manufactured,mobile/manufactured,"
    "manufactured/mobile,park home,studio,loft,penthouse,villa,villas,cottage,chalet,cabin,farmhouse,row house,"
    "rowhouse,rowhome,row home,patio home,cluster home,multi storey flat,multi-storey flat,high rise flat,"
    "low rise flat,bedsit,bedsits,maison,appartement,wohnung,einfamilienhaus,reihenhaus,"
    "doppelhaushalfte,vrijstaand,twee-onder-een-kap,tussenwoning,hoekwoning,appartamento,villetta,piso,chalet adosado"
)
# House, Flat, Apartment, Studio, Villa, Cottage, Cabin, Loft and Semi are also other things (the House of a
# legislature, a flat finish, film studios, football clubs, a cabin class) and Detached and Duplex are also states
# of processes and printers: they count only in a field named after the dwelling.
DWELLING_TYPES_SPECIFIC = DWELLING_TYPES - _words(
    "detached,semi,terrace,flat,flats,apartment,apartments,house,houses,studio,loft,penthouse,villa,villas,cottage,"
    "chalet,cabin,farmhouse,duplex,triplex,manufactured,co-op,coop,cooperative,condo,condos,maison,appartement,"
    "wohnung,piso,appartamento,sfr,sfh"
)


def validate_dwelling_type(value):
    """The type of a dwelling: Detached, Semi-detached, Terraced, Flat/Maisonette, Bungalow, Single Family, Condo,
    Townhouse, Apartment, Mobile Home, Duplex, House (not Commercial, Residential, Land or 3 Bedroom)."""
    return fold(_clean(value)) in DWELLING_TYPES


def validate_dwelling_type_value(value):
    """A type of dwelling that is no other word: Semi-detached, Terraced, End Terrace, Flat/Maisonette, Townhouse,
    Condominium, Single Family, Mobile Home (not House, Flat, Apartment, Studio, Villa, Detached or Duplex alone)."""
    return fold(_clean(value)) in DWELLING_TYPES_SPECIFIC


# ------------------------------------------------------------------ age groups of youth sports
_SEX = r"(?:boys|girls|men|women|men's|women's|mens|womens|male|female|mixed|coed|co-ed|b|g)"
_AGE_GROUP_U = re.compile(rf"(?i)^(?:{_SEX}\s?)?u\s?-?\s?(\d{{1,2}})(?:\s?{_SEX})?$|^(\d{{1,2}})\s?u(?:\s?{_SEX})?$")
_AGE_GROUP_WORDS = re.compile(rf"(?i)^(?:{_SEX}\s)?(?:under|under-)\s?-?\s?(\d{{1,2}})s?(?:\s{_SEX})?$|"
                              r"^(\d{1,2})\s?(?:&|and)\s?(?:under|u)$")


def validate_sports_age_group(value):
    """The age group of a youth team or competition: U12, U-14, U 8, 12U, U12 Boys, Girls U14, BU10, Under 16,
    Under-12, 10 & Under (not U, 12, 18-24, U2B or Under 200)."""
    v = _clean(value)
    m = _AGE_GROUP_U.match(v) or _AGE_GROUP_WORDS.match(v)
    if not m:
        return False
    age = int(next(g for g in m.groups() if g))
    return 4 <= age <= 23


def validate_sports_age_group_value(value):
    """An age group with the U of youth sports: U10 to U23, U12 Boys, U19 Girls, and 10U to 19U (not U6 to U9,
    which are also lines of an underground, U2, Under 16, also an age band of surveys, or 22U and 42U, the heights
    of racks in rack units)."""
    m = _AGE_GROUP_U.match(_clean(value))
    if not m:
        return False
    if m.group(1):
        return 10 <= int(m.group(1)) <= 23
    return 10 <= int(m.group(2)) <= 19


# ------------------------------------------------------------------ Dublin Core elements
DUBLIN_CORE_ELEMENTS = {
    "title", "creator", "subject", "description", "publisher", "contributor", "date", "type", "format", "identifier",
    "source", "language", "relation", "coverage", "rights",
    # the terms of the DCMI namespace (dcterms) that are not among the fifteen elements, in lower case
    "abstract", "accessrights", "accrualmethod", "accrualperiodicity", "accrualpolicy", "alternative", "audience",
    "available", "bibliographiccitation", "conformsto", "created", "dateaccepted", "datecopyrighted",
    "datesubmitted", "educationlevel", "extent", "hasformat", "haspart", "hasversion", "instructionalmethod",
    "isformatof", "ispartof", "isreferencedby", "isreplacedby", "isrequiredby", "issued", "isversionof", "license",
    "mediator", "medium", "modified", "provenance", "references", "replaces", "requires", "rightsholder", "spatial",
    "tableofcontents", "temporal", "valid",
    # elements that DSpace adds to its dc schema
    "embargo", "thesis",
}
_DUBLIN_CORE = re.compile(r"^(?i:dc|dcterms|dct)[.:]([A-Za-z]+)((?:\.[A-Za-z]+){0,2})(?:\[[A-Za-z_-]*\])?$")


def validate_dublin_core_element(value):
    """The name of a Dublin Core element, in the dotted notation of DSpace and other repositories or with a
    namespace prefix: dc.title, dc.date.issued, dc.contributor.author, dc.identifier.uri, dc.description.abstract,
    dc:creator, dcterms:created, dc.title[en_US] (not dc, dc.foo, Title or dc_title)."""
    m = _DUBLIN_CORE.match(text(value))
    return bool(m) and m.group(1).lower() in DUBLIN_CORE_ELEMENTS


# ------------------------------------------------------------------ keyboard shortcuts
_MODIFIER = (r"(?:ctrl|control|ctl|strg|alt|alt\s?gr|option|opt|shift|umschalt|cmd|command|meta|super|win|windows|"
             r"fn|⌘|⌥|⇧|⌃|⎇)")
_KEY = (r"(?:f(?:[1-9]|1\d|2[0-4])|enter|return|tab|esc|escape|space|spacebar|space\s?bar|delete|del|backspace|"
        r"home|end|pg\s?up|pg\s?dn|page\s?up|page\s?down|insert|ins|(?:up|down|left|right)(?:\s?arrow)?|"
        r"(?:arrow\s?)?(?:up|down|left|right)|print\s?screen|prt\s?sc|pause|break|caps\s?lock|num\s?lock|"
        r"scroll\s?lock|plus|minus|comma|period|menu|click|left\s?click|right\s?click|drag|scroll|wheel|"
        r"mouse\s?wheel|num\s?[0-9+*/-]|[^\s+])")
_SHORTCUT = re.compile(rf"(?i)^(?:{_MODIFIER}\s?[+-]\s?)+{_KEY}$|^[⌘⌥⇧⌃]+\s?{_KEY}$")
_EMACS = re.compile(r"^(?:(?:[CMs]-)+(?:[^\s]|<?[a-z]+>?))(?:\s(?:[CMs]-)*(?:[^\s]|<?[a-z]+>?))?$")
_SINGLE_KEY = re.compile(rf"(?i)^{_KEY}$")
_SEQUENCE = re.compile(r"\s*(?:,|\bthen\b|\bfollowed by\b|;)\s*|(?<![+\-\s])\s+(?=(?:ctrl|alt|shift|cmd)\b)", re.I)


def _combos(value):
    return [p for p in _SEQUENCE.split(_clean(value)) if p and p.strip()]


def validate_keyboard_shortcut(value):
    """A key or a combination of keys: Ctrl+C, Alt+F4, Shift + Tab, Cmd+Shift+S, ⌘S, Ctrl-X, Ctrl+K, Ctrl+C, C-x
    C-f and M-x of Emacs, F1, Esc, Home (not Copy, Ctrl or +)."""
    parts = _combos(value)
    return bool(parts) and all(_SHORTCUT.match(p) or _EMACS.match(p) or _SINGLE_KEY.match(p) for p in parts)


def validate_keyboard_shortcut_value(value):
    """A combination with a modifier key named in words or by its symbol: Ctrl+C, Alt + F4, Shift+Tab, Cmd-Shift-S,
    ⌘⇧S, Ctrl+K, Ctrl+C (not C-x, M-F or F1 alone, which count only in a field named Shortcut or Hotkey)."""
    parts = _combos(value)
    return bool(parts) and all(_SHORTCUT.match(p) for p in parts)


# ------------------------------------------------------------------ Exif tags
EXIF_TAGS = _words(
    "make,model,camera make,camera model,camera model name,camera,lens,lens model,lens make,lens info,"
    "lens specification,lens id,software,artist,copyright,orientation,x resolution,y resolution,xresolution,"
    "yresolution,resolution unit,date/time,datetime,date time,date and time,date/time original,date time original,"
    "datetimeoriginal,date/time digitized,date time digitized,datetimedigitized,date and time (original),"
    "date and time (digitized),date taken,create date,modify date,exposure time,exposure,shutter speed,"
    "shutter speed value,shutterspeedvalue,f-number,fnumber,f number,f-stop,aperture,aperture value,aperturevalue,"
    "max aperture value,max aperture,maximum lens aperture,exposure program,exposureprogram,iso,iso speed,"
    "iso speed ratings,iso speed rating,isospeedratings,photographic sensitivity,exif version,exifversion,"
    "flashpix version,components configuration,compressed bits per pixel,brightness value,brightness,"
    "exposure bias,exposure bias value,exposurebiasvalue,exposure compensation,metering mode,meteringmode,"
    "light source,lightsource,flash,flash used,focal length,focallength,focal length in 35mm film,"
    "focal length in 35mm format,focal length (35mm format),focal length (35mm),focal length 35mm,"
    "focallengthin35mmfilm,35mm focal length,subject distance,subject distance range,subject area,color space,"
    "colour space,colorspace,pixel x dimension,pixel y dimension,exif image width,exif image height,"
    "exif image length,image width,image height,image length,sensing method,file source,scene type,custom rendered,"
    "exposure mode,exposuremode,white balance,whitebalance,digital zoom ratio,digital zoom,scene capture type,"
    "scenecapturetype,gain control,contrast,saturation,sharpness,ycbcr positioning,ycbcrpositioning,compression,"
    "interoperability index,interoperability version,gps latitude,gps longitude,gps altitude,gps latitude ref,"
    "gps longitude ref,gps altitude ref,gps version id,gps time stamp,gps date stamp,gps img direction,"
    "image description,user comment,maker note,makernote,sub sec time,subsec time original,"
    "focal plane x resolution,focal plane y resolution,focal plane resolution unit,exposure index,cfa pattern,"
    "image unique id,body serial number,camera serial number,serial number,owner name,camera owner name,"
    "flash energy,spectral sensitivity,subject location,thumbnail offset,thumbnail length,exif offset,"
    "exif ifd pointer,gps info ifd pointer"
)
# Make, Model, Software, Artist, Copyright, Orientation, Flash, ISO, Contrast, Saturation, Sharpness and the
# dates are also the names of other fields: a column of Exif tags needs the tags of photography itself.
EXIF_TAGS_SPECIFIC = EXIF_TAGS - _words(
    "make,model,camera,lens,software,artist,copyright,orientation,date/time,datetime,date time,date and time,"
    "date taken,create date,modify date,exposure,shutter speed,aperture,iso,brightness,flash,contrast,saturation,"
    "sharpness,compression,image width,image height,image length,image description,serial number,digital zoom,"
    "camera make,camera model,lens model,lens make,owner name,user comment"
)


def _exif_tag(value):
    return fold(_clean(text(value).rstrip(":")))


def validate_exif_tag(value):
    """The name of a tag of the Exif metadata of a photo: Make, Model, Exposure Time, F-Number, ISO Speed Ratings,
    Focal Length, Metering Mode, Flash, Exposure Bias Value, Color Space, Date/Time Original, White Balance (not
    1/60 sec, f/5.6 or Canon)."""
    return _exif_tag(value) in EXIF_TAGS


def validate_exif_tag_value(value):
    """An Exif tag that is no other field name: Exposure Time, Exposure Program, Metering Mode, Focal Length,
    Shutter Speed Value, Aperture Value, Exposure Bias Value, Color Space, White Balance (not Make, Model, Flash,
    ISO, Software or Date/Time alone)."""
    return _exif_tag(value) in EXIF_TAGS_SPECIFIC


# ------------------------------------------------------------------ branches of the armed forces
MILITARY_BRANCHES = _words(
    "army,navy,air force,marine corps,marines,marine,usmc,coast guard,uscg,space force,ussf,national guard,"
    "army national guard,air national guard,arng,ang,army reserve,usar,navy reserve,naval reserve,usnr,"
    "air force reserve,usafr,marine corps reserve,usmcr,coast guard reserve,uscgr,us army,u.s. army,united states army,"
    "us navy,u.s. navy,united states navy,us air force,u.s. air force,united states air force,us marine corps,"
    "u.s. marine corps,united states marine corps,us coast guard,u.s. coast guard,united states coast guard,usa,usn,"
    "usaf,merchant marine,us merchant marine,u.s. merchant marine,army air forces,army air corps,usaaf,"
    "us army air forces,public health service,noaa corps,royal navy,royal air force,raf,british army,royal marines,"
    "royal canadian navy,royal canadian air force,rcaf,canadian army,royal australian navy,ran,"
    "royal australian air force,raaf,australian army,royal new zealand navy,royal new zealand air force,"
    "new zealand army,bundeswehr,heer,luftwaffe,marine nationale,armee de terre,armee de l'air,"
    "army/navy,navy/marine corps,army & navy,air force reserve command,army nat'l guard,air nat'l guard"
)
# Army, Navy, Air Force and Marines are also teams of the service academies in college sports, USA, RAN and ANG
# are also codes of countries, and Marine and Heer are also words: they count only in a field named Branch.
MILITARY_BRANCHES_SPECIFIC = MILITARY_BRANCHES - _words(
    "army,navy,air force,marines,marine,usa,ran,ang,raf,heer,luftwaffe,army/navy,army & navy,arng"
)


def validate_military_branch(value):
    """A branch of the armed forces: Army, Navy, Air Force, Marine Corps, Coast Guard, USMC, USN, USAF, Army
    National Guard, Navy Reserve, U.S. Army, Royal Navy, RAF (not Police, Fire or Infantry)."""
    return fold(_clean(value)) in MILITARY_BRANCHES


def validate_military_branch_value(value):
    """A branch of the armed forces that is no team or other word: Marine Corps, Coast Guard, USMC, USAF, USCG,
    Army National Guard, U.S. Navy, Royal Navy (not Army, Navy, Air Force, Marines or USA alone)."""
    return fold(_clean(value)) in MILITARY_BRANCHES_SPECIFIC


# ------------------------------------------------------------------ stock market indexes
STOCK_INDEXES = _words(
    "s&p 500,s&p500,s&p 500 index,sp500,s&p 400,s&p midcap 400,s&p 600,s&p smallcap 600,s&p 100,s&p 1500,"
    "s&p/tsx composite,s&p/tsx composite index,s&p/tsx,s&p/tsx 60,tsx composite,s&p/asx 200,asx 200,s&p/asx 50,"
    "all ordinaries,s&p/nzx 50,nzx 50,dow jones industrial average,dow jones industrials,dow jones industrial,"
    "dow jones industrial avg,djia,dow,the dow,dow 30,dow jones,dow jones transportation average,"
    "dow jones transportation,dow jones transports,dow jones utilities,dow jones utility average,dow jones composite,"
    "dow jones us total stock market,nasdaq composite,nasdaq composite index,nasdaq,nasdaq 100,nasdaq-100,"
    "nasdaq 100 index,nyse composite,nyse composite index,amex composite,russell 1000,russell 2000,russell 3000,"
    "russell 2000 index,wilshire 5000,value line,vix,cboe volatility index,ftse 100,ftse 250,ftse 350,"
    "ftse all-share,ftse all share,ftse mib,ftse 100 index,dax,dax 30,dax index,mdax,sdax,tecdax,cac 40,cac40,"
    "ibex 35,ibex,aex,bel 20,smi,swiss market index,atx,psi 20,psi-20,omx stockholm 30,omxs30,omx copenhagen 20,"
    "omxc20,omx helsinki 25,omxh25,obx,iseq,iseq overall,wig,wig20,wig 20,px,bux,rts,rts index,micex,moex,"
    "moex russia index,bist 100,xu100,ise 100,ta-35,ta-25,nikkei 225,nikkei,nikkei 225 index,topix,hang seng,"
    "hang seng index,hsi,shanghai composite,shanghai composite index,sse composite,sse composite index,"
    "shenzhen component,szse component,csi 300,kospi,kospi composite,kosdaq,taiex,sti,straits times,"
    "straits times index,klci,ftse bursa malaysia klci,set,set index,jci,jakarta composite,psei,sensex,"
    "s&p bse sensex,bse sensex,bse 30,nifty 50,nifty,cnx nifty,s&p cnx nifty,bovespa,ibovespa,ipc,s&p/bmv ipc,"
    "merval,ipsa,igbvl,colcap,euro stoxx 50,euro stoxx,stoxx 50,stoxx europe 50,stoxx europe 600,stoxx 600,"
    "msci world,msci eafe,msci emerging markets,msci em,msci acwi,msci all country world,msci europe,"
    "jse top 40,ftse/jse all share,jse all share,egx 30,tasi,qe index,dfm general index,ads index"
)
# Dow, Nasdaq, DAX, SMI, AEX, ATX, IPC, SET, STI, PX, WIG, RTS, VIX, OBX, BUX, HSI, JCI, IBEX and Nifty alone are
# also a company, exchanges, tickers and words: they count only in a field named Index.
STOCK_INDEXES_SPECIFIC = STOCK_INDEXES - _words(
    "dow,the dow,dow jones,nasdaq,dax,smi,aex,atx,ipc,set,sti,px,wig,rts,vix,obx,bux,hsi,jci,ibex,nifty,value line,"
    "moex,micex,kosdaq,euro stoxx,iseq,bovespa"
)


def validate_stock_market_index(value):
    """A stock market index: S&P 500, Dow Jones Industrial Average, DJIA, Dow, Nasdaq Composite, Nasdaq-100, Russell
    2000, FTSE 100, DAX, CAC 40, Nikkei 225, Hang Seng, Euro Stoxx 50, Bovespa (not AAPL, NYSE or 2,093.25)."""
    return fold(_clean(value)) in STOCK_INDEXES


def validate_stock_market_index_value(value):
    """A stock market index named with its number or in words: S&P 500, Dow Jones Industrials, Nasdaq Composite,
    FTSE 100, CAC 40, Nikkei 225, Hang Seng, Russell 2000 (not Dow, Nasdaq, DAX, SMI or SET alone)."""
    return fold(_clean(value)) in STOCK_INDEXES_SPECIFIC


# ------------------------------------------------------------------ stock exchanges
STOCK_EXCHANGES = _words(
    "nyse,new york stock exchange,new york stock exchange inc.,nyse mkt,nyse american,nyse amex,amex,"
    "american stock exchange,nyse arca,nysearca,nyse euronext,nasdaq,nasdaqgs,nasdaqgm,nasdaqcm,nasdaq gs,nasdaq gm,"
    "nasdaq cm,nasdaq global select,nasdaq global select market,nasdaq global market,nasdaq capital market,"
    "nasdaq stock market,nasdaq omx,nasdaq nms,nasdaq smallcap,otc,otcbb,otc bb,otc markets,otcqx,otcqb,otc pink,"
    "otc pink sheets,pink sheets,pink,pnk,otcmkts,otc markets group,bats,bats europe,bats global markets,cboe,"
    "chicago board options exchange,cbot,chicago board of trade,cme,chicago mercantile exchange,cme group,nymex,"
    "comex,ice,ice futures,ice futures us,ice futures europe,lse,london stock exchange,aim,lse aim,tsx,"
    "toronto stock exchange,tsxv,tsx-v,tsx venture,tsx venture exchange,cse,canadian securities exchange,cnsx,asx,"
    "australian securities exchange,australian stock exchange,nzx,jse,johannesburg stock exchange,bse,"
    "bombay stock exchange,nse,national stock exchange,national stock exchange of india,sgx,singapore exchange,hkex,"
    "hkse,hong kong stock exchange,hong kong exchanges,sehk,sse,shanghai stock exchange,szse,shenzhen stock exchange,"
    "tse,tokyo stock exchange,jpx,japan exchange group,osaka securities exchange,krx,korea exchange,"
    "korea exchange (stock market),kosdaq,twse,taiwan stock exchange,euronext,euronext paris,euronext amsterdam,"
    "euronext brussels,euronext lisbon,nyse euronext - euronext paris,xetra,frankfurt,frankfurt stock exchange,fwb,"
    "deutsche borse,borse frankfurt,boerse frankfurt,berlin,stuttgart,munich,muenchen,munchen,dusseldorf,hamburg,"
    "six,six swiss exchange,swx,swiss exchange,borsa italiana,borsa italiana s.p.a.,bme,madrid stock exchange,"
    "bolsa de madrid,omx,nasdaq stockholm,nasdaq copenhagen,nasdaq helsinki,nasdaq omx stockholm,oslo bors,"
    "oslo stock exchange,wse,warsaw stock exchange,gpw,moex,micex,moscow exchange,bist,borsa istanbul,"
    "istanbul stock exchange,tase,tel aviv stock exchange,bmv,mexican stock exchange,bolsa mexicana de valores,"
    "bovespa,b3,bm&fbovespa,bcba,buenos aires stock exchange,eurex,lme,london metal exchange,ise,irish stock exchange"
)
# OTC, AIM, ICE, CSE, BSE, NSE, TSE, SSE, ISE, SIX, Pink, AMEX, LSE, BATS, CME and the names of cities are also
# words, cards, schools, courses and places, ASX and TSX are also models of cars (Mitsubishi ASX, Acura TSX), and
# Bovespa, MOEX and KOSDAQ are also indexes: they count only in a field named Exchange.
STOCK_EXCHANGES_SPECIFIC = STOCK_EXCHANGES - _words(
    "otc,aim,ice,cse,bse,nse,tse,sse,ise,six,pink,pnk,amex,lse,bats,kosdaq,frankfurt,berlin,stuttgart,munich,muenchen,"
    "munchen,dusseldorf,hamburg,omx,b3,bme,bist,cme,wse,fwb,bovespa,moex,micex,jse,bmv,bcba,gpw,swx,krx,jpx,tase,asx,"
    "tsx"
)


def validate_stock_exchange(value):
    """A stock, futures or options exchange: NYSE, NASDAQ, NYSE MKT, NYSE Arca, OTCBB, OTC Markets, London Stock
    Exchange, AIM, TSX, ASX, Xetra, Euronext Paris, CME, NYMEX, Frankfurt (not New York, S&P 500 or Bitstamp)."""
    return fold(_clean(value)) in STOCK_EXCHANGES


def validate_stock_exchange_value(value):
    """An exchange that is no word, city or other code: NYSE, NASDAQ, NYSE MKT, NYSE Arca, OTCBB, OTCQB, London
    Stock Exchange, Toronto Stock Exchange, Euronext Paris (not OTC, AIM, ICE, BSE, AMEX or Frankfurt alone)."""
    return fold(_clean(value)) in STOCK_EXCHANGES_SPECIFIC


# ------------------------------------------------------------------ betting odds
_ODDS = re.compile(r"(?i)^(?:(\d{1,3})\s?[/-]\s?(\d{1,3})|evs|evens|even|evn|ev)(?:\s?(?:f|jf|cf|fav|\*))?$")
_MONEYLINE = re.compile(r"^[+-]\d{3,5}$")
# Odds on, where the stake is larger than the win, are a short list of fractions; other fractions with the larger
# number second are sizes of clothes and socks (12/14, 35-38, 9-13 under M/L).
ODDS_ON = {(1, 100), (1, 50), (1, 33), (1, 25), (1, 20), (1, 16), (1, 14), (1, 12), (1, 10), (1, 9), (1, 8),
           (1, 7), (1, 6), (1, 5), (2, 11), (2, 9), (1, 4), (2, 7), (3, 10), (1, 3), (4, 11), (2, 5), (4, 9), (1, 2),
           (8, 15), (4, 7), (8, 13), (4, 6), (8, 11), (4, 5), (5, 6), (10, 11), (3, 5), (3, 4), (5, 8), (2, 3),
           (5, 7), (9, 10), (7, 10), (5, 9), (3, 8)}


def validate_betting_odds(value):
    """The odds of a bet: fractional odds of race cards and bookmakers (9-2, 5/1, 100/30, 11/10, 2-5, Evs, 9/4F) or
    the American moneyline (+150, -110) (not 0-0, 2015-16, 1/0 or 2.50)."""
    v = _clean(value)
    m = _ODDS.match(v)
    if m:
        if m.group(1) is None:
            return True
        num, den = int(m.group(1)), int(m.group(2))
        if num >= den:
            return den > 0 and den <= 100
        return (num, den) in ODDS_ON
    return bool(_MONEYLINE.match(v)) and abs(int(v)) >= 100


# ------------------------------------------------------------------ types of crimes
CRIME_TYPES = _words(
    "murder,homicide,criminal homicide,murder and nonnegligent manslaughter,murder/nonnegligent manslaughter,"
    "murder & nonnegligent manslaughter,murder/manslaughter,manslaughter,negligent manslaughter,"
    "manslaughter by negligence,rape,forcible rape,rape (legacy definition),rape (revised definition),"
    "sexual assault,sex offenses,sex offences,forcible sex offenses,sex offenses - forcible,non-forcible sex offenses,"
    "sex offenses - non-forcible,fondling,incest,statutory rape,sodomy,sexual battery,robbery,armed robbery,"
    "strong-arm robbery,aggravated assault,agg assault,agg. assault,simple assault,assault,battery,"
    "assault and battery,assault & battery,domestic violence,domestic assault,intimidation,burglary,"
    "breaking and entering,breaking & entering,residential burglary,commercial burglary,burglary - residential,"
    "burglary - commercial,burglary dwelling,burglary other,larceny,larceny-theft,larceny/theft,larceny theft,"
    "theft,petty theft,grand theft,grand larceny,petit larceny,petty larceny,shoplifting,pocket-picking,"
    "pickpocketing,purse-snatching,theft from building,theft from motor vehicle,theft from vehicle,theft from auto,"
    "larceny from auto,auto burglary,vehicle burglary,theft of motor vehicle parts,motor vehicle theft,"
    "motor vehicle theft (mvt),vehicle theft,auto theft,car theft,grand theft auto,stolen vehicle,bicycle theft,"
    "bike theft,theft from the person,arson,vandalism,criminal mischief,criminal damage,criminal damage and arson,"
    "criminal damage & arson,destruction of property,destruction/damage/vandalism of property,damage to property,"
    "property damage,graffiti,fraud,forgery,counterfeiting,forgery and counterfeiting,forgery/counterfeiting,"
    "embezzlement,identity theft,credit card fraud,wire fraud,bribery,extortion,blackmail,kidnapping,"
    "kidnapping/abduction,abduction,human trafficking,stolen property,receiving stolen property,"
    "stolen property offenses,possession of stolen property,drug abuse violations,drug law violations,drug violations,"
    "drug offenses,drug offences,drug offense,drugs,drug/narcotic violations,drug/narcotic offenses,narcotics,"
    "narcotic drug laws,drug possession,possession of drugs,drug trafficking,drug equipment violations,weapons,"
    "weapons violations,weapon law violations,weapons law violations,weapons offenses,weapon offenses,"
    "weapons offences,possession of weapons,weapons possession,carrying concealed weapon,"
    "liquor law violations,liquor law,liquor violations,drunkenness,"
    "public intoxication,drunk and disorderly,dui,dwi,driving under the influence,driving while intoxicated,"
    "disorderly conduct,public order,public order offences,harassment,stalking,trespassing,trespass,"
    "criminal trespass,prostitution,prostitution and commercialized vice,gambling,curfew and loitering,"
    "curfew and loitering law violations,curfew,loitering,runaway,runaways,vagrancy,hate crime,hate crimes,"
    "dating violence,anti-social behaviour,antisocial behaviour,anti social behaviour,anti-social behavior,"
    "violence and sexual offences,violent crime,violent crimes,property crime,property crimes,violence with injury,"
    "violence without injury,other crime,other crimes,other theft,vehicle crime,sexual offences,animal cruelty,"
    "child abuse,offenses against family and children,offenses against the family and children,"
    "all other offenses,all other offenses (except traffic),other assaults,suspicion,cybercrime,cyber crime,"
    "homicide - murder,robbery - armed,obstructing justice,resisting arrest,violation of protective order"
)
# Assault, Battery, Theft, Drugs, Weapons, Gambling, Curfew, Runaway, Suspicion and Intimidation are also batteries,
# words and parts of other names: they count only in a field named Crime or Offense.
CRIME_TYPES_SPECIFIC = CRIME_TYPES - _words(
    "assault,battery,theft,drugs,narcotics,weapons,gambling,curfew,runaway,runaways,suspicion,intimidation,fondling,"
    "trespass,graffiti,fraud,harassment,extortion,blackmail,abduction,vagrancy,loitering,incest,sodomy,public order"
)
_CRIME_SPLIT = re.compile(r"\s+[-–:]\s+|\s*/\s*(?=[A-Z])")


def _crime_keys(value):
    v = _clean(value)
    return [fold(v)] + [fold(p) for p in _CRIME_SPLIT.split(v)[:1] if p.strip()]


def validate_crime_type(value):
    """A type of crime or offence: Murder, Rape, Robbery, Aggravated Assault, Burglary, Larceny-Theft, Motor
    Vehicle Theft, Arson, Simple Assault, Vandalism, DUI, Anti-social behaviour, Burglary - Residential (not
    Slashing, Holding, Felony or 2)."""
    return any(k in CRIME_TYPES for k in _crime_keys(value))


def validate_crime_type_value(value):
    """A type of crime that is no other word: Burglary, Robbery, Larceny-Theft, Aggravated Assault, Motor Vehicle
    Theft, Arson, Vandalism, Criminal Mischief, Shoplifting (not Assault, Battery, Theft, Drugs or Fraud alone)."""
    return any(k in CRIME_TYPES_SPECIFIC for k in _crime_keys(value))


# ------------------------------------------------------------------ crops
CROPS = _words(
    "wheat,winter wheat,spring wheat,durum,durum wheat,all wheat,other spring wheat,hard red winter wheat,hrw wheat,"
    "soft red winter wheat,srw wheat,hard red spring wheat,white wheat,soft white wheat,corn,maize,grain corn,"
    "corn for grain,corn grain,field corn,sweet corn,corn silage,silage corn,maize (corn),"
    "soybeans,soybean,soya,soya beans,soyabeans,soy,soybeans for beans,barley,malting barley,feed barley,"
    "spring barley,winter barley,oats,oat,rye,triticale,sorghum,grain sorghum,sorghum for grain,milo,millet,"
    "proso millet,pearl millet,rice,paddy,paddy rice,rough rice,long grain rice,medium grain rice,buckwheat,quinoa,"
    "canola,rapeseed,oilseed rape,winter rape,spring rape,rape seed,sunflower,sunflowers,sunflower seed,"
    "oil sunflower,flax,flaxseed,linseed,safflower,peanuts,peanut,groundnuts,groundnut,groundnut (in shell),"
    "cotton,upland cotton,pima cotton,cottonseed,seed cotton,sugar beets,sugarbeets,sugar beet,sugarbeet,sugarcane,"
    "sugar cane,sugarcane for sugar,tobacco,potatoes,potato,irish potatoes,sweet potatoes,sweet potato,cassava,"
    "yams,taro,dry beans,dry edible beans,beans,peas,dry peas,field peas,lentils,chickpeas,chick peas,"
    "alfalfa,lucerne,alfalfa hay,hay,other hay,hay & haylage,haylage,clover,silage,pasture,hops,tea,coffee,cocoa,"
    "cacao,cocoa beans,oil palm,palm oil,oil palm fruit,rubber,natural rubber,jute,sisal,hemp,"
    "mustard,mustard seed,sesame,sesame seed,castor beans,castor bean,mung beans,pigeon peas,cowpeas,fava beans,"
    "faba beans,broad beans,lupins,vetch,canary seed,camelina,oilseeds,pulses,cereals"
)
# Corn, Rice, Cotton, Hay, Tobacco, Potatoes, Beans, Peas, Rye, Tea, Coffee, Cocoa, Rubber, Flax, Hemp, Mustard
# and Soy are also a university, fabrics, foods and materials: they count only in a field named Crop.
CROPS_SPECIFIC = CROPS - _words(
    "corn,rice,cotton,hay,tobacco,potatoes,potato,beans,peas,rye,tea,coffee,cocoa,cacao,rubber,natural rubber,flax,"
    "hemp,mustard,soy,soya,silage,pasture,clover,oil palm,palm oil,jute,sisal,sesame,yams,taro,hops,oat,peanut,"
    "peanuts,sweet potato,sweet potatoes,cereals,pulses,oilseeds,lupins,vetch,durum,milo,sunflower,sunflowers,"
    "paddy,quinoa,lentils,chickpeas"
)


def validate_crop(value):
    """A crop: Corn, Wheat, Winter Wheat, Soybeans, Barley, Oats, Rice, Sorghum, Cotton, Canola, Sugar Beets,
    Potatoes, Alfalfa, Hay, Maize, Cassava (not Gold, Crude Oil, Cattle or Apples)."""
    return fold(_clean(value)) in CROPS


def validate_crop_value(value):
    """A crop that is no food, fabric or other word: Wheat, Winter Wheat, Soybeans, Barley, Oats, Sorghum, Canola,
    Sugar Beets, Alfalfa, Maize, Cassava (not Corn, Rice, Cotton, Hay or Potatoes alone)."""
    return fold(_clean(value)) in CROPS_SPECIFIC
