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
