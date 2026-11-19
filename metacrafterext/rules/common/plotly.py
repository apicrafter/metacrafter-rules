"""Validators of the types found in the tables of the Plotly community feed (the VizNet corpus of Plotly charts,
2015 to 2018: 1 090 629 charts of Plotly users, 1 013 540 distinct tables): NYC 311 complaint types, social
networks, marketing channels of web analytics, GICS sectors, emotions, sentiment labels, energy sources,
weather conditions, planets, cryptocurrency exchanges, log levels, credit ratings, Amazon EC2 instance types,
web browsers and operating systems by value, and colors in the CSS notations of charts.

Plotly names the columns of a chart after its traces (x, y, labels, trace 0, y), so most of these types are
found by their values. Each function takes one value and returns True when it has the form of the type. Words
are compared folded, as in the validators of the Many Eyes archive: lower case, without accents, spaces and
punctuation (Noise - Residential, NOISE - RESIDENTIAL and noise residential are noiseresidential).

The lists leave out the words that are as common in other columns as in the type (General, Electric, Lead of
311; Line and Medium of social networks; Error and Warning of log levels), so that a column needs the words of
the type itself to reach the share of values that labels it.
"""
import re

from metacrafterext.rules.common.b13 import text
from metacrafterext.rules.common.manyeyes import _in_list, _words, fold
from metacrafterext.rules.common.respondents import _BROWSERS, _OPERATING_SYSTEMS, _OS_VERSION, _fold

# ------------------------------------------------------------------ NYC 311 complaint types
NYC_311 = _words(
    "noise - residential,heat/hot water,heating,illegal parking,blocked driveway,street condition,"
    "street light condition,plumbing,water system,unsanitary condition,indoor unsanitary condition,"
    "general construction,general construction/plumbing,noise - street/sidewalk,noise - commercial,paint/plaster,"
    "paint - plaster,paint condition,sanitation condition,dirty conditions,rodent,derelict vehicle,derelict vehicles,"
    "noise - vehicle,noise - park,noise - helicopter,noise - house of worship,noise survey,collection truck noise,"
    "sewer,traffic signal condition,damaged tree,dead tree,dead/dying tree,illegal tree damage,new tree request,"
    "overgrown tree/branches,root/sewer/sidewalk condition,building/use,consumer complaint,"
    "missed collection (all materials),missed collection,door/window,water leak,nonconst,graffiti,taxi complaint,"
    "taxi report,taxi compliment,for hire vehicle complaint,animal abuse,homeless encampment,"
    "homeless person assistance,broken muni meter,broken parking meter,literature request,hpd literature request,"
    "dof literature request,dot literature request,dca literature request,elevator,sidewalk condition,"
    "curb condition,highway condition,bridge condition,air quality,indoor air quality,food establishment,"
    "food poisoning,standing water,flooring/stairs,request large bulky item collection,derelict bicycle,"
    "special enforcement,hazardous materials,street sign - damaged,street sign - missing,street sign - dangling,"
    "maintenance or facility,non-emergency police matter,drug activity,urinating in public,panhandling,"
    "animal in a park,illegal fireworks,bike/roller/skate chronic,disorderly youth,posting advertisement,"
    "outside building,sweeping/missed,sweeping/inadequate,sweeping/missed-inadequate,litter basket / request,"
    "overflowing litter baskets,recycling enforcement,other enforcement,dof property - reduction issue,"
    "dof property - owner issue,dof property - request copy,dof property - payment issue,"
    "dof property - update account,dof parking - payment issue,dof parking - request copy,water conservation,"
    "water quality,drinking water,indoor sewage,emergency response team (ert),vacant lot,"
    "special projects inspection team (spit),benefit card replacement,scrie,star exemption,"
    "dhs advantage - tenant,dhs advantage -landlord/broker,dhs advantage - landlord/broker,"
    "unsanitary animal pvt property,dead animal,unleashed dog,illegal animal kept as pet,boilers,"
    "housing - low income senior,housing options,dca / doh new license application request,"
    "fire safety director - f58,eap inspection - f59,violation of park rules,electronics waste,industrial waste,"
    "school maintenance,asbestos,window guard,cranes and derricks,scaffold safety,best/site safety,"
    "city vehicle placard complaint,fire alarm - new system,open flame permit,adopt-a-basket,"
    "special natural area district (snad),ferry inquiry,ferry complaint,illegal dumping,abandoned vehicle,"
    "mosquitoes,lost property,bus stop shelter placement,public payphone complaint,beach/pool/sauna complaint,"
    "tattooing,day care,mold,poison ivy,electrical,appliance,vending,smoking,drinking,construction,traffic,"
    "noise,snow,safety,general,lead,electric,agency issues,doe complaint or compliment,opinion for the mayor"
)
# Topics that are ordinary words in other columns: they count in a column of complaint types but do not
# make one (a list of utilities or hazards has Electric, Lead, Snow and Safety).
_NYC_311_COMMON = _words(
    "electrical,appliance,vending,smoking,drinking,construction,traffic,noise,snow,safety,general,lead,electric,mold,"
    "elevator,plumbing,heating,graffiti,sewer,boilers,asbestos,tattooing,mosquitoes"
)
NYC_311_SPECIFIC = NYC_311 - _NYC_311_COMMON


def validate_nyc_311_complaint_type(value):
    """A complaint type of NYC 311: Noise - Residential, HEAT/HOT WATER, Blocked Driveway, Street Light Condition,
    Rodent, Missed Collection (All Materials), and in a field named after it also Plumbing or Electric
    (not Pothole on Main St, 311 or Brooklyn)."""
    return _in_list(value, NYC_311, combined=False)


def validate_nyc_311_complaint_type_value(value):
    """A complaint type of NYC 311 that is no ordinary word: Blocked Driveway, Rodent, HEAT/HOT WATER (not
    Electric, Noise or Snow, which count only in a field named after the type)."""
    return _in_list(value, NYC_311_SPECIFIC, combined=False)


# ------------------------------------------------------------------ social networks
SOCIAL_NETWORKS = _words(
    "facebook,twitter,instagram,linkedin,linked-in,pinterest,pintrest,reddit,tumblr,snapchat,google plus,"
    "googleplus,whatsapp,wechat,weibo,sina weibo,vk,vkontakte,odnoklassniki,ok.ru,flickr,vine,periscope,tiktok,"
    "quora,myspace,foursquare,swarm,stumbleupon,digg,delicious,hacker news,livejournal,naver,orkut,hi5,tagged,"
    "yikyak,yik yak,houzz,deviantart,goodreads,meetup,xing,viadeo,qzone,douban,renren,mixi,plurk,mastodon,"
    "kakaotalk,kakao story,viber,youtube,twitch,discord,snapchat stories,facebook messenger,telegram,"
    "pocket,blogger,tumblr blogs,disqus,research gate,researchgate,academia.edu,stack exchange,stack overflow,"
    "slashdot,hatena bookmark,yelp,tripadvisor,nextdoor,bebo,friendster,ello,diaspora,gab,parler,threads,"
    "bluesky,x"
)
# X alone is also a letter, a mark and an axis: it counts in a column of networks but does not make one.
_SOCIAL_COMMON = _words("x,pocket,threads,swarm,telegram,discord,vine,delicious,tagged")


def validate_social_network(value):
    """A social network by name: Facebook, Twitter, Instagram, LinkedIn, Pinterest, Reddit, VKontakte, Weibo,
    StumbleUpon, Google+ (not Email, Google or Web)."""
    # Folding drops the plus: Google+ is compared as Google Plus, not as Google.
    return _in_list(text(value).replace("+", " plus"), SOCIAL_NETWORKS - _SOCIAL_COMMON, combined=False)


# ------------------------------------------------------------------ marketing channels
MARKETING_CHANNELS = _words(
    "direct,direct traffic,organic search,organic_search,seo,paid search,paid_search,ppc,sem,cpc,"
    "branded paid search,non branded paid search,non-branded paid search,generic paid search,shopping search,"
    "social,social media,organic social,paid social,other social,email,e-mail,emailing,newsletter,referral,"
    "referrals,display,display ads,display advertising,programmatic,retargeting,re-targeting,affiliate,"
    "affiliates,other advertising,(other),video,paid video,audio,sms,push,marketing automation,"
    "cross-network,(unassigned),unassigned"
)
_CHANNEL_COMMON = _words("direct,social,email,e-mail,video,audio,sms,push,display,newsletter,unassigned")


def validate_marketing_channel(value):
    """A channel of a web analytics channel grouping: Organic Search, Paid Search, Referral, Affiliates,
    (Other), Other Advertising, and also Direct, Social and Email among them (not Google, Facebook or Phone)."""
    return _in_list(value, MARKETING_CHANNELS, combined=False)


def validate_marketing_channel_value(value):
    """A channel of a web analytics channel grouping that is no ordinary word: Organic Search, Paid Search,
    Referral, (Other), Affiliates, Paid Social (not Direct, Social or Email alone)."""
    return _in_list(value, MARKETING_CHANNELS - _CHANNEL_COMMON, combined=False)


# ------------------------------------------------------------------ GICS sectors
GICS_SECTORS = _words(
    "energy,materials,basic materials,industrials,industrial,consumer discretionary,consumer disc,consumer disc.,"
    "consumer staples,health care,healthcare,financials,financial,financial services,fin. services,"
    "information technology,info. tech,information tech.,technology,it,communication services,"
    "communications services,telecommunication services,telecommunications services,telecommunications,"
    "telecom services,telecom. services,telecom,utilities,real estate,consumer cyclical,consumer cyclicals,"
    "cons. cyclical,consumer defensive,cons. def.,consumer non-cyclical,consumer non-cyclicals,consumer goods,"
    "consumer services"
)
# Sectors that are names of industries in any list: they count beside the GICS names, but a column of
# industries (Technology, Energy, Retail) is industry. Health Care and Healthcare fold to the same word and
# stay.
_GICS_COMMON = _words(
    "energy,materials,industrial,financial,technology,it,telecom,telecommunications,real estate,"
    "utilities,consumer goods,consumer services,financial services"
)


def validate_gics_sector(value):
    """A sector of GICS or of another provider's sector list: Consumer Discretionary, Information Technology,
    Health Care, Financials, Telecommunication Services, Consumer Cyclical (not Banking or Retail)."""
    return _in_list(value, GICS_SECTORS, combined=False)


def validate_gics_sector_value(value):
    """A GICS sector name that is not a common industry word: Consumer Discretionary, Consumer Staples,
    Financials, Industrials, Health Care, Information Technology, Communication Services (not Energy,
    Technology or Real Estate alone)."""
    return _in_list(value, GICS_SECTORS - _GICS_COMMON, combined=False)


# ------------------------------------------------------------------ emotions
EMOTIONS = _words(
    "anger,angry,disgust,disgusted,fear,fearful,afraid,scared,happiness,happy,joy,sadness,sad,surprise,surprised,"
    "suprise,trust,anticipation,neutral,netural,contempt,shame,ashamed,guilt,boredom,bored,enthusiasm,worry,"
    "relief,love,hate,anxiety,anxious,jealousy,loneliness,disappointment,disappointed,contentment,calm,"
    "excitement,frustration,pride,gratitude,amusement,awe,embarrassment,confusion,interest"
)
_EMOTION_COMMON = _words("love,hate,interest,calm,neutral,netural,pride,awe,trust")


def validate_emotion(value):
    """An emotion category: anger, disgust, fear, joy, sadness, surprise, anticipation, Happy, Boredom
    (not positive, negative, tweets or trust alone)."""
    return _in_list(value, EMOTIONS - _EMOTION_COMMON, combined=False)


# ------------------------------------------------------------------ sentiment labels
SENTIMENTS = _words(
    "positive,negative,neutral,very positive,very negative,somewhat positive,somewhat negative,slightly positive,"
    "slightly negative,strongly positive,strongly negative,mixed,pos,neg,neu,positivo,negativo,neutro,positif,"
    "negatif,neutre,positiv,negativ"
)


def validate_sentiment(value):
    """A sentiment label: positive, negative, neutral, very positive, pos, neg, neu, Positivo (not 0.43 or
    joy)."""
    return _in_list(value, SENTIMENTS, combined=False)


# ------------------------------------------------------------------ energy sources
ENERGY_SOURCES = _words(
    "coal,hard coal,lignite,brown coal,imported coal,white coal,natural gas,gas,gas (natural),ng,lng,oil,crude oil,"
    "petroleum,petroleum liquids,petroleum coke,petro,diesel,furnace oil,fuel oil,heavy fuel oil,nuclear,"
    "nuclear power,hydro,hydroelectric,hydroelectricity,hydropower,hydro power,hydro conventional,small hydro,"
    "large hydro,run-of-river,run of river,pumped storage,pumped hydro,hydro pumped storage,"
    "hydro run-of-river and poundage,hydro water reservoir,wind,onshore wind,offshore wind,wind onshore,"
    "wind offshore,solar,solar pv,photovoltaics,photovoltaic,pv,solar thermal,utility solar,distributed pv,"
    "biomass,biogas,gas (biogas),biofuels,biofuels & waste,biofuels and waste,bioenergy,other biomass,other bio,"
    "waste,geothermal,tidal,wave,marine,ccgt,ocgt,combined cycle,open cycle gas turbine,cogeneration,"
    "co-generation,chp,fossil gas,fossil hard coal,fossil brown coal/lignite,fossil oil,fossil coal-derived gas,"
    "fossil oil shale,fossil peat,peat,oil shale,other renewables,other renewable,renewables,"
    "renewable energy sources,other fossil fuel,other gases,thermal,wood,storage,battery storage,imports"
)
_ENERGY_COMMON = _words("gas,oil,wind,solar,waste,wood,wave,marine,storage,thermal,imports,ng,pv,renewables")


def validate_energy_source(value):
    """An energy source of energy or electricity production: Coal, Natural Gas, Nuclear, Hydro, Wind Offshore,
    Solar PV, Biomass, CCGT, Fossil Hard coal (not Residential, Transport or 450 MW)."""
    return _in_list(value, ENERGY_SOURCES - _ENERGY_COMMON)


# ------------------------------------------------------------------ weather conditions
WEATHER = _words(
    "clear,clear sky,sky is clear,clear night,sunny,mostly sunny,partly sunny,sunny day,fair,cloudy,clouds,"
    "partly cloudy,partly cloudy (day),partly cloudy (night),mostly cloudy,overcast,overcast clouds,"
    "partial overcast,few clouds,scattered clouds,broken clouds,thin clouds,rain,rainy,raining,light rain,"
    "moderate rain,heavy rain,torrential rain,rain showers,showers,light rain shower,light rain showers,"
    "patchy rain possible,chance of rain,drizzle,light drizzle,patchy light drizzle,light intensity drizzle,"
    "light intensity drizzle rain,freezing drizzle,freezing rain,sleet,light sleet,rain/sleet,snow,snowy,light snow,"
    "moderate snow,heavy snow,patchy light snow,patchy moderate snow,blowing snow,snow/hail,blizzard,hail,"
    "thunderstorm,thunderstorms,t-storms,thunder,moderate or heavy rain with thunder,rain-thunderstorm,"
    "fog-rain-thunderstorm,fog,foggy,freezing fog,mist,haze,hazy,smoke,dust,sand,fog, smog, smoke,smog,"
    "windy,breezy,blowing sand,squalls,tornado,humid,clear-day,clear-night,partly-cloudy-day,"
    "partly-cloudy-night"
)
_WEATHER_COMMON = _words("clear,fair,sand,dust,smoke,thunder,humid,windy,breezy,clouds,rain,snow,hail,mist")


def validate_weather_condition(value):
    """A weather condition in words: Clear, Partly Cloudy, Overcast, Rain, Light Snow, Thunderstorm, Fog,
    Breezy and Mostly Cloudy, Rain/Sleet (not Dry, Wet or 23 °C)."""
    return _in_list(value, WEATHER)


def validate_weather_condition_value(value):
    """A weather condition that is no ordinary word: Partly Cloudy, Overcast, Light Rain, Thunderstorm, Drizzle,
    Foggy, Sunny (not Clear, Rain or Snow alone)."""
    return _in_list(value, WEATHER - _WEATHER_COMMON)


# ------------------------------------------------------------------ planets
PLANETS = _words("mercury,venus,earth,mars,jupiter,saturn,uranus,neptune,pluto")
_PLANET_NOTE = re.compile(r"\s*\((?:planet|dwarf planet)\)\s*$", re.I)


def validate_planet(value):
    """A planet of the Solar System, with Pluto: Mercury, Earth, Jupiter, Neptune, Mercury (planet) (not Moon,
    Sun or Ceres)."""
    return _in_list(_PLANET_NOTE.sub("", text(value)), PLANETS, combined=False)


# ------------------------------------------------------------------ cryptocurrency exchanges
CRYPTO_EXCHANGES = _words(
    "binance,coinbase,coinbase pro,gdax,kraken,bitfinex,bitstamp,bittrex,poloniex,gemini,bithumb,huobi,huobi pro,"
    "okex,okx,okcoin,hitbtc,kucoin,cryptopia,liqui,bitmex,bitflyer,coincheck,zaif,upbit,korbit,coinone,exmo,"
    "livecoin,yobit,cex.io,quoine,quoinex,liquid,quadrigacx,btc-e,wex,itbit,lakebtc,gatecoin,bitbay,bitso,"
    "mercado bitcoin,btcc,zb.com,bibox,gate.io,coinexchange,tidex,bleutrade,c-cex,novaexchange,coinsquare,"
    "bitmart,bybit,ftx,crypto.com,bitget,mexc,bitpanda,luno,paxful,localbitcoins,bitvavo,coinfloor,therocktrading,"
    "btc markets,independent reserve,bitkub,indodax,wazirx,coindcx,zebpay,bitbns,bitonic,bitpay"
)
_EXCHANGE_COMMON = _words("gemini,liquid,luno")


def validate_crypto_exchange(value):
    """A cryptocurrency exchange by name: Binance, Coinbase, GDAX, Kraken, Bitfinex, Bitstamp, Poloniex, cex.io
    (not Bitcoin, BTC or NASDAQ)."""
    return _in_list(value, CRYPTO_EXCHANGES - _EXCHANGE_COMMON, combined=False)


# ------------------------------------------------------------------ log levels
LOG_LEVELS = _words(
    "trace,debug,info,information,informational,notice,warn,warning,error,err,critical,crit,alert,emerg,emergency,"
    "fatal,severe,fine,finer,finest,config,verbose,panic,off,all"
)
# In capitals the words are levels (INFO, WARN, ERROR); in lower case only those that are no ordinary word
# (trace is also the series of a chart).
_LOG_LOWER = _words("debug,info,warn,fatal,crit,emerg,err,finer,finest,verbose")


def validate_log_level(value):
    """A log level: INFO, WARN, ERROR, DEBUG, FATAL, TRACE, Informational, SEVERE, and in a field named after it
    also error, warning or notice (not High, 3 or Failed)."""
    return _in_list(value, LOG_LEVELS, combined=False)


def validate_log_level_value(value):
    """A log level written as levels are written: INFO, WARN, ERROR, CRITICAL in capitals, or debug, info, warn,
    fatal (not error, warning, critical or trace in lower case, which are ordinary words)."""
    raw = text(value)
    if raw.isupper():
        return _in_list(raw, LOG_LEVELS - _words("off,all"), combined=False)
    return _in_list(raw, _LOG_LOWER, combined=False)


# ------------------------------------------------------------------ credit ratings
_SP_FITCH = r"AAA|AA[+-]?|A[+-]?|BBB[+-]?|BB[+-]?|B[+-]?|CCC[+-]?|CC|C|R?D|SD"
_MOODYS = r"Aaa|Aa[123]|A[123]|Baa[123]|Ba[123]|B[123]|Caa[123]|Ca|C"
_RATING = re.compile(r"^(?:%s|%s)(?:\s?\((?:sf|p|pi|u|e)\)|u|\*[+-]?)?$" % (_SP_FITCH, _MOODYS))
# The doubled letters and the grades of Moody's that are no school grade, cell reference or abbreviation: AA+,
# BBB-, Baa2, Caa1 (not A, B+, C, A1, B2, SD, a standard deviation or South Dakota, or CC, the communauté de
# communes of French EPCI types).
_RATING_DISTINCT = re.compile(r"^(?:AAA|AA[+-]?|BBB[+-]?|BB[+-]?|CCC[+-]?|Aaa|Aa[123]|Baa[123]|Ba[123]|Caa[123]|Ca)"
                              r"(?:\s?\((?:sf|p|pi|u|e)\)|u|\*[+-]?)?$")


def validate_credit_rating(value):
    """A long-term credit rating of S&P, Fitch or Moody's: AAA, AA+, BBB-, B, CCC, D, Aaa, Baa2, A1, AA+u (not
    AAAA, A++ or 4)."""
    return bool(_RATING.match(text(value)))


def validate_credit_rating_value(value):
    """A credit rating that no school grade, cell reference or abbreviation shares: AAA, AA+, BBB-, BB, Baa2,
    Caa1 (not A, B+, C, A1, B2, SD or CC, which count only in a field named after ratings)."""
    return bool(_RATING_DISTINCT.match(text(value)))


# ------------------------------------------------------------------ web browsers and operating systems
# Facebook and Instagram are in-app browsers in the lists of the survey validators, and social networks
# here; BlackBerry and IE are also a phone and a country code.
_BROWSERS_BY_VALUE = frozenset(_BROWSERS - {"facebook", "instagram", "blackberry", "ie", "silk", "edge", "webkit"}) | {
    "chrome mobile ios", "chrome frame", "pale moon", "iceweasel", "phantomjs", "mobile safari ui/wkwebview",
    "opera mobile", "opera tablet", "ie mobile", "iemobile", "yabrowser", "maxthon", "puffin", "sleipnir",
    "rockmelt", "k-meleon", "epiphany", "midori", "lunascape", "coc coc", "qq browser", "sogou explorer",
    "baidu browser", "360 browser", "netfront", "dolfin", "avant",
}
_OS_BY_VALUE = frozenset(_OPERATING_SYSTEMS - {"mac", "blackberry", "unix", "debian", "fedora"}) | {
    "windows 10", "windows 8.1", "windows 8", "windows 7", "windows vista", "windows xp", "windows 2000",
    "windows 98", "windows 95", "windows rt", "windows server", "fire os", "fireos", "webos", "bada",
    "firefox os", "symbian os", "symbianos", "blackberry os", "solaris", "openbsd", "playstation vita",
}


def validate_web_browser_value(value):
    """A web browser by name, for a column whose name says nothing: Chrome, Firefox, Safari, Internet Explorer,
    Opera, Chrome Mobile, Android Browser (not Facebook, IE, Other or Unknown alone)."""
    return _fold(value) in _BROWSERS_BY_VALUE


def validate_operating_system_value(value):
    """An operating system by name, for a column whose name says nothing: Windows, iOS, Android, Linux, macOS,
    OS X 10.10, Windows 7, Chrome OS (not Mac, Unix, Other or Unknown alone)."""
    folded = _fold(value)
    return folded in _OS_BY_VALUE or bool(_OS_VERSION.match(folded))


# ------------------------------------------------------------------ Amazon EC2 instance types
_EC2_TYPE = re.compile(r"^[a-z][a-z0-9-]*\d[a-z0-9-]*\.(?:nano|micro|small|medium|large|\d{0,3}xlarge|metal(?:-\d{1,3}xl)?)$")


def validate_aws_ec2_instance_type(value):
    """An Amazon EC2 instance type: t2.micro, m4.large, c5.2xlarge, c7gn.xlarge, m7i-flex.large, mac1.metal (not
    m4-large, t2 or file.large)."""
    return bool(_EC2_TYPE.match(text(value)))


# ------------------------------------------------------------------ colors in CSS notations
_BYTE = r"\s*(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\s*"
_RGB = re.compile(r"^rgb ?\(%s,%s,%s\)$" % (_BYTE, _BYTE, _BYTE))
_RGBA = re.compile(r"^rgba ?\(%s,%s,%s,\s*(?:0|1|0?\.\d+|1\.0+)\s*\)$" % (_BYTE, _BYTE, _BYTE))
_HUE = r"\s*(?:360(?:\.0+)?|(?:3[0-5]\d|[12]\d\d|[1-9]?\d)(?:\.\d+)?)\s*"
_PERCENT = r"\s*(?:100(?:\.0+)?|[1-9]?\d(?:\.\d+)?)%\s*"
_HSL = re.compile(r"^hsl ?\(%s,%s,%s\)$" % (_HUE, _PERCENT, _PERCENT))
_HEX = re.compile(r"^#(?:[0-9A-Fa-f]{3}){1,2}$")


def validate_rgb_color(value):
    """A color in the CSS rgb() notation: rgb(255, 99, 71), rgb(10,10,10) (not rgb(256,0,0) or 220,220,220)."""
    return bool(_RGB.match(text(value)))


def validate_rgba_color(value):
    """A color in the CSS rgba() notation: rgba(179,226,205,1), rgba(222, 45, 38, 0.8), rgba (255, 0, 0, 1)
    (not rgba(256,0,0,1) or rgba(0,0,0,2))."""
    return bool(_RGBA.match(text(value)))


def validate_hsl_color(value):
    """A color in the CSS hsl() notation, with whole or decimal numbers: hsl(0, 100%, 50%), hsl(0.0,50%,50%),
    hsl(360.0,50%,50%) (not hsl(361,50%,50%) or 0, 100%, 50%)."""
    return bool(_HSL.match(text(value)))


def validate_hex_color(value):
    """A hex color with its hash: #2ca02c, #FFF, #1F5FBF (not 2ca02c, #12345 or #wikileaks)."""
    return bool(_HEX.match(text(value)))
