"""Names of higher taxa: the scientific names of ranks above the genus that a value alone shows.

Domains, kingdoms, phyla and subphyla, and the classes and orders of animals whose names have no
standard ending, as in the GBIF Backbone Taxonomy and the Catalogue of Life (Eukaryota, Animalia,
Arthropoda, Hexapoda, Insecta, Mammalia, Primates). The other ranks have Latin endings that the
nomenclature codes fix: families -idae (animals) and -aceae (plants, fungi), subfamilies -inae
and -oideae, superfamilies -oidea, classes -opsida, -phyceae and -mycetes, phyla -phyta and
-mycota; insect orders end in -ptera and bird and fish orders in -formes. Genera, tribes (-ini,
also Italian surnames), subtribes (-ina) and plant and fungal orders (-ales, also Spanish
plurals) are not told by a value.
"""
import re

HIGHER_TAXA = frozenset("""
Eukaryota Prokaryota Bacteria Archaea Animalia Plantae Fungi Protozoa Chromista Protista Viruses

Acanthocephala Annelida Arthropoda Brachiopoda Bryozoa Chaetognatha Chordata Cnidaria Ctenophora
Cycliophora Dicyemida Echinodermata Entoprocta Gastrotricha Gnathostomulida Hemichordata
Kinorhyncha Loricifera Micrognathozoa Mollusca Nematoda Nematomorpha Nemertea Onychophora
Orthonectida Phoronida Placozoa Platyhelminthes Porifera Priapulida Rotifera Sipuncula Tardigrada
Xenacoelomorpha Amoebozoa Apicomplexa Cercozoa Ciliophora Euglenozoa Foraminifera Myzozoa
Actinobacteria Bacteroidetes Cyanobacteria Firmicutes Proteobacteria

Cephalochordata Chelicerata Crustacea Hexapoda Myriapoda Tunicata Vertebrata

Actinopterygii Amphibia Arachnida Aves Bivalvia Branchiopoda Calcarea Cephalopoda Cestoda
Chilopoda Chondrichthyes Chromadorea Clitellata Collembola Copepoda Crinoidea Cubozoa Demospongiae
Diplopoda Diplura Elasmobranchii Enoplea Entognatha Gastropoda Hexactinellida Hydrozoa Insecta
Malacostraca Mammalia Maxillopoda Merostomata Monogenea Ostracoda Pauropoda Polychaeta
Polyplacophora Protura Pycnogonida Reptilia Sarcopterygii Scaphopoda Scyphozoa Symphyla Anthozoa
Thaliacea Trematoda

Acari Amphipoda Anura Araneae Artiodactyla Blattodea Carnivora Caudata Cetacea Cingulata
Crocodylia Decapoda Didelphimorphia Diprotodontia Eulipotyphla Gymnophiona Isopoda Lagomorpha
Mantodea Opiliones Perissodactyla Phasmida Pilosa Primates Proboscidea Pseudoscorpiones Psocodea
Rodentia Scorpiones Sirenia Squamata Testudines Urodela Odonata
""".split())

# Endings fixed by the codes of nomenclature, with the shortest stem before each (the capital
# included): Poaceae, Diptera; not Informes or Uniformes (Spanish reports, uniforms). The
# order ending -ales is left out: Spanish plurals have it (Municipales, Federales, Generales).
_RANK_ENDINGS = (
    ("idae", 2), ("aceae", 2), ("inae", 2), ("oideae", 2), ("oidea", 2), ("ptera", 2), ("opsida", 2),
    ("phyceae", 2), ("mycetes", 2), ("mycota", 2), ("phyta", 2), ("formes", 4),
)
_LATIN_WORD = re.compile(r"^[A-Z][a-z]{3,39}$")


def validate_higher_taxon_name(value):
    """The name of a taxon above the genus that its value shows: a listed domain, kingdom, phylum,
    class or order (Eukaryota, Animalia, Arthropoda, Insecta, Primates), or one capitalized Latin
    word with the ending of its rank (Formicidae, Rosaceae, Myrmicinae, Formicoidea, Hymenoptera,
    Passeriformes, Magnoliopsida). Genera (Tetramorium) and species are not."""
    if not isinstance(value, str):
        return False
    text = value.strip()
    if not _LATIN_WORD.match(text):
        return False
    if text in HIGHER_TAXA:
        return True
    return any(text.endswith(ending) and len(text) - len(ending) >= stem for ending, stem in _RANK_ENDINGS)


# Darwin Core lifeStage values: the GBIF LifeStage vocabulary and the words and abbreviations of
# fish, invertebrate, coral and plant surveys.
LIFE_STAGES = frozenset("""
adult adults subadult sub-adult juvenile juveniles immature mature larva larvae larval egg eggs
embryo embryos pupa pupae nymph nymphs imago instar seedling seedlings sapling saplings spore
spores gametophyte sporophyte zygote yearling neonate hatchling fledgling chick nestling calf cub
fry fingerling smolt parr alevin recruit recruits settler settlers megalopa zoea nauplius
copepodite veliger polyp medusa planula ephyra cyprid postlarva post-larva young yoy
ad adu juv juvs sa imm lar
""".split())


def validate_life_stage(value):
    """A life stage: adult, juvenile, larva, AD, JUV, sub-adult, young of year."""
    text = " ".join(str(value).strip().lower().split())
    if text in LIFE_STAGES or text in ("young of year", "young of the year"):
        return True
    return text.rstrip(".") in LIFE_STAGES


# Common names of species: one to six words of letters, with the scientific name in brackets after
# them as wildlife reports write it (australian magpie (cracticus tibicen); masked lapwing - plover
# (vanellus miles)). Swooping bird reports and fishing surveys of Camden Council (New South Wales).
_VERNACULAR_WORD = r"[^\W\d_][^\W\d_'’.-]*(?:['’-][^\W\d_]+)*\.?"
_VERNACULAR_NAME = re.compile(rf"^{_VERNACULAR_WORD}(?:(?: | - | / |/|-){_VERNACULAR_WORD}){{0,5}}$")
_WITH_SCIENTIFIC = re.compile(rf"^(.+?) \(([A-Za-z][a-z]+ (?:x )?[a-z][a-z-]+(?: [a-z][a-z-]+)?)\)$")


def validate_vernacular_name(value):
    """A common name of a taxon, alone or with the scientific name in brackets: European Carp,
    Australian Bass, noisy miner, masked lapwing - plover (vanellus miles), London plane (not 1234,
    a sentence of seven words or more, or Animalia)."""
    text = " ".join(str(value).split())
    if not 2 <= len(text) <= 100:
        return False
    m = _WITH_SCIENTIFIC.match(text)
    if m:
        text = m.group(1)
    if text in HIGHER_TAXA:
        return False
    return bool(_VERNACULAR_NAME.match(text))


def validate_vernacular_with_scientific(value):
    """A common name followed by the scientific name in brackets: australian magpie (cracticus tibicen),
    Noisy Miner (Manorina melanocephala) (not Manorina melanocephala or noisy miner alone)."""
    text = " ".join(str(value).split())
    m = _WITH_SCIENTIFIC.match(text)
    return bool(m) and validate_vernacular_name(m.group(1))


# Threat categories in words: the IUCN Red List categories, the EPBC Act 1999 (Conservation
# Dependent), Queensland (Special Least Concern) and the ACT Nature Conservation Act 2014
# (Regionally Conservation Dependent). The abbreviations (CR, EN, VU) are iucn_red_list_category.
CONSERVATION_STATUSES = frozenset(
    s.lower()
    for s in (
        "Extinct", "Extinct in the Wild", "Critically Endangered", "Critically Endangered (Possibly Extinct)",
        "Endangered", "Vulnerable", "Near Threatened", "Least Concern", "Data Deficient", "Not Evaluated",
        "Conservation Dependent", "Regionally Conservation Dependent", "Special Least Concern", "Rare",
    )
)


def validate_conservation_status(value):
    """A conservation status in words: Critically Endangered, Vulnerable, Regionally Conservation
    Dependent, Least concern (not VU, Bird or Current)."""
    return " ".join(str(value).strip().split()).lower() in CONSERVATION_STATUSES
