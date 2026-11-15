"""Country names in Portuguese: the names of the Common Locale Data Repository in Brazilian and European
Portuguese (Alemanha, Estados Unidos, Países Baixos, Arménia and Armênia) and the names Brazilian registers
still use (Holanda, Inglaterra, Coréia do Sul, Iugoslávia). BNDES and CAPES files write them in upper case
without accents (REPUBLICA DOMINICANA, ESTADOS UNIDOS)."""
import unicodedata

PT_COUNTRY_NAMES = (
    'Afeganistão', 'Alanda', 'Albânia', 'Alemanha', 'Alemanha Ocidental', 'Andorra', 'Angola', 'Anguila',
    'Antilhas Holandesas', 'Antártida', 'Antígua e Barbuda', 'Argentina', 'Argélia', 'Arménia', 'Armênia', 'Aruba',
    'Arábia Saudita', 'Austrália', 'Azerbaijão', 'Baamas', 'Bahamas', 'Bangladeche', 'Bangladesh', 'Barbados',
    'Barein', 'Barém', 'Belize', 'Benim', 'Benin', 'Bermudas', 'Bielorrússia', 'Birmânia', 'Bolívia', 'Botsuana',
    'Brasil', 'Brunei', 'Bulgária', 'Burquina Faso', 'Burundi', 'Butão', 'Bélgica', 'Bósnia',
    'Bósnia e Herzegovina', 'Cabo Verde', 'Camarões', 'Camboja', 'Canadá', 'Catar', 'Cazaquistão', 'Chade',
    'Chile', 'China', 'Chipre', 'Chéquia', 'Cidade do Vaticano', 'Colômbia', 'Comores', 'Congo - Kinshasa',
    'Congo-Brazzaville', 'Congo-Kinshasa', 'Coreia', 'Coreia do Norte', 'Coreia do Sul', 'Coreia, República da',
    'Coréia do Norte', 'Coréia do Sul', 'Costa do Marfim', 'Costa Rica', 'Croácia', 'Cuba', 'Curaçao', 'Curaçau',
    'Côte d’Ivoire (Costa do Marfim)', 'Dinamarca', 'Djibuti', 'Dominica', 'Domínica', 'Egito', 'El Salvador',
    'Emirados Árabes', 'Emirados Árabes Unidos', 'Equador', 'Eritreia', 'Escócia', 'Eslováquia', 'Eslovénia',
    'Eslovênia', 'Espanha', 'Essuatíni', 'Estados Unidos', 'Estados Unidos da América', 'Estónia', 'Estônia',
    'Etiópia', 'EUA', 'Federação Russa', 'Fiji', 'Filipinas', 'Finlândia', 'França', 'Gabão', 'Gana', 'Geórgia',
    'Gibraltar', 'Granada', 'Groenlândia', 'Gronelândia', 'Grã-Bretanha', 'Grécia', 'Guadalupe', 'Guam', 'Guame',
    'Guatemala', 'Guernesey', 'Guernsey', 'Guiana', 'Guiana Francesa', 'Guiné', 'Guiné Bissau', 'Guiné Equatorial',
    'Guiné-Bissau', 'Gâmbia', 'Haiti', 'Holanda', 'Honduras', 'Hong Kong', 'Hong Kong, RAE da China', 'Hungria',
    'Ilha Bouvet', 'Ilha Christmas', 'Ilha de Man', 'Ilha do Natal', 'Ilha Norfolk', 'Ilhas Aland', 'Ilhas Caimão',
    'Ilhas Cayman', 'Ilhas Cocos (Keeling)', 'Ilhas Cook', 'Ilhas dos Cocos (Keeling)', 'Ilhas Falkland',
    'Ilhas Faroé', 'Ilhas Geórgia do Sul e Sandwich do Sul', 'Ilhas Heard e McDonald', 'Ilhas Malvinas',
    'Ilhas Marianas do Norte', 'Ilhas Marshall', 'Ilhas Menores Afastadas dos EUA',
    'Ilhas Menores Distantes dos EUA', 'Ilhas Pitcairn', 'Ilhas Salomão', 'Ilhas Turcas e Caicos',
    'Ilhas Virgens Americanas', 'Ilhas Virgens Britânicas', 'Ilhas Virgens dos EUA', 'Indonésia', 'Inglaterra',
    'Iraque', 'Irlanda', 'Irlanda do Norte', 'Irã', 'Irão', 'Islândia', 'Israel', 'Itália', 'Iugoslávia', 'Iémen',
    'Iêmen', 'Jamaica', 'Japão', 'Jersey', 'Jibuti', 'Jordânia', 'Kosovo', 'Koweit', 'Kuwait', 'Laos', 'Lesoto',
    'Letónia', 'Letônia', 'Libéria', 'Liechtenstein', 'Listenstaine', 'Lituânia', 'Luxemburgo', 'Líbano', 'Líbia',
    'Macau', 'Macau, RAE da China', 'Macedónia', 'Macedónia do Norte', 'Macedônia', 'Macedônia do Norte',
    'Madagascar', 'Madagáscar', 'Maiote', 'Malaui', 'Maldivas', 'Mali', 'Malta', 'Malásia', 'Maláui', 'Marrocos',
    'Martinica', 'Mauritânia', 'Maurícia', 'Maurício', 'Mayotte', 'Mianmar (Birmânia)', 'Micronésia', 'Moldávia',
    'Mongólia', 'Monserrate', 'Montenegro', 'Montserrat', 'Moçambique', 'México', 'Mónaco', 'Mônaco', 'Namíbia',
    'Nauru', 'Nepal', 'Nicarágua', 'Nigéria', 'Niue', 'Niuê', 'Noruega', 'Nova Caledónia', 'Nova Caledônia',
    'Nova Zelândia', 'Níger', 'Omã', 'Palau', 'Palestina', 'Panamá', 'Papua-Nova Guiné', 'Paquistão', 'Paraguai',
    'País de Gales', 'Países Baixos', 'Países Baixos Caribenhos', 'Peru', 'Polinésia Francesa', 'Polónia',
    'Polônia', 'Porto Rico', 'Portugal', 'Quirguistão', 'Quiribati', 'Quiribáti', 'Quénia', 'Quênia',
    'Reino Unido', 'República Centro-Africana', 'República Democrática do Congo', 'República do Congo',
    'República Dominicana', 'República Popular da China', 'República Tcheca', 'Reunião', 'Roménia', 'Romênia',
    'Ruanda', 'Rússia', 'Saara Ocidental', 'Salvador', 'Samoa', 'Samoa Americana', 'San Marino', 'Santa Helena',
    'Santa Lúcia', 'Sara Ocidental', 'Seicheles', 'Senegal', 'Serra Leoa', 'Singapura', 'Sint Maarten', 'Somália',
    'Sri Lanca', 'Sri Lanka', 'Suazilândia', 'Sudão', 'Sudão do Sul', 'Suriname', 'Suécia', 'Suíça',
    'Svalbard e Jan Mayen', 'São Bartolomeu', 'São Cristóvão e Neves', 'São Cristóvão e Névis', 'São Marinho',
    'São Martinho', 'São Martinho (Saint-Martin)', 'São Martinho (Sint Maarten)', 'São Pedro e Miquelão',
    'São Tomé e Príncipe', 'São Vicente e Granadinas', 'Sérvia', 'Síria', 'Tadjiquistão', 'Tailândia', 'Taiwan',
    'Tajiquistão', 'Tanzânia', 'Tcheca', 'Tchecoslováquia', 'Tchéquia', 'Território Britânico do Oceano Índico',
    'Territórios Austrais Franceses', 'Territórios Franceses do Sul', 'Territórios palestinianos',
    'Territórios palestinos', 'Timor Leste', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Toquelau',
    'Trindade e Tobago', 'Trinidad e Tobago', 'Tunísia', 'Turcomenistão', 'Turquemenistão', 'Turquia', 'Tuvalu',
    'Ucrânia', 'Uganda', 'União Soviética', 'Uruguai', 'Usbequistão', 'Uzbequistão', 'Vanuatu', 'Vaticano',
    'Venezuela', 'Vietname', 'Vietnã', 'Wallis e Futuna', 'Zimbabué', 'Zimbábue', 'Zâmbia', 'África do Sul',
    'Áustria', 'Índia',
)


def _ascii(value):
    return unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()


_EXACT = {" ".join(n.lower().split()) for n in PT_COUNTRY_NAMES}
_FOLDED = {_ascii(n) for n in _EXACT}


def validate_pt_country_name(value):
    """A country name in Portuguese, with its accents in any case (Alemanha, ESTADOS UNIDOS, França, Japão),
    or in upper case without accents (FRANCA, REPUBLICA DOMINICANA). Spanish spellings with accents that
    Portuguese lacks fail (Perú, Japón)."""
    text = " ".join(str(value).split())
    if not text:
        return False
    if text.lower() in _EXACT:
        return True
    return text.isupper() and _ascii(text) == text and text.lower() in _FOLDED
