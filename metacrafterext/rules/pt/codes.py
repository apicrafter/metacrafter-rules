"""Portuguese codes and names found in 2024 snapshots of Portuguese open data portals (Dateno sources
cdi00001307, Observatório do Alto Tâmega e Barroso; cdi00001313, Águeda; cdi00001315, Cascais; cdi00001317,
dados.gov.pt; cdi00001318, Dados na Justiça): DICOFRE codes of districts, municipalities and parishes,
subsection codes of the census (BGRI), municipalities, districts, quarters and postal codes.
"""
import re
import unicodedata

# Districts 01 to 18, Madeira 31 and 32, the Azores 41 to 49.
_DISTRICT = r"(?:0[1-9]|1[0-8]|3[12]|4[1-9])"
_DICOFRE = re.compile(_DISTRICT + r"\d{2}(?:\d{2})?")
_BGRI = re.compile(_DISTRICT + r"\d{9}")
_QUARTER = re.compile(r"[1-4]\.?[ºo°]? ?trimestre(?: (?:de )?\d{4})?", re.I)
_POSTCODE = re.compile(r"[1-9]\d{3}(?:[- ]\d{3})?(?: \S.*)?")

# The municipalities of the list of the Ministry of Justice (dados.justica.gov.pt) and Corvo: 306 names
# of 308 municipalities, as Lagoa and Calheta are each the name of two.
CONCELHOS = (
    "Abrantes", "Aguiar da Beira", "Alandroal", "Albergaria-a-Velha", "Albufeira", "Alcanena", "Alcobaça",
    "Alcochete", "Alcoutim", "Alcácer do Sal", "Alenquer", "Alfândega da Fé", "Alijó", "Aljezur", "Aljustrel",
    "Almada", "Almeida", "Almeirim", "Almodôvar", "Alpiarça", "Alter do Chão", "Alvaiázere", "Alvito",
    "Amadora", "Amarante", "Amares", "Anadia", "Angra do Heroísmo", "Ansião", "Arcos de Valdevez", "Arganil",
    "Armamar", "Arouca", "Arraiolos", "Arronches", "Arruda dos Vinhos", "Aveiro", "Avis", "Azambuja", "Baião",
    "Barcelos", "Barrancos", "Barreiro", "Batalha", "Beja", "Belmonte", "Benavente", "Bombarral", "Borba",
    "Boticas", "Braga", "Bragança", "Cabeceiras de Basto", "Cadaval", "Caldas da Rainha", "Calheta", "Caminha",
    "Campo Maior", "Cantanhede", "Carrazeda de Ansiães", "Carregal do Sal", "Cartaxo", "Cascais",
    "Castanheira de Pêra", "Castelo Branco", "Castelo de Paiva", "Castelo de Vide", "Castro Daire",
    "Castro Marim", "Castro Verde", "Celorico da Beira", "Celorico de Basto", "Chamusca", "Chaves", "Cinfães",
    "Coimbra", "Condeixa-a-Nova", "Constância", "Coruche", "Corvo", "Covilhã", "Crato", "Cuba",
    "Câmara de Lobos", "Elvas", "Entroncamento", "Espinho", "Esposende", "Estarreja", "Estremoz", "Fafe",
    "Faro", "Felgueiras", "Ferreira do Alentejo", "Ferreira do Zêzere", "Figueira da Foz",
    "Figueira de Castelo Rodrigo", "Figueiró dos Vinhos", "Fornos de Algodres", "Freixo de Espada à Cinta",
    "Fronteira", "Funchal", "Fundão", "Gavião", "Golegã", "Gondomar", "Gouveia", "Grândola", "Guarda",
    "Guimarães", "Góis", "Horta", "Idanha-a-Nova", "Lagoa", "Lagos", "Lajes das Flores", "Lajes do Pico",
    "Lamego", "Leiria", "Lisboa", "Loulé", "Loures", "Lourinhã", "Lousada", "Lousã", "Macedo de Cavaleiros",
    "Machico", "Madalena", "Mafra", "Maia", "Mangualde", "Manteigas", "Marco de Canaveses", "Marinha Grande",
    "Marvão", "Matosinhos", "Mação", "Mealhada", "Melgaço", "Mesão Frio", "Mira", "Miranda do Corvo",
    "Miranda do Douro", "Mirandela", "Mogadouro", "Moimenta da Beira", "Moita", "Monchique", "Mondim de Basto",
    "Monforte", "Montalegre", "Montemor-o-Novo", "Montemor-o-Velho", "Montijo", "Monção", "Mora", "Mortágua",
    "Moura", "Mourão", "Murtosa", "Murça", "Mértola", "Mêda", "Nazaré", "Nelas", "Nisa", "Nordeste", "Odemira",
    "Odivelas", "Oeiras", "Oleiros", "Olhão", "Oliveira de Azeméis", "Oliveira de Frades", "Oliveira do Bairro",
    "Oliveira do Hospital", "Ourique", "Ourém", "Ovar", "Palmela", "Pampilhosa da Serra", "Paredes",
    "Paredes de Coura", "Paços de Ferreira", "Pedrógão Grande", "Penacova", "Penafiel", "Penalva do Castelo",
    "Penamacor", "Penedono", "Penela", "Peniche", "Peso da Régua", "Pinhel", "Pombal", "Ponta Delgada",
    "Ponta do Sol", "Ponte da Barca", "Ponte de Lima", "Ponte de Sor", "Portalegre", "Portel", "Portimão",
    "Porto", "Porto Moniz", "Porto Santo", "Porto de Mós", "Povoação", "Proença-a-Nova", "Póvoa de Lanhoso",
    "Póvoa de Varzim", "Redondo", "Reguengos de Monsaraz", "Resende", "Ribeira Brava", "Ribeira Grande",
    "Ribeira de Pena", "Rio Maior", "Sabrosa", "Sabugal", "Salvaterra de Magos", "Santa Comba Dão",
    "Santa Cruz", "Santa Cruz da Graciosa", "Santa Cruz das Flores", "Santa Maria da Feira",
    "Santa Marta de Penaguião", "Santana", "Santarém", "Santiago do Cacém", "Santo Tirso", "Sardoal", "Seia",
    "Seixal", "Sernancelhe", "Serpa", "Sertã", "Sesimbra", "Setúbal", "Sever do Vouga", "Silves", "Sines",
    "Sintra", "Sobral de Monte Agraço", "Soure", "Sousel", "Sátão", "São Brás de Alportel",
    "São João da Madeira", "São João da Pesqueira", "São Pedro do Sul", "São Roque do Pico", "São Vicente",
    "Tabuaço", "Tarouca", "Tavira", "Terras de Bouro", "Tomar", "Tondela", "Torre de Moncorvo", "Torres Novas",
    "Torres Vedras", "Trancoso", "Trofa", "Tábua", "Vagos", "Vale de Cambra", "Valença", "Valongo", "Valpaços",
    "Velas", "Vendas Novas", "Viana do Alentejo", "Viana do Castelo", "Vidigueira", "Vieira do Minho",
    "Vila Flor", "Vila Franca de Xira", "Vila Franca do Campo", "Vila Nova da Barquinha",
    "Vila Nova de Cerveira", "Vila Nova de Famalicão", "Vila Nova de Foz Côa", "Vila Nova de Gaia",
    "Vila Nova de Paiva", "Vila Nova de Poiares", "Vila Pouca de Aguiar", "Vila Real",
    "Vila Real de Santo António", "Vila Velha de Ródão", "Vila Verde", "Vila Viçosa",
    "Vila da Praia da Vitória", "Vila de Rei", "Vila do Bispo", "Vila do Conde", "Vila do Porto", "Vimioso",
    "Vinhais", "Viseu", "Vizela", "Vouzela", "Águeda", "Évora", "Ílhavo", "Óbidos",
)
DISTRICTS = (
    "Aveiro", "Beja", "Braga", "Bragança", "Castelo Branco", "Coimbra", "Évora", "Faro", "Guarda", "Leiria",
    "Lisboa", "Portalegre", "Porto", "Santarém", "Setúbal", "Viana do Castelo", "Vila Real", "Viseu",
)
_DISTRICT_EXTRA = ("Açores", "Madeira", "Região Autónoma dos Açores", "Região Autónoma da Madeira", "R.A. Açores",
                   "R.A. Madeira")


def _text(value):
    if value is None or isinstance(value, bool):
        return ""
    return " ".join(str(value).split())


def _fold(text):
    """Lower case without accents: VILA POUCA DE AGUIAR and Vila Pouca de Aguiar are one name."""
    return "".join(c for c in unicodedata.normalize("NFD", text.lower()) if unicodedata.category(c) != "Mn")


_CONCELHOS = frozenset(_fold(name) for name in CONCELHOS) | frozenset(("praia da vitoria", "meda"))
_DISTRICTS = frozenset(_fold(name) for name in DISTRICTS + _DISTRICT_EXTRA)


def validate_pt_dicofre(value):
    """A DICOFRE code: 170301 (a parish), 1703 (a municipality), with a district from 01 to 18, 31, 32 or
    41 to 49. The leading zero added by some layers (0170215) and a decimal tail (170301.0) are dropped."""
    text = _text(value)
    if text.endswith(".0"):
        text = text[:-2]
    if len(text) == 7 and text.startswith("0"):
        text = text[1:]
    if len(text) in (3, 5):
        text = "0" + text
    return bool(_DICOFRE.fullmatch(text))


def validate_pt_bgri_code(value):
    """A subsection code of the BGRI: 17032100111, also with the apostrophe that spreadsheets put before
    it."""
    text = _text(value).lstrip("'")
    if len(text) == 10:
        text = "0" + text
    return bool(_BGRI.fullmatch(text))


def validate_pt_concelho(value):
    """A municipality of Portugal: Abrantes, Águeda, VILA POUCA DE AGUIAR, Agueda."""
    return _fold(_text(value)) in _CONCELHOS


def validate_pt_district(value):
    """A district of Portugal or an autonomous region: Vila Real, FARO, Açores."""
    return _fold(_text(value)) in _DISTRICTS


def validate_pt_quarter(value):
    """A quarter in Portuguese: 4º Trimestre, 1.º trimestre de 2023."""
    return bool(_QUARTER.fullmatch(_text(value)))


def validate_pt_postcode(value):
    """A Portuguese postal code, with the locality that tables write after it: 2765-013, 5460,
    2765-013 Estoril."""
    return bool(_POSTCODE.fullmatch(_text(value)))


# A parish name: Valongo do Vouga, São Pedro da Afurada, UF Águeda e Borralha, Santa Maria Maior (Lisboa).
_FREGUESIA = re.compile(r"[^\W\d_][^\W\d_ '.()/,-]*(?:[ '.()/,-]+[^\W\d_][^\W\d_'.()-]*\)?)*")
_NOT_PARISH = frozenset(("nao conhecido", "nao conhecida", "desconhecido", "desconhecida", "null", "none",
                         "n/a", "na", "outros", "sem informacao"))


def validate_pt_freguesia(value):
    """A civil parish of Portugal: Valongo do Vouga, UF Águeda e Borralha (not 0, -- Não conhecido --)."""
    v = _text(value)
    if not 2 <= len(v) <= 120 or not _FREGUESIA.fullmatch(v):
        return False
    return _fold(v) not in _NOT_PARISH
