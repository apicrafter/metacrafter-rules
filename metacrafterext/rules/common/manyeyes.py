"""Validators of the types found in the tables of the Many Eyes archive (IBM Many Eyes, 2007 to 2012: 203 534
tables uploaded by its users, 114 585 distinct headers): sports, player positions, medals, video game
platforms, zodiac signs, parts of the day, vehicle makes and models, Bible references, letter grades, course
codes, film genres, stock tickers, film ratings, post IDs and call signs.

Each function takes one value and returns True when it has the form of the type. Words are compared folded:
lower case, without accents, spaces and punctuation (Fútbol, FUTBOL and fut-bol are futbol).
"""
import re
import unicodedata

from metacrafterext.rules.common.b13 import number, text


def fold(value):
    """Lower case without accents, spaces and punctuation; letters of any script stay (Овен is овен)."""
    decomposed = unicodedata.normalize("NFKD", text(value).lower().replace("ß", "ss"))
    plain = "".join(c for c in decomposed if not unicodedata.combining(c))
    return re.sub(r"[\W_]+", "", plain)


def _words(*groups):
    return {fold(word) for group in groups for word in group.split(",")}


_SPLIT = re.compile(r"\s*(?:[/,;&+]|\s(?:and|und|y|e|et|or|o|ou)\s)\s*", re.I)
_LEADING_RANK = re.compile(r"^\s*\d+\s*[º°.)-]?\s+")


def _parts(value):
    """The parts of a combined value: Base- und Softball, 3B,OF, F/G, WII, Nintendo DS."""
    return [p for p in _SPLIT.split(text(value)) if p.strip()]


def _in_list(value, words, combined=True):
    key = fold(value)
    if not key:
        return False
    if key in words:
        return True
    if combined:
        # Base- und Softball: the first word shares its end with the next one.
        parts = [p for p in _parts(value) if not p.rstrip().endswith(("-", "‐"))]
        return len(_parts(value)) > 1 and bool(parts) and all(fold(p) in words for p in parts)
    return False


# ------------------------------------------------------------------ sports
SPORTS = _words(
    # English
    "football,soccer,american football,association football,basketball,baseball,softball,tennis,table tennis,"
    "ping pong,badminton,squash,golf,hockey,ice hockey,field hockey,volleyball,beach volleyball,swimming,"
    "diving,water polo,synchronized swimming,artistic swimming,athletics,track and field,track,cross country,"
    "marathon,running,boxing,wrestling,judo,karate,taekwondo,fencing,archery,shooting,cycling,road cycling,"
    "mountain biking,bmx,rowing,canoeing,kayaking,canoe kayak,sailing,surfing,skiing,alpine skiing,"
    "cross-country skiing,ski jumping,snowboarding,skating,figure skating,speed skating,gymnastics,"
    "artistic gymnastics,rhythmic gymnastics,trampoline,handball,rugby,rugby union,rugby league,rugby sevens,"
    "cricket,lacrosse,equestrian,equestrianism,horse riding,horse racing,triathlon,modern pentathlon,"
    "weightlifting,powerlifting,bowling,climbing,sport climbing,skateboarding,motorsport,auto racing,"
    "motor racing,formula one,nascar,curling,bobsleigh,bobsled,luge,skeleton,biathlon,nordic combined,polo,"
    "netball,darts,snooker,billiards,pool,chess,esports,softball,frisbee,ultimate,dodgeball,kickboxing,"
    "mixed martial arts,mma,martial arts,aerobics,fitness,yoga,pilates,hiking,orienteering,fishing,hunting,"
    "dance,dancing,cheerleading,paralympics,wheelchair basketball",
    # Spanish
    "futbol,futbol americano,futbol sala,baloncesto,basquetbol,basquet,beisbol,softbol,tenis,tenis de mesa,"
    "voleibol,voley,natacion,clavados,saltos,waterpolo,atletismo,ciclismo,boxeo,lucha,esgrima,tiro con arco,"
    "tiro,remo,vela,gimnasia,balonmano,hockey sobre hielo,hockey sobre cesped,halterofilia,levantamiento de pesas,"
    "esqui,patinaje,piraguismo,hipica,equitacion,ajedrez,padel,triatlon,deportes acuaticos,montanismo,"
    "pesca,danza",
    # Portuguese
    "futebol,futebol americano,futsal,basquete,basquetebol,voleibol,volei,volei de praia,natacao,saltos ornamentais,"
    "polo aquatico,atletismo,ciclismo,boxe,luta,esgrima,tiro com arco,remo,vela,ginastica,handebol,andebol,"
    "tenis de mesa,xadrez,surfe,hipismo,canoagem,levantamento de peso,triatlo,patinacao,esqui",
    # Italian
    "calcio,calcio a 5,pallacanestro,pallavolo,beach volley,nuoto,tuffi,pallanuoto,atletica,atletica leggera,"
    "ciclismo,pugilato,lotta,scherma,tiro con l'arco,canottaggio,vela,ginnastica,pallamano,tennistavolo,sci,"
    "pattinaggio,equitazione,scacchi,sollevamento pesi,canoa",
    # German
    "fussball,american football,basketball,handball,tennis,tischtennis,schwimmen,wasserspringen,wasserball,"
    "leichtathletik,radsport,radfahren,boxen,ringen,fechten,bogenschiessen,schiessen,rudern,segeln,turnen,"
    "eishockey,feldhockey,volleyball,beachvolleyball,skisport,ski alpin,skilanglauf,skispringen,eiskunstlauf,"
    "eisschnelllauf,reiten,reitsport,pferdesport,schach,gewichtheben,kanu,kanusport,bobsport,rodeln,"
    "schlittensport,kampfsport,tanzen,tanzsport,klettern,bob- und schlittensport",
    # French
    "athletisme,natation,plongeon,cyclisme,boxe,lutte,escrime,tir a l'arc,aviron,voile,gymnastique,"
    "equitation,echecs,patinage,tennis de table,halterophilie,ski alpin,ski de fond,canoe-kayak,judo",
)


def validate_sport(value):
    """A sport: Basketball, Archery, Pallavolo, Fútbol, Leichtathletik, Base- und Softball (not 10, ESPN)."""
    return _in_list(value, SPORTS)


# ------------------------------------------------------------------ positions in team sports
POSITIONS = _words(
    # American and Canadian football
    "qb,rb,hb,fb,wr,te,ol,ot,og,t,g,c,dl,de,dt,nt,lb,ilb,olb,mlb,cb,db,s,fs,ss,k,p,ls,kr,pr,"
    "quarterback,running back,halfback,fullback,wide receiver,receiver,tight end,offensive line,offensive lineman,"
    "offensive tackle,offensive guard,tackle,guard,center,centre,defensive line,defensive lineman,defensive end,"
    "defensive tackle,nose tackle,linebacker,inside linebacker,outside linebacker,middle linebacker,cornerback,"
    "defensive back,safety,free safety,strong safety,kicker,punter,long snapper,kick returner,punt returner",
    # baseball and softball
    "1b,2b,3b,lf,cf,rf,of,if,dh,sp,rp,rhp,lhp,cl,ut,inf,pitcher,catcher,first base,first baseman,second base,"
    "second baseman,third base,third baseman,shortstop,left field,left fielder,center field,center fielder,"
    "centre field,right field,right fielder,outfield,outfielder,infield,infielder,designated hitter,"
    "starting pitcher,relief pitcher,closer,utility",
    # basketball
    "pg,sg,sf,pf,f,gf,fc,point guard,shooting guard,small forward,power forward,forward,swingman",
    # association football
    "gk,gkp,df,def,mf,mid,fw,fwd,st,cf,lwb,rwb,cdm,cm,cam,lm,rm,lw,rw,goalkeeper,keeper,goalie,defender,"
    "centre back,center back,centre-back,full back,left back,right back,wing back,sweeper,midfielder,"
    "defensive midfielder,central midfielder,attacking midfielder,winger,striker,attacker,"
    "portero,arquero,guardameta,defensa,defensor,defensa central,lateral,lateral derecho,lateral izquierdo,"
    "centrocampista,mediocampista,medio,volante,mediapunta,delantero,extremo,"
    "goleiro,goleira,zagueiro,lateral direito,lateral esquerdo,meia,meio-campo,meio campista,atacante,ponta,"
    "centroavante,torwart,torhuter,abwehr,verteidiger,innenverteidiger,mittelfeld,mittelfeldspieler,sturm,"
    "sturmer,angriff,portiere,difensore,terzino,centrocampista,ala,attaccante,gardien,gardien de but,defenseur,"
    "milieu,milieu de terrain,attaquant,ailier",
    # rugby
    "prop,props,loosehead prop,tighthead prop,hooker,hookers,lock,locks,second row,locks/second row,flanker,"
    "flankers,blindside flanker,openside flanker,number 8,number eight,no 8,no. 8,back row,scrum half,scrum-half,"
    "fly half,fly-half,inside centre,outside centre,centres,wing,wings,full-back",
    # ice hockey
    "d,left wing,right wing,defenseman,defenceman,defence,defense,goaltender,goalie",
)
_POSITION_NUMBER = re.compile(r"^\d{1,2}\s*[-.)]?\s+")


def validate_sports_position(value):
    """A position in a team sport: QB, WR, SS, 1B, RHP, PG, Goalkeeper, Zagueiro, Flanker, 3B,OF, G-F,
    1 point guard (not Library Director, Youth Services, 8)."""
    raw = text(value)
    if not raw or raw.isdigit():
        return False
    raw = _POSITION_NUMBER.sub("", raw)
    if _in_list(raw, POSITIONS):
        return True
    parts = [p for p in re.split(r"\s*[-/,]\s*", raw) if p]
    return len(parts) > 1 and all(fold(p) in POSITIONS for p in parts)


# ------------------------------------------------------------------ medals
MEDALS = _words(
    "gold,silver,bronze,gold medal,silver medal,bronze medal,oro,plata,bronce,medalla de oro,medalla de plata,"
    "medalla de bronce,ouro,prata,medalha de ouro,medalha de prata,medalha de bronze,argento,medaglia d'oro,"
    "medaglia d'argento,medaglia di bronzo,bronzo,or,argent,medaille d'or,medaille d'argent,medaille de bronze,"
    "silber,goldmedaille,silbermedaille,bronzemedaille,золото,серебро,бронза"
)


def validate_medal(value):
    """A medal: Gold, Silver, Bronze, Oro, Plata, Prata, Médaille d'or (not 28, Platinum)."""
    return _in_list(value, MEDALS, combined=False)


# ------------------------------------------------------------------ video game platforms
PLATFORMS = _words(
    "playstation,playstation 1,playstation 2,playstation 3,playstation 4,playstation 5,play station,ps,ps1,ps2,"
    "ps3,ps4,ps5,psx,psone,psp,ps vita,psvita,vita,playstation portable,playstation vita,xbox,xbox 360,x360,"
    "xb360,xbox one,xone,xb1,xbox series x,xbox series s,xbox series x/s,xb,wii,wii u,wiiu,switch,"
    "nintendo switch,nintendo ds,nintendo dsi,nds,ds,dsi,3ds,nintendo 3ds,gamecube,nintendo gamecube,gc,ngc,"
    "n64,nintendo 64,nes,snes,super nintendo,super nes,famicom,super famicom,nintendo,game boy,gameboy,gb,gbc,"
    "game boy color,gameboy color,game boy advance,gameboy advance,gba,game gear,master system,sega master system,"
    "mega drive,sega mega drive,genesis,sega genesis,saturn,sega saturn,dreamcast,sega dreamcast,dc,atari,"
    "atari 2600,2600,atari 7800,jaguar,lynx,neo geo,neogeo,turbografx-16,3do,n-gage,pc,pc games,computer,"
    "windows,mac,macintosh,linux,ios,android,iphone,ipad,mobile,arcade,steam,wiiware,xbla,xbox live arcade,"
    "360,psn,playstation network,virtual console,ouya,stadia,pc cd-rom,dos,ms-dos,commodore 64,c64,amiga,"
    "zx spectrum,msx,game boy/game boy color,playstation ii,playstation iii"
)
_ROMAN = {"ii": "2", "iii": "3", "iv": "4"}


def _platform(part):
    key = fold(part)
    for roman, digit in _ROMAN.items():
        if key.endswith(roman) and key[: -len(roman)] in ("playstation", "ps"):
            key = key[: -len(roman)] + digit
    return key in PLATFORMS


def validate_video_game_platform(value):
    """A video game platform: PlayStation 3, Xbox 360, Wii, Nintendo DS, PS2, GBA, PC, Play Station 2,
    WII, Nintendo DS (not Facebook, DTT, Linux IA32)."""
    raw = text(value)
    if not raw:
        return False
    if _platform(raw):
        return True
    parts = _parts(raw)
    if len(parts) < 2:
        return False
    # Playstation II, III e PSP: a numeral alone continues the PlayStation before it.
    previous = ""
    for part in parts:
        if _platform(part):
            previous = fold(part)
            continue
        numeral = fold(part) in _ROMAN or fold(part) in ("2", "3", "4")
        if not (numeral and previous.startswith(("playstation", "ps"))):
            return False
    return True


# ------------------------------------------------------------------ zodiac signs
ZODIAC = _words(
    "aries,taurus,gemini,cancer,leo,virgo,libra,scorpio,scorpius,sagittarius,sagitarius,capricorn,capricornus,"
    "aquarius,pisces,"
    "tauro,geminis,escorpio,escorpion,sagitario,capricornio,acuario,piscis,"
    "touro,gemeos,cancer,leao,escorpiao,capricornio,aquario,peixes,"
    "widder,stier,zwillinge,krebs,lowe,jungfrau,waage,skorpion,schutze,steinbock,wassermann,fische,"
    "belier,taureau,gemeaux,lion,vierge,balance,scorpion,sagittaire,capricorne,verseau,poissons,"
    "ariete,toro,gemelli,cancro,leone,vergine,bilancia,scorpione,sagittario,capricorno,acquario,pesci,"
    "овен,телец,близнецы,рак,лев,дева,весы,скорпион,стрелец,козерог,водолей,рыбы"
)


def validate_zodiac_sign(value):
    """A sign of the zodiac: Aries, Leo, Capricorn, sagitarius, Escorpio, Steinbock, Овен (not 100 %, AOT)."""
    return _in_list(value, ZODIAC, combined=False)


# ------------------------------------------------------------------ parts of the day
DAYPARTS = _words(
    "morning,early morning,late morning,mid morning,mid-morning,forenoon,noon,midday,lunchtime,afternoon,"
    "early afternoon,late afternoon,evening,early evening,late evening,night,late night,overnight,midnight,"
    "dawn,dusk,daytime,nighttime,night time,day,"
    "manana,media manana,mediodia,tarde,noche,madrugada,medianoche,"
    "manha,meio-dia,meio dia,noite,"
    "morgen,morgens,vormittag,mittag,nachmittag,abend,abends,nacht,nachts,"
    "matin,matinee,midi,apres-midi,soir,soiree,nuit,"
    "mattina,mattino,pomeriggio,sera,notte"
)
_PARENTHESES = re.compile(r"\s*[(\[].*?[)\]]\s*")


def validate_part_of_day(value):
    """A part of the day: Morning, Afternoon, Evening (6pm-9pm), Late night, Noche, Manhã (not 14:30, 3)."""
    return _in_list(_PARENTHESES.sub(" ", text(value)), DAYPARTS)


# ------------------------------------------------------------------ vehicle makes and models
MAKES = _words(
    "abarth,acura,agrale,alfa romeo,alpine,amc,american motors,aston martin,audi,austin,bentley,bmw,bugatti,"
    "buick,byd,cadillac,chery,chevrolet,chevy,chrysler,citroen,cupra,dacia,daewoo,daf,daihatsu,datsun,desoto,"
    "dodge,ds,eagle,ferrari,fiat,fisker,ford,freightliner,gaz,geely,genesis,geo,gm,gmc,great wall,gurgel,haval,"
    "holden,honda,hudson,hummer,hyundai,infiniti,international,international harvester,isuzu,iveco,jaguar,jeep,"
    "kenworth,kia,koenigsegg,lada,lamborghini,lancia,land rover,landrover,lexus,lincoln,lotus,lucid,mack,"
    "mahindra,man,maruti,maruti suzuki,maserati,maybach,mazda,mclaren,mercedes,mercedes-benz,mercedes benz,"
    "mercury,mg,mini,mitsubishi,moskvich,nash,nissan,oldsmobile,opel,packard,pagani,perodua,peterbilt,peugeot,"
    "plymouth,polestar,pontiac,porsche,proton,ram,renault,rivian,rolls-royce,rolls royce,rover,saab,saturn,"
    "scania,scion,seat,simca,skoda,smart,ssangyong,studebaker,subaru,suzuki,talbot,tata,tatra,tesla,toyota,"
    "trabant,triumph,troller,uaz,vauxhall,vaz,volkswagen,vw,volvo,wartburg,willys,yugo,zastava,zaz,"
    "harley-davidson,harley davidson,yamaha,kawasaki,ducati,ktm,aprilia,vespa,piaggio,royal enfield,"
    "moto guzzi,mv agusta,indian,victory,polaris,can-am,bajaj,hero,tvs"
)
_MAKER_SUFFIX = re.compile(
    r"\s*,?\s+(?:motors?|motor (?:company|co\.?|corporation|corp\.?)|automobiles?|automotive|cars|ag|gmbh|"
    r"s\.?p\.?a\.?|s\.?a\.?|inc\.?|corp\.?|co\.?|ltd\.?|llc|group|usa|of america|north america|america)$",
    re.I,
)


def validate_vehicle_make(value):
    """A make of motor vehicles: Toyota, chevrolet, VW, Mercedes-Benz, Land Rover, 1º FIAT, Ford Motor Company
    (not Caterpillar Inc., Acer America, SAGEM, 3)."""
    raw = _LEADING_RANK.sub("", text(value))
    while True:
        if fold(raw) in MAKES:
            return True
        shorter = _MAKER_SUFFIX.sub("", raw)
        if shorter == raw or not shorter:
            return False
        raw = shorter


_MODEL = re.compile(r"(?=.*[^\W\d_])[\w .,'&+/()-]{1,60}")


def validate_vehicle_model(value):
    """A vehicle model under a field that names vehicles: Corolla, Ford Focus, S10, Audi A6 3.0 Avant Quattro
    (not 3, 27.5, not a sentence)."""
    raw = text(value)
    return bool(_MODEL.fullmatch(raw)) and len(raw.split()) <= 8


def validate_vehicle_model_with_make(value):
    """A vehicle model written after its make, for a field named only model: Ford Focus, chevrolet chevelle
    malibu, Acura MDX, BMW 325xi Sport (not Corolla alone, not iPhone 4, not Thickness (mm))."""
    raw = text(value)
    if not validate_vehicle_model(raw):
        return False
    words = raw.split()
    for size in (3, 2, 1):
        if len(words) > size and fold(" ".join(words[:size])) in MAKES:
            return True
    return False


# ------------------------------------------------------------------ Bible references
_BOOKS = (
    r"Genesis|Gen|Gn|Ge|Exodus|Exod|Exo|Ex|Leviticus|Lev|Lv|Le|Numbers|Num|Nm|Nu|Nb|Deuteronomy|Deut|Dt|De|"
    r"Joshua|Josh|Jos|Jsh|Judges|Judg|Jdgs|Jdg|Jg|Ruth|Rth|Ru|Samuel|Sam|Sa|Sm|Kings|Kgs|Ki|Chronicles|Chron|Chr|Ch|"
    r"Ezra|Ezr|Nehemiah|Neh|Ne|Esther|Esth|Est|Es|Job|Jb|Psalms|Psalm|Pss|Psa|Psm|Ps|Proverbs|Prov|Prv|Pro|Pr|"
    r"Ecclesiastes|Eccles|Eccl|Ecc|Ec|Qoh|Song of Solomon|Song of Songs|Song|SoS|Canticles|Isaiah|Isa|Is|"
    r"Jeremiah|Jer|Je|Jr|Lamentations|Lam|La|Ezekiel|Ezek|Eze|Ezk|Daniel|Dan|Dn|Da|Hosea|Hos|Ho|Joel|Jl|Amos|Am|"
    r"Obadiah|Obad|Ob|Jonah|Jon|Jnh|Micah|Mic|Mc|Nahum|Nah|Na|Habakkuk|Hab|Hb|Zephaniah|Zeph|Zep|Zp|Haggai|Hag|Hg|"
    r"Zechariah|Zech|Zec|Zc|Malachi|Mal|Ml|Matthew|Matt|Mat|Mt|Mark|Mrk|Mk|Mr|Luke|Luk|Lk|John|Joh|Jhn|Jn|Acts|Act|Ac|"
    r"Romans|Rom|Rm|Ro|Corinthians|Cor|Co|Galatians|Gal|Ga|Ephesians|Ephes|Eph|Philippians|Phil|Php|Pp|"
    r"Colossians|Col|Thessalonians|Thess|Thes|Th|Timothy|Tim|Ti|Titus|Tit|Philemon|Philem|Phlm|Phm|Hebrews|Heb|"
    r"James|Jas|Jm|Peter|Pet|Pe|Pt|Jude|Jud|Jd|Revelations?|Rev|Re"
)
_BIBLE = re.compile(
    r"(?:(?:[1-3]|I{1,3}|First|Second|Third)[ _]?)?(?:" + _BOOKS + r")\.?[ _]?"
    r"\d{1,3}(?:[:.]\d{1,3}(?:[a-c])?(?:\s?[-–]\s?\d{1,3}(?:[:.]\d{1,3})?)?)?",
    re.I,
)


def validate_bible_reference(value):
    """A Bible reference with a chapter and a verse: John 3:16, Genesis 1:1, 1 Samuel 15:2-3, Mt_28.19,
    2_Co_13.14, Ps 23:1 (not John 3, Mark 12, 3:16, AC2:0)."""
    raw = text(value)
    if not _BIBLE.fullmatch(raw) or not re.search(r"\d[:.]\d", raw):
        return False
    # Chapters and verses count from 1: AC2:0 and AC3:0 are lipids, not Acts.
    return all(int(n) > 0 for n in re.findall(r"\d+", re.sub(r"^\s*[1-3][ _]?", "", raw)))


# ------------------------------------------------------------------ grades and courses
_LETTER_GRADE = re.compile(r"[A-D][+-]?|[EF]")
_COURSE = re.compile(r"[A-Z]{2,5}[ -]?\d{3,4}[A-Z]?")


def validate_letter_grade(value):
    """A letter grade: A, A-, B+, C, F, b+ (not 85, A++, G, Pass)."""
    raw = text(value).replace("−", "-")
    return bool(_LETTER_GRADE.fullmatch(raw.upper() if len(raw) <= 2 else raw))


def validate_course_code(value):
    """A course code: CSI 101, MUS 100, SI 505, ACTG3000, TP-100 (not A101, FY2003, APR 2008, Engineering)."""
    raw = text(value)
    if not _COURSE.fullmatch(raw):
        return False
    letters = re.match(r"[A-Z]+", raw).group()
    return letters not in {"FY", "CY", "AY", "SY", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP",
                           "SEPT", "OCT", "NOV", "DEC", "Q", "YEAR", "AD", "BC", "CE", "BCE"}


# ------------------------------------------------------------------ genres
_GENDER = _words("male,female,m,f,h,man,woman,men,women,homme,femme,hommes,femmes,masculin,feminin,masculino,"
                 "femenino,feminino,mixte,other,autre,unknown,inconnu,boy,girl,garcon,fille")
# In French, genre is also the kind of a thing: the genre of a Belgian school is Ordinaire or Spécialisé.
_KINDS = _words("ordinaire,specialise,special,fondamental,primaire,maternelle,secondaire,superieur,general,"
                "technique,professionnel,artistique,public,prive,libre,officiel,subventionne")
_NAMED = re.compile(r"(?=.*[^\W\d_])[\w .,'&+/()!-]{2,60}")


def validate_genre(value):
    """A genre: Drama, R&B/Soul, Hip-Hop, Science fiction, Rap (not 3, not Homme or Femme, not Ordinaire or
    Spécialisé)."""
    raw = text(value)
    return bool(_NAMED.fullmatch(raw)) and fold(raw) not in _GENDER and fold(raw) not in _KINDS


# ------------------------------------------------------------------ stock tickers, ratings, posts, call signs
# Letters with a class or market suffix (BRK.B, VOD.L, RDS.A), or four characters and the class number of B3
# (BBAS3, ALLL11); not a bond code with digits inside (LB436A, th_bond_symbol).
_TICKER = re.compile(r"\$?(?:[A-Z]{1,5}(?:[.-][A-Z0-9]{1,3})?|[A-Z][A-Z0-9]{3}(?:[1-9]|1[01]))")
_MPA = {"G", "PG", "PG-13", "PG13", "R", "NC-17", "NC17", "X"}
_POST_ID = re.compile(r"[1-9]\d{1,18}")
_CALL_SIGN = re.compile(r"[A-Z0-9]{3,7}(?:-(?:AM|FM|TV|LP|DT|CD|CA|LD|HD\d?))?")


def validate_tickersymbol(value):
    """A stock ticker: AAPL, SPY, BRK.B, BBAS3, VOD.L (not Apple Inc., 12.5, aapl, LB436A)."""
    raw = text(value)
    return bool(_TICKER.fullmatch(raw)) and any(c.isalpha() for c in raw)


def validate_us_mpa_rating(value):
    """An MPA film rating: G, PG, PG-13, R, NC-17, Rated R (not 8.1, TV-MA, NR)."""
    raw = re.sub(r"^rated\s+", "", text(value), flags=re.I).upper().replace(" ", "")
    return raw in _MPA


def validate_x_post_id(value):
    """An X (Twitter) post ID: 440322224407314432, 20 (not 1.30481E+12, abc)."""
    return bool(_POST_ID.fullmatch(number(value)))


def validate_call_sign(value):
    """A radio call sign: KDKA, WNYC-FM, KABC-TV, 9A1AA (not Radio 1, 101.5)."""
    raw = text(value)
    return bool(_CALL_SIGN.fullmatch(raw)) and any(c.isalpha() for c in raw)


# ------------------------------------------------------------------ hashtags and coordinates in degrees
_HASHTAG = re.compile(r"#?(?=\w*[^\W\d_])\w{1,139}")
_HEX_COLOUR = re.compile(r"#(?:[0-9A-Fa-f]{3}|[0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})")
_DEG = (r"\d{1,3}(?:[.,]\d+)?\s?(?:°\s?(?:\d{1,2}(?:[.,]\d+)?\s?['′’]\s?(?:\d{1,2}(?:[.,]\d+)?\s?(?:[″\"”]|'')\s?)?)?)?")
_DMS_PAIR = re.compile(
    _DEG.replace(r"\d{1,3}", r"\d{1,2}", 1) + r"[NS]\s?[,;/]?\s?" + _DEG + r"[EW](?:\s?[-+]?\d+(?:[.,]\d+)?\s?m)?",
    re.I,
)


def validate_hashtag(value):
    """A hashtag, with or without its #: #wikileaks, #COVID19, cablegate (not #, 2011, #0047B2, a sentence)."""
    raw = text(value)
    return bool(_HASHTAG.fullmatch(raw)) and not _HEX_COLOUR.fullmatch(raw)


def validate_iso6709_dms(value):
    """A point in degrees, minutes and seconds with the hemispheres: 50°40′46.461″N 95°48′26.533″W,
    48°51′N 2°21′E, 43.42°S, 172.14°E, 40.8N 72.3E (not 10° 28' N alone, not -14.24,-51.41)."""
    return bool(_DMS_PAIR.fullmatch(text(value)))
