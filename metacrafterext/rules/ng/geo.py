"""Nigerian geography: states, local government areas (LGAs), and the LGA and ward codes of the
GRID3 / eHealth Africa settlement data (openAFRICA snapshot of metacrafter-testdata)."""
import re
import unicodedata


def _norm(value):
    """ASCII lower case without spaces, hyphens, slashes or other punctuation: Isiala-Ngwa North and
    Isiala Ngwa North are one key."""
    text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", text)


#: The 36 states and the Federal Capital Territory with their ISO 3166-2:NG codes (without NG-),
#: in alphabetical order: the position is the state number of the GRID3 LGA codes (19 Kaduna).
NG_STATES = (
    ("Abia", "AB"), ("Adamawa", "AD"), ("Akwa Ibom", "AK"), ("Anambra", "AN"), ("Bauchi", "BA"),
    ("Bayelsa", "BY"), ("Benue", "BE"), ("Borno", "BO"), ("Cross River", "CR"), ("Delta", "DE"),
    ("Ebonyi", "EB"), ("Edo", "ED"), ("Ekiti", "EK"), ("Enugu", "EN"), ("Federal Capital Territory", "FC"),
    ("Gombe", "GO"), ("Imo", "IM"), ("Jigawa", "JI"), ("Kaduna", "KD"), ("Kano", "KN"), ("Katsina", "KT"),
    ("Kebbi", "KE"), ("Kogi", "KO"), ("Kwara", "KW"), ("Lagos", "LA"), ("Nasarawa", "NA"), ("Niger", "NI"),
    ("Ogun", "OG"), ("Ondo", "ON"), ("Osun", "OS"), ("Oyo", "OY"), ("Plateau", "PL"), ("Rivers", "RI"),
    ("Sokoto", "SO"), ("Taraba", "TA"), ("Yobe", "YO"), ("Zamfara", "ZA"),
)
NG_STATE_CODES = frozenset(code for _, code in NG_STATES)
_STATE_NAMES = frozenset(_norm(name) for name, _ in NG_STATES) | frozenset(
    _norm(n) for n in ("FCT", "Abuja", "FCT Abuja", "Federal Capital Territory (Abuja)", "Nassarawa", "Akwa-Ibom"))
_STATE_SUFFIX = re.compile(r"(?i)\s+state$")


def validate_ng_state(value):
    """A Nigerian state or the FCT: Kaduna, Akwa Ibom, Cross River, Kano State, FCT, Nassarawa (the
    GADM spelling); not Northern Nigeria, a code (KD) or TOTAL."""
    text = _STATE_SUFFIX.sub("", str(value).strip())
    return _norm(text) in _STATE_NAMES


def validate_ng_state_code(value):
    """The ISO 3166-2:NG code of a state without the country: KD, AK, FC (not NG or KDS)."""
    return str(value).strip().upper() in NG_STATE_CODES and len(str(value).strip()) == 2


#: LGA names of the population tables of citypopulation.de (eHealth Africa on openAFRICA, 775 LGAs
#: and FCT area councils), the GADM 2 spellings (truncated at eight letters: Arochukw, AwkaNort) and
#: the Kaduna Electric settlement data.
_NG_LGA_NAMES = """
Aba North|Aba South|Abadam|Abaji|Abak|Abakalik|Abakaliki|Abeokuta North|Abeokuta
South|AbeokutaNorth|Abi|Abo-Mbaise|Aboh-Mba|Abua - Odual|Abua/Odu|Abuja Municipal Area
Council|AbujaMun|Adavi|Ado|Ado Ekiti|Ado-Ekiti|Ado-Odo/Ota|AdoOdo/Ota|Afijio|Afikpo|Afikpo North|Afikpo
South|AfikpoSo|Agaie|Agatu|Agege|Aguata|Agwara|Ahiazu-Mbaise|Ahizu-Mb|Ahoada East|Ahoada
West|Aiyedaade|Aiyedire|Aiyekire
(Gbonyin)|Ajaokuta|Ajeromi-Ifelodun|Ajeromi/Ifelodun|Ajingi|Akamkpa|Akinyele|Akko|Akoko North East|Akoko North
West|Akoko North-East|Akoko South East|Akoko South West|Akoko South-East|Akoko
South-West|Akoko-Ed|Akoko-Edo|AkokoNorthWest|Akpabuyo|Akuku Toru|Akukutor|Akure North|Akure
South|Akwanga|Albasu|Aleiro|Alimosho|Alkaleri|Amuwo Odofin|Amuwo-Odofin|Anambra East|Anambra
West|Anaocha|Andoni|Andoni/O|Aninri|Aniocha North|Aniocha
South|AniochaN|AniochaS|Anka|Ankpa|Apa|Apapa|Ardo-Kola|Arewa|Arewa-Dandi|Argungu|Arochukw|Arochukwu|Asa|Asari-To|Asari-Toru|Askira/U|Askira/Uba|Atakumosa
East|Atakumosa West|Atakunmosa East|Atakunmosa West|Atiba|Atisbo|Augie|Auyo|Awe|Awgu|Awka North|Awka
South|AwkaNort|AwkaSout|Ayamelum|Ayedaade|Ayedire|Babura|Badagary|Badagry|Bade|Bagudo|Bagwai|Bakassi|Bakassi
[→ Cameroon (2008)]|Bakori|Bakura|Balanga|Bali|Bama|Barkin
Ladi|Baruten|Bassa|Batagarawa|Batsari|Bauchi|Baure|Bayo|Bebeji|Bekwara|Bekwarra|Bende|Biase|Bichi|Bida|Billiri|Bindawa|Binji|Biriniwa|Birnin
Gwari|Birnin Kebbi|Birnin Kudu|Birnin
Magaji|Birnin-G|Birnin-Gwari|Birnin-Magaji/Kiyaw|BirninKe|BirninKu|Biu|Bodinga|Bogoro|Boki|Bokkos|Boluwaduro|Bomadi|Bonny|Borgu|Boripe|Borsari|Bosso|Brass|Buji|Bukkuyum|Bungudu|Bunkure|Bunza|Bursari|Buruku|Burutu|Bwari|Calabar|Calabar
Municipal|Calabar South|Chanchaga|Charanchi|Chibok|Chikun|Dala|Damaturu|Damban|Dambatta|Damboa|Dan
Musa|Dandi|Dandume|Dange Shuni|Dange-Shuni|Danja|Danko Wasagu|Danmusa|Darazo|Dass|Daura|Dawakin Kudu|Dawakin
Tofa|DawakinK|DawakinT|Degema|Dekina|Demsa|Dikwa|Disputed
Areas|Doguwa|Doma|Donga|Dukku|Dunukofia|Dutse|Dutsi|Dutsin-M|Dutsin-Ma|Eastern Obolo|Ebonyi|Edati|Ede
North|Ede
South|Edu|Efon|EgbadoNorth|EgbadoSouth|Egbeda|Egbedore|Egor|Ehime-Mb|Ehime-Mbano|Ejigbo|Ekeremor|Eket|Ekiti|Ekiti
East|Ekiti South West|Ekiti
West|EkitiEas|EkitiSouth-West|EkitiWest|Ekwusigo|Eleme|Emuoha|Emure|Emure/Ise/Orun|Enugu East|Enugu
North|Enugu South|EnuguSou|Epe|Esan Central|Esan North East|Esan South East|Esan
West|EsanCent|EsanNort|EsanSout|EsanWest|Ese-Odo|Esit Eket|Essien Udim|Essien-U|Etche|Ethiope East|Ethiope
West|EthiopeE|Eti-Osa|Etim Ekpo|EtimEkpo|Etinan|Etsako Central|Etsako East|Etsako
West|EtsakoEa|EtsakoWe|Etung|Ewekoro|Ezeagu|Ezinihit|Ezinihitte|Ezza North|Ezza
South|Fagge|Fakai|Faskari|Fika|Fufore|Funakaye|Fune|Funtua|Gabasawa|Gada|Gagarawa|Gamawa|Gamjuwa|Ganjuwa|Ganye|Garki|Garko|Garum
Mallam|Gashaka|Gassol|Gaya|Gbako|Gboko|Gboyin|Geidam|Gezawa|Giade|Girei|Girie|Giwa|Gokana|Gombe|Gombi|Goronyo|Gubio|Gudu|Gujba|Gulani|Guma|Gumel|Gummi|Gurara|Guri|Gusau|Guyuk|Guzamala|Gwadabaw|Gwadabawa|Gwagwala|Gwagwalada|Gwale|Gwandu|Gwaram|Gwarzo|Gwer
East|Gwer West|GwerWest|Gwiwa|Gwoza|Hadejia|Hawul|Hong|Ibadan North|Ibadan North East|Ibadan North West|Ibadan
South East|Ibadan South
West|IbadanNorth|IbadanNorth-East|IbadanNorth-West|IbadanSouth-East|IbadanSouth-West|Ibaji|Ibarapa
Central|Ibarapa East|Ibarapa North|Ibeju/Lekki|Ibeno|Ibesikpo Asutan|Ibi|Ibiono Ibom|Idah|Idanre|Ideato
North|Ideato South|IdeatoNo|Idemili North|Idemili South|Ido|Ido-Osi|Ido/Osi|Ifako-Ijaye|Ifako/Ijaye|Ife
Central|Ife East|Ife North|Ife
South|IfeCentral|Ifedayo|Ifedore|Ifelodun|Ifo|Igabi|Igalamela-Odolu|Igbo-Eti|Igbo-Etiti|Igbo-Eze
North|Igbo-Eze South|Igbo-eze North|Igbo-eze South|Igueben|Ihiala|Ihitte/U|Ihitte/Uboma|Ijebu East|Ijebu
North|Ijebu North East|Ijebu North-East|Ijebu Ode|IjebuEast|IjebuNorth|IjebuOde|Ijero|Ijumu|Ika|Ika North
East|Ika South|IkaNorth|IkaSouth|Ikara|Ikeduru|Ikeja|Ikenne|Ikere|Ikole|Ikom|Ikono|Ikorodu|Ikot Abasi|Ikot
Ekpene|Ikot-Aba|Ikot-Ekp|Ikpoba-Okha|Ikwerre|Ikwo|Ikwuano|Ila|Ilaje|IlajeEseodo|Ile-Oluji-Okeigbo|IleOluji/Okeigbo|Ilejemeje|Ilesha
East|Ilesha West|Illela|Ilorin East|Ilorin South|Ilorin West|IlorinWe|Imeko
Afon|Imeko-Afon|Ingawa|Ini|Ipokia|Irele|Irepo|Irepodun|Irepodun/Ifelodun|Irewole|Isa|Ise/Orun|Iseyin|Ishielu|Isi-Uzo|Isiala
Ngwa North|Isiala Ngwa South|Isiala-Mbano|Isiala-Ngwa North|Isiala-Ngwa South|IsialaMb|Isin|Isokan|Isoko
North|Isoko
South|IsokoNor|IsokoSou|Isu|Isuikwua|Isuikwuato|Itas/Gad|Itas/Gadau|Itesiwaju|Itu|Ivo|Iwajowa|Iwo|Izzi|Jaba|Jada|Jahun|Jakusko|Jalingo|Jama'are|Jega|Jema'A|Jema'a|Jere|Jibia|Jos
East|Jos North|Jos South|Kabba/Bu|Kabba/Bunu|Kabo|Kachia|Kaduna North|Kaduna South|Kafin
Hausa|KafinHau|Kafur|Kaga|Kagarko|Kaiama|Kaita|Kajola|Kajuru|Kala/Balge|Kalgo|Kaltungo|Kanam|Kankara|Kanke|Kankia|Kankiya|Kano|Kano
Municipal|Karasuwa|Karaye|Karim-La|Karim-Lamido|Karu|Katagum|Katcha|Katsina|Katsina (Benue)|Katsina
(K)|Katsina-Ala|Kaugama|Kaura|Kaura Namoda|Kaura-Na|Kauru|Kazaure|Keana|Kebbe|Keffi|Khana|Kibiya|Kirfi|Kiri
Kasama|KiriKasa|Kiru|Kiyawa|Kogi|Koko/Bes|Koko/Besse|Kokona|Kolokuma/Opokuma|Konduga|Konshish|Konshisha|Kontagora|Kontogur|Kosofe|Kotonkar|Kuban|Kubau|Kudan|Kuje|Kukawa|Kumbotso|Kunchi|Kura|Kurfi|Kurmi|Kusada|Kwali|Kwami|Kwande|Kware|Kwaya
Kusar|Lafia|Lagelu|Lagos Island|Lagos Mainland|LagosIsland|Lake Chad|Lamurde|Langtang North|Langtang
South|Lapai|Lau|Lavun|Lere|Logo|Lokoja|Machina|Madagali|Madobi|Mafa|Magama|Magumeri|Mai'Adua|Mai'adua|Maidugur|Maiduguri|Maigatari|Maiha|Mainland|Maiyama|Makarfi|Makoda|Makurdi|Malam
Madori|MalamMad|Malumfashi|Mangu|Mani|Maradun|Mariga|Marte|Maru|Mashegu|Mashi|Matazu|Mayo-Bel|Mayo-Belwa|Mbaitoli|Mbo|Michika|Miga|Mikang|Minjibir|Misau|Mkpat
Enin|Moba|Mobbar|Mokwa|Monguno|Mopa-Muro|Moro|Mubi North|Mubi
South|Musawa|Mushin|Muya|Nafada|Nangere|Nasarawa|Nasarawa-Eggon|Nassaraw|Nassarawa Egon|Ndokwa East|Ndokwa
West|Nembe|Ngala|Nganzai|Ngaski|Ngor-Okp|Ngor-Okpala|Nguru|Ningi|Njaba|Njikoka|Nkanu East|Nkanu
West|Nkwerre|Nnewi North|Nnewi South|NnewiNort|NnewiSou|Nsit Atai|Nsit Ibom|Nsit
Ubium|Nsukka|Numan|Nwangele|Obafemi-Owode|Obanliku|Obi|Obi Ngwa|Obio/Akp|Obio/Akpor|Obokun|Oboma Ngwa|Obot
Akara|Obowo|Obubra|Obudu|Odeda|Odigbo|Odo-Otin|Odo0tin|Odogbolu|Odukpani|Offa|Ofu|Ogba - Egbema -
Ndoni|Ogba/Egbe|Ogbadibo|Ogbaru|Ogbia|Ogbomosho North|Ogbomosho South|Ogo
Oluwa|Ogo-Oluw|Ogoja|Ogori/Magongo|Ogu - Bolo|Ogu/Bolo|Ogun Waterside|OgunWaterside|Oguta|Ohafia|Ohafia
Abia|Ohaji/Eg|Ohaji/Egbema|Ohaozara|Ohaukwu|Ohimini|Oji-River|Ojo|Oju|Oke-Ero|Okehi|Okene|Okigwe|Okitipupa|Okobo|Okpe|Okpokwu|Okrika|Ola-Oluwa|Olamabor|Olamaboro|Olorunda|Olorunsogo|Oluyole|Omala|Omumma|Ona-Ara|Ondo
East|Ondo West|Onicha|Onitsha North|Onitsha South|Onna|Opobo - Nkoro|Opobo/Nkoro|Oredo|Oredo
Edo|Orelope|Orhionmw|Orhionmwon|Ori Ire|Ori-Ire|Oriade|Orlu|Orolu|Oron|Orsu|Oru East|Oru West|Oruk
Anam|Oruk-Ana|Orumba North|Orumba South|OrumbaNo|OrumbaSo|Ose|Oshimili North|Oshimili
South|Oshodi-Isolo|Oshodi/Isolo|Osisioma Ngwa|Osogbo|Oturkpo|Ovia North East|Ovia South
West|OviaNort|OviaSouth-West|Owan East|Owan West|OwanWest|Owerri Municipal|Owerri North|Owerri
West|Owo|Oye|Oyi|Oyigbo|Oyo East|Oyo West|Oyun|Paikoro|Pankshin|Patani|Pategi|Port
Harcourt|Port-Harcourt|Potiskum|Qua'an Pan|Qua'anpa|Rabah|Rafi|Rano|Remo North|Remo-North|Rijau|Rimi|Rimin
Gado|RiminGad|Ringim|Riyom|Rogo|Roni|Sabon Birni|Sabon
Gari|Sabon-Ga|Sabon-Gari|Sabuwa|Safana|Sagamu|Sagbama|Sakaba|Saki East|Saki
West|Sandamu|Sanga|Sapele|Sardauna|Shagamu|Shagari|Shanga|Shani|Shanono|Shelleng|Shendam|Shinkafi|Shira|Shiroro|Shomgom|Shomolu|Silame|Soba|Sokoto
North|Sokoto South|Song|Southern Ijaw|Sule
Tankarkar|Sule-Tan|Suleja|Sumaila|Suru|Surulere|Tafa|Tafawa-B|Tafawa-Balewa|Tai|Takai|Takum|Talata
Mafara|Talata-Mafara|Tambawal|Tambuwal|Tangaza|Tangazar|Tarauni|Tarka|Tarmua|Tarmuwa|Taura|Teungo|Tofa|Toro|Toto|Toungo|Tsafe|Tsanyawa|Tudun
Wada|Tundun Wada|Tureta|Udenu|Udi|Udu|Udung Uko|Ughelli North|Ughelli
South|Ugwunagbo|Uhunmwonde|Ukanafun|Ukum|Ukwa East|Ukwa West|Ukwuani|Umu-Nneochi|Umuahia North|Umuahia
South|Ungogo|Unuimo|Uruan|Urue-Offong/Oruko|UrueOffo|Ushongo|Ussa|Uvwie|Uyo|Uzo-Uwani|Vandeiky|Vandeikya|Wamakko|Wamba|Warawa|Warji|Warri
North|Warri South|Warri South West|Warri South-West|Wasagu/Danko|Wase|Wudil|Wukari|Wurno|Wushishi|Yabo|Yagba
East|Yagba West|Yakurr|Yala|Yala Cross|Yamaltu|Yamaltu/Deba|Yankwashi|Yauri|Yenagoa|Yenegoa|Yewa North (Egbado
North)|Yewa South (Egbado South)|Yola North|Yola South|Yorro|Yunusari|Yusufari|Zaki|Zango|Zangon
Kataf|Zangon-Kataf|ZangonKa|Zaria|Zing|Zurmi|Zuru"""
NG_LGAS = frozenset(_norm(n) for n in " ".join(_NG_LGA_NAMES.split("\n")).split("|") if n.strip())
_LGA_SUFFIX = re.compile(r"(?i)\s+(?:l\.?g\.?a\.?|local government(?: area| council)?|area council)$")


def validate_ng_lga(value):
    """A Nigerian local government area: Birnin Gwari, Aba North, Isiala-Ngwa South, Ado-Odo/Ota,
    Ikeja LGA; not a state (Kaduna State), a ward or a code (19001)."""
    text = str(value).strip()
    key = _norm(text)
    if key in NG_LGAS:
        return not key.isdigit()
    key = _norm(_LGA_SUFFIX.sub("", text))
    return bool(key) and not key.isdigit() and key in NG_LGAS


def validate_ng_lga_code(value):
    """A five-digit LGA code of GRID3: the state number (01 Abia to 37 Zamfara) and the LGA number,
    19001 (Birnin Gwari, Kaduna); not 38001, 00001 or 19000."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return len(text) == 5 and text.isdigit() and 1 <= int(text[:2]) <= 37 and int(text[2:]) > 0


_WARD_CODE = re.compile(r"^([A-Z]{2})(\d{2})(\d{2})$")


def validate_ng_ward_code(value):
    """A ward code of the GRID3 / eHealth Africa settlement data: state code, LGA number and ward
    number, KD0101 (not E05000026, a UK ward, or XX0101)."""
    match = _WARD_CODE.match(str(value).strip())
    return bool(match) and match.group(1) in NG_STATE_CODES and match.group(2) != "00" and match.group(3) != "00"
