"""Procurement methods: the type of procedure by which a public buyer awards a contract (open
tender, restricted procedure, direct award), as procurement registers write it in Spanish,
Portuguese, French, Italian, German, English, Estonian, Russian and Japanese, and the codes of
the OCDS method and eForms procedure type code lists.

Found in the ARSAT purchase orders (Argentina: Contratacion directa - Inciso F, Compras Menores,
Licitacion Publica Nacional), the public works of the City of Buenos Aires, the contract
registers of Madrid, the SIPOT direct awards of Veracruz, the French DECP, the Estonian contract
notices and the bid results of Tochigi of metacrafter-testdata.
"""
import re
import unicodedata

# Words of procedure names, folded to lower-case ASCII (Cyrillic and Japanese are kept). A value
# is a procurement method when it starts with one of them and adds at most a few words (Nacional,
# Internacional, - Inciso F, BAC, (art. 9 inc. c)). They are long enough not to be other words.
_PHRASES = {
    # Spanish: Argentina (Decreto 1030/2016, the procurement rules of ARSAT, BAC of Buenos Aires),
    # Spain (Ley 9/2017), Mexico (LAASSP), Chile (ChileCompra), Colombia, Peru, Uruguay
    "licitacion publica", "licitacion privada", "licitacion abreviada", "licitacion restringida",
    "licitacion internacional", "licitacion nacional", "contratacion directa", "compra directa",
    "compra menor", "compras menores", "contrato menor", "contratos menores", "concurso de precios",
    "concurso publico", "concurso privado", "concurso de meritos", "concurso de proyectos",
    "subasta publica", "subasta inversa", "subasta electronica", "adjudicacion directa",
    "adjudicacion simplificada", "invitacion a cuando menos tres", "invitacion restringida",
    "seleccion abreviada", "minima cuantia", "procedimiento abierto", "abierto simplificado",
    "procedimiento restringido", "negociado sin publicidad", "negociado con publicidad",
    "procedimiento negociado", "dialogo competitivo", "asociacion para la innovacion",
    "basado en acuerdo marco", "trato directo", "comparacion de precios", "procedimiento abreviado",
    "procedimiento especial de seleccion", "convenio marco",
    # Portuguese: Brazil (Lei 8.666/1993, Lei 14.133/2021), Portugal (Código dos Contratos Públicos)
    "pregao eletronico", "pregao presencial", "pregao", "concorrencia publica", "concorrencia",
    "tomada de precos", "dispensa de licitacao", "dispensa", "inexigibilidade", "ajuste direto",
    "consulta previa", "concurso limitado por previa qualificacao", "procedimento de negociacao",
    "dialogo concorrencial", "leilao", "credenciamento",
    # French: Code de la commande publique
    "procedure adaptee", "appel d'offres", "appel d offres", "procedure avec negociation",
    "procedure negociee", "procedure concurrentielle avec negociation", "marche negocie",
    "marche passe sans publicite", "marche sans publicite", "marche public negocie",
    "marche public negocie sans publicite", "marche public passe sans publicite", "dialogue competitif",
    "partenariat d'innovation", "partenariat d innovation", "concours restreint",
    # Italian: Codice dei contratti pubblici
    "procedura aperta", "procedura ristretta", "procedura negoziata", "affidamento diretto",
    "procedura competitiva con negoziazione", "dialogo competitivo", "partenariato per l'innovazione",
    "cottimo fiduciario", "affidamento in economia",
    # German: GWB, VgV, UVgO, VOB/A, BVergG
    "offenes verfahren", "nichtoffenes verfahren", "nicht offenes verfahren", "verhandlungsverfahren",
    "offentliche ausschreibung", "oeffentliche ausschreibung", "beschrankte ausschreibung",
    "beschraenkte ausschreibung", "freihandige vergabe", "freihaendige vergabe", "direktauftrag",
    "direktvergabe", "verhandlungsvergabe", "wettbewerblicher dialog", "innovationspartnerschaft",
    # English: EU directives, OCDS, World Bank, UK
    "open procedure", "restricted procedure", "negotiated procedure", "competitive dialogue",
    "innovation partnership", "competitive procedure with negotiation", "competitive flexible procedure",
    "open tender", "open tendering", "restricted tender", "selective tender", "selective tendering",
    "limited tender", "limited tendering", "direct award", "direct procurement", "direct contracting",
    "single source", "sole source", "request for quotation", "request for quotations",
    "request for proposal", "request for proposals", "national competitive bidding",
    "international competitive bidding", "competitive bidding", "invitation to tender",
    "call for competition",
    # Estonian: riigihangete seadus
    "avatud hankemenetlus", "piiratud hankemenetlus", "lihthange", "vaikehange",
    "valjakuulutamiseta labiraakimistega hankemenetlus", "labiraakimistega hankemenetlus",
    "konkurentsipohine labiraakimistega hankemenetlus", "voistlev dialoog", "innovatsioonipartnerlus",
    # Russian: 44-FZ, 223-FZ
    "открытый конкурс", "открытый аукцион", "электронный аукцион", "аукцион в электронной форме",
    "запрос котировок", "запрос предложений", "конкурс с ограниченным участием",
    "закупка у единственного поставщика", "единственный поставщик",
}

# Japanese public works and goods contracts: open, designated and conditional competitive bidding,
# negotiated contracts (随意契約), proposals.
PROCUREMENT_METHOD_JA = ("一般競争入札", "指名競争入札", "随意契約", "公募型プロポーザル", "プロポーザル方式",
                         "見積合わせ", "総合評価落札方式")

# Codes of the OCDS method code list and of the eForms / TED procedure type code list, accepted in
# a field named for the procedure only.
PROCUREMENT_METHOD_CODES = frozenset((
    "open", "selective", "limited", "direct", "restricted", "neg-w-call", "neg-wo-call", "comp-dial",
    "comp-tend", "innovation", "oth-single", "oth-mult", "negotiated", "competitive dialogue",
    "abierto", "restringido", "negociado", "ouvert", "restreint", "aperta", "ristretta", "negoziata",
    "offen", "nicht offen", "avatud", "piiratud"))

_MAX_EXTRA = 40


def _fold(value):
    text = unicodedata.normalize("NFKD", str(value))
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.replace("’", "'").lower()
    text = re.sub(r"[\s_]+", " ", text)
    return text.strip(" .;:-")


# Folded like the values (й loses its breve), longest first so that the longest phrase decides.
PROCUREMENT_METHOD_PHRASES = tuple(sorted({_fold(p) for p in _PHRASES}, key=len, reverse=True))


def validate_procurement_method(value):
    """A procurement procedure written out: Licitación Pública Nacional, Contratacion directa -
    Inciso F, Procédure adaptée, Appel d'offres ouvert, Pregão eletrônico, Offenes Verfahren,
    Avatud hankemenetlus, 指名競争入札; not a code alone and not a sentence that names one."""
    text = _fold(value)
    if not text or len(text) > 120:
        return False
    for word in PROCUREMENT_METHOD_JA:
        if word in text and len(text) <= len(word) + 12:
            return True
    for phrase in PROCUREMENT_METHOD_PHRASES:
        if text.startswith(phrase):
            rest = text[len(phrase):]
            if rest and rest[0].isalnum() and phrase[-1].isalnum():
                continue  # "concurso" is not "concursos de belleza"; "pregao" not "pregaoeiro"
            return len(rest.strip()) <= _MAX_EXTRA and not re.search(r"\d{3,}", rest)
    return False


def validate_procurement_method_or_code(value):
    """A procurement procedure written out, or a code of the OCDS method (open, selective,
    limited, direct) or eForms procedure type (neg-wo-call, oth-single) code lists; for fields
    named after the procedure."""
    text = _fold(value)
    return text in PROCUREMENT_METHOD_CODES or validate_procurement_method(value)
