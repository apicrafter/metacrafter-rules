"""Country names in Spanish: the names of the Common Locale Data Repository (Alemania, Estados Unidos, Países
Bajos, Corea del Sur) with the other spellings and short forms that Spanish and Latin American tables use
(Méjico, Irak, Qatar, EE.UU., Holanda, Inglaterra, Rep. Dominicana). Survey answers and registers write them in
upper case or without accents (PERU, Haiti). Found in the Chilean files of metacrafter-testdata (the country of
birth of the respondents of the NEMS-P-Ch pilot survey and the countries of the universities of a survey on
research data management, datos.uchile.cl)."""
import unicodedata

ES_COUNTRY_NAMES = (
    "Afganistán", "Albania", "Alemania", "Andorra", "Angola", "Anguila", "Antigua y Barbuda", "Arabia Saudita",
    "Arabia Saudí", "Argelia", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaiyán", "Bahamas",
    "Bangladés", "Bangladesh", "Barbados", "Baréin", "Bahréin", "Bélgica", "Belice", "Benín", "Bermudas",
    "Bielorrusia", "Birmania", "Bolivia", "Bosnia y Herzegovina", "Bosnia-Herzegovina", "Botsuana", "Botswana",
    "Brasil", "Brunéi", "Bulgaria", "Burkina Faso", "Burundi", "Bután", "Cabo Verde", "Camboya", "Camerún",
    "Canadá", "Catar", "Qatar", "Chad", "Chequia", "República Checa", "Chile", "China", "Chipre",
    "Ciudad del Vaticano", "Vaticano", "Santa Sede", "Colombia", "Comoras", "Congo", "República del Congo",
    "República Democrática del Congo", "Corea", "Corea del Norte", "Corea del Sur", "República de Corea",
    "Costa de Marfil", "Costa Rica", "Croacia", "Cuba", "Curazao", "Dinamarca", "Dominica", "Ecuador", "Egipto",
    "El Salvador", "Emiratos Árabes Unidos", "Emiratos Árabes", "Eritrea", "Escocia", "Eslovaquia", "Eslovenia",
    "España", "Estados Unidos", "Estados Unidos de América", "Estados Unidos de Norteamérica", "EE.UU.", "EEUU",
    "EE. UU.", "Estonia", "Esuatini", "Suazilandia", "Etiopía", "Filipinas", "Finlandia", "Fiyi", "Francia",
    "Gabón", "Gales", "Gambia", "Georgia", "Ghana", "Gibraltar", "Granada", "Grecia", "Groenlandia", "Guadalupe",
    "Guam", "Guatemala", "Guayana Francesa", "Guinea", "Guinea Ecuatorial", "Guinea-Bisáu", "Guinea Bissau",
    "Guyana", "Haití", "Holanda", "Honduras", "Hong Kong", "Hungría", "India", "Indonesia", "Inglaterra", "Irak",
    "Iraq", "Irán", "Irlanda", "Irlanda del Norte", "Islandia", "Islas Caimán", "Islas Cook", "Islas Feroe",
    "Islas Malvinas", "Islas Marshall", "Islas Salomón", "Islas Vírgenes Británicas",
    "Islas Vírgenes de los Estados Unidos", "Israel", "Italia", "Jamaica", "Japón", "Jordania", "Kazajistán",
    "Kazajstán", "Kenia", "Kirguistán", "Kiribati", "Kosovo", "Kuwait", "Laos", "Lesoto", "Letonia", "Líbano",
    "Liberia", "Libia", "Liechtenstein", "Lituania", "Luxemburgo", "Macao", "Macedonia", "Macedonia del Norte",
    "Madagascar", "Malasia", "Malaui", "Malawi", "Maldivas", "Malí", "Malta", "Marruecos", "Martinica", "Mauricio",
    "Mauritania", "México", "Méjico", "Micronesia", "Moldavia", "Mónaco", "Mongolia", "Montenegro", "Mozambique",
    "Myanmar", "Namibia", "Nauru", "Nepal", "Nicaragua", "Níger", "Nigeria", "Noruega", "Nueva Caledonia",
    "Nueva Zelanda", "Nueva Zelandia", "Omán", "Países Bajos", "Pakistán", "Palaos", "Palestina", "Panamá",
    "Papúa Nueva Guinea", "Paraguay", "Perú", "Polinesia Francesa", "Polonia", "Portugal", "Puerto Rico",
    "Reino Unido", "Gran Bretaña", "República Centroafricana", "República Dominicana", "Rep. Dominicana",
    "Ruanda", "Rumania", "Rumanía", "Rusia", "Federación de Rusia", "Federación Rusa", "Sahara Occidental",
    "Samoa", "San Cristóbal y Nieves", "San Marino", "San Vicente y las Granadinas", "Santa Lucía",
    "Santo Tomé y Príncipe", "Senegal", "Serbia", "Seychelles", "Sierra Leona", "Singapur", "Siria", "Somalia",
    "Sri Lanka", "Sudáfrica", "Sudán", "Sudán del Sur", "Suecia", "Suiza", "Surinam", "Tailandia", "Taiwán",
    "Tanzania", "Tayikistán", "Timor Oriental", "Togo", "Tonga", "Trinidad y Tobago", "Trinidad y Tabago",
    "Túnez", "Turkmenistán", "Turquía", "Tuvalu", "Ucrania", "Uganda", "Uruguay", "Uzbekistán", "Vanuatu",
    "Venezuela", "Vietnam", "Viet Nam", "Yemen", "Yibuti", "Yugoslavia", "Zambia", "Zimbabue", "Zimbabwe",
    "Unión Soviética", "Checoslovaquia",
)
# Names that English writes in the same way: a column of these alone does not show Spanish.
_ALSO_ENGLISH = frozenset((
    "albania", "andorra", "angola", "argentina", "armenia", "aruba", "australia", "austria", "bahamas",
    "bangladesh", "barbados", "bolivia", "botswana", "bulgaria", "burkina faso", "burundi", "chad", "chile",
    "china", "colombia", "congo", "costa rica", "cuba", "dominica", "ecuador", "el salvador", "eritrea", "estonia",
    "gambia", "georgia", "ghana", "gibraltar", "guam", "guatemala", "guinea", "guyana", "honduras", "hong kong",
    "india", "indonesia", "iraq", "israel", "jamaica", "kiribati", "kosovo", "kuwait", "laos", "liberia",
    "liechtenstein", "madagascar", "malawi", "malta", "mauritania", "micronesia", "mongolia", "montenegro",
    "mozambique", "myanmar", "namibia", "nauru", "nepal", "nicaragua", "nigeria", "paraguay", "portugal",
    "puerto rico", "qatar", "samoa", "san marino", "senegal", "serbia", "seychelles", "somalia", "sri lanka",
    "tanzania", "togo", "tonga", "tuvalu", "uganda", "uruguay", "vanuatu", "venezuela", "vietnam", "viet nam",
    "yemen", "yugoslavia", "zambia", "zimbabwe",
))


def _fold(value):
    text = unicodedata.normalize("NFKD", " ".join(str(value).strip().lower().split()))
    return "".join(c for c in text if not unicodedata.combining(c))


_NAMES = frozenset(_fold(name) for name in ES_COUNTRY_NAMES)


def validate_es_country_name(value):
    """A country name in Spanish: Alemania, Estados Unidos, Perú, BRASIL, Haiti, EE.UU. (not Germany,
    United States, CL or a number). Names that are the same in English (Argentina, Chile) pass too."""
    text = _fold(value)
    return bool(text) and len(text) <= 60 and text in _NAMES


def validate_es_only_country_name(value):
    """A country name that is Spanish and not also English: Alemania, Perú, Brasil, España (not
    Argentina or Chile, which both languages write alike)."""
    text = _fold(value)
    return text in _NAMES and text not in _ALSO_ENGLISH
