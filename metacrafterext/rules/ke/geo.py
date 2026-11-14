"""Kenyan geography: the 47 counties and the sub-counties (openAFRICA snapshot of metacrafter-testdata)."""
import re
import unicodedata


def _norm(value):
    text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", text)


#: The counties in the order of their codes (001 Mombasa to 047 Nairobi City).
KE_COUNTIES = (
    "Mombasa", "Kwale", "Kilifi", "Tana River", "Lamu", "Taita Taveta", "Garissa", "Wajir", "Mandera",
    "Marsabit", "Isiolo", "Meru", "Tharaka Nithi", "Embu", "Kitui", "Machakos", "Makueni", "Nyandarua",
    "Nyeri", "Kirinyaga", "Murang'a", "Kiambu", "Turkana", "West Pokot", "Samburu", "Trans Nzoia",
    "Uasin Gishu", "Elgeyo Marakwet", "Nandi", "Baringo", "Laikipia", "Nakuru", "Narok", "Kajiado",
    "Kericho", "Bomet", "Kakamega", "Vihiga", "Bungoma", "Busia", "Siaya", "Kisumu", "Homa Bay", "Migori",
    "Kisii", "Nyamira", "Nairobi",
)
_COUNTY_NAMES = frozenset(_norm(n) for n in KE_COUNTIES) | frozenset(
    _norm(n) for n in ("Nairobi City", "Tharaka", "Keiyo Marakwet", "Taita", "Muranga"))
_COUNTY_WORDS = re.compile(r"(?i)\s+(?:city\s+)?county(?:\s+government)?$|^county\s+(?:government\s+)?of\s+|\s+city$")


def validate_ke_county(value):
    """A Kenyan county: Mombasa, Taita/Taveta, Tharaka-Nithi, Murang'a, Muranga, Nairobi City,
    Kilifi County; not a former province (Rift Valley, Coast), Kenya, Rural or a number."""
    text = _COUNTY_WORDS.sub("", str(value).strip())
    return _norm(text) in _COUNTY_NAMES


#: Sub-county names of the Kenya Subcounties list of Code for Africa (openAFRICA) and of the
#: Kenya Master Health Facility List (most are constituencies).
_KE_SUBCOUNTY_NAMES = """
Aberdare Forest|Aberdare National Park|Ainabkoi|Ainamoi|Aldai|Alego Usonga|Athi
River|Awendo|Balambala|Banisa|Banissa|Baringo Central|Baringo North|Belgut|Bobasi|Bomachoge Borabu|Bomachoge
Chache|Bomet Central|Bomet East|Bonchari|Bondo|Borabu|Bumula|Buna|Bungoma Central|Bungoma East|Bungoma
North|Bungoma South|Bungoma West|Bunyala|Bura|Bureti|Busia|Butere|Butula|Buuri|Buuri East|Buuri
West.|Changamwe|Chepalungu|Cheptais|Cherangany|Chesumei|Chonyi|Chuka|Dadaab|Dagoretti|Dagoretti
North|Dagoretti South|East Pokot|Eldas|Embakasi|Embakasi Central|Embakasi East|Embakasi North|Embakasi
South|Embakasi West|Embu East|Embu North|Embu
West|Emgwen|Emuhaya|Endebess|Etago|Fafi|Galole|Ganze|Garbatulla.|Garissa|Garsen|Gatanga|Gatundu North|Gatundu
South|Gem|Gilgil|Githunguri|Gucha|Gucha South|Habaswein.|Hamisi|Homa Bay|Homa Bay
Town|Hulugho|Igambang'ombe|Igambangombe|Igembe Central|Igembe North|Igembe South|Ijara|Ikolomani|Ikutha|Imenti
Central|Imenti North|Imenti North.|Imenti South|Imenti South.|Isinya|Isiolo|Jomvu|Juja|Kabete|Kabondo
Kasipul|Kabuchai|Kahuro|Kajiado Central|Kajiado East|Kajiado North|Kajiado West|Kakamega Central|Kakamega
East|Kakamega Forest|Kakamega North|Kakamega
South|Kalama|Kaloleni|Kamukunji|Kandara|Kanduyi|Kangema|Kangundo|Kapseret|Karachuonyo|Kasarani|Kathiani|Kathonzweni|Katulani|Kauma|Keiyo
North|Keiyo South|Kenyenya|Kericho East|Kesses|Khwisero|Kiambaa|Kiambu|Kiambu
Town|Kibish|Kibra|Kibwezi|Kibwezi East|Kibwezi West|Kieni East|Kieni West|Kigumo|Kiharu|Kikuyu|Kilifi
North|Kilifi South|Kilome|Kilungu|Kimilili|Kimilili
Bungoma|Kiminini|Kinango|Kinangop|Kipipiri|Kipkelion|Kipkelion East|Kipkelion West|Kipkomo|Kirinyaga
Central|Kirinyaga East|Kirinyaga North/Mwea West|Kirinyaga South|Kirinyaga West|Kisasi|Kisauni|Kisii
Central|Kisii South|Kisumu Central|Kisumu East|Kisumu West|Kitui Central|Kitui Rural|Kitui South|Kitui
West|Kitutu Central|Kitutu Chache North|Kitutu Chache South|Koibatek|Konoin|Kuresoi North|Kuresoi South|Kuria
East|Kuria West|Kutulo|Kwanza|Kyuso|Lafey|Lagdera|Laikipia Central|Laikipia East|Laikipia North|Laikipia
West|Laisamis|Lamu East|Lamu
West|Lang'ata|Langata|Lari|Likoni|Likuyani|Limuru|Loima|Loitokitok|Loiyangalani|Londiani|Lower
Yatta|Luanda|Lugari|Lunga
Lunga|Lungalunga|Lurambi|Maara|Machakos|Magarini|Makadara|Makindu|Makueni|Malava|Malindi|Mandera
Central|Mandera East|Mandera North|Mandera South|Mandera West|Mandera West.|Manga|Manyatta|Marakwet
East|Marakwet West|Marani|Marigat|Marsabit Central.|Marsabit North.|Marsabit South.|Masaba North|Masaba
South|Mashuuru|Masinga|Matayos|Matete|Mathare|Mathioya|Mathira East|Mathira
West|Matinyani|Matuga|Matungu|Matungulu|Mau Forest|Mbeere North|Mbeere South|Mbita|Mbooni|Mbooni East|Mbooni
West|Merti|Meru Central|Meru National Park.|Meru
South|Migwani|Mirangine|Mogotio|Moiben|Molo|Mosop|Moyale|Msambweni|Mt Elgon|Mt Elgon Forest|Mt Kenya
Forest|Muhoroni|Mukaa|Mukurwe ini|Mukurweini|Mumias East|Mumias West|Mumoni|Murang'a East|Murang'a
South|Muthambi|Mutitu|Mutitu North|Mutomo|Mvita|Mwala|Mwatate|Mwea East|Mwea West|Mwimbi|Mwingi Central|Mwingi
East|Mwingi North|Mwingi West|Naivasha|Nakuru East|Nakuru North|Nakuru West|Nambale|Nandi Central|Nandi
East|Nandi Hills|Nandi North|Nandi South|Narok East|Narok North|Narok South|Narok
West|Navakholo|Ndhiwa|Njiru|Njoro|North Horr|Nyahururu|Nyakach|Nyali|Nyamache|Nyamira|Nyamira North|Nyamira
South|Nyandarua Central|Nyandarua North|Nyandarua South|Nyandarua West|Nyando|Nyaribari Chache|Nyatike|Nyeri
Central|Nyeri South|Nzambani|Nzaui|Oljoroorok|Olkalou|Pokot Central|Pokot North|Pokot South|Rabai|Rachuonyo
East|Rachuonyo North|Rachuonyo
South|Rangwe|Rarieda|Rongai|Rongo|Roysambu|Ruaraka|Ruiru|Runyenjes|Sabatia|Saboti|Saku|Samburu Central|Samburu
East|Samburu Kwale|Samburu North|Sameta|Samia|Seme|Shinyalu|Siaya|Sigowet/Soin|Sirisia|Soin
Sigowet|Sololo|Sotik|South Mugirango|Soy|Starehe|Suba North|Suba South|Subukia|Suna East|Suna West|Taita|Tana
Delta|Tana North|Tana River|Tarbaj|Taveta|Teso North|Teso South|Tetu|Thagicu|Tharaka North|Tharaka South|Thika
East|Thika Town|Thika West|Tiaty East|Tigania Central|Tigania East|Tigania East.|Tigania
West|Tinderet|Tongaren|Trans Mara East|Trans Mara West|Trans Nzoia East|Trans Nzoia West|Transmara
East|Transmara West|Tseikuru|Turbo|Turkana Central|Turkana East|Turkana North|Turkana South|Turkana
West|Ugenya|Ugunja|Uriri|Vihiga|Voi|Wajir East|Wajir East.|Wajir North|Wajir South|Wajir West|Webuye
East|Webuye West|West Pokot|Westlands|Wundanyi|Yatta|muranga south"""
KE_SUBCOUNTIES = frozenset(_norm(n) for n in " ".join(_KE_SUBCOUNTY_NAMES.split("\n")).split("|") if n.strip())
_SUBCOUNTY_WORDS = re.compile(r"(?i)\s+sub[ -]?county$")


def validate_ke_subcounty(value):
    """A Kenyan sub-county: Changamwe, Kisauni, Lungalunga, Embakasi East, Kirinyaga North/Mwea West,
    Mvita Sub County; not a Ugandan sub county (Abarilela) or a number."""
    key = _norm(_SUBCOUNTY_WORDS.sub("", str(value).strip()))
    return bool(key) and not key.isdigit() and key in KE_SUBCOUNTIES
