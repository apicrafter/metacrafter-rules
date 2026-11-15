"""Chilean geography found in the Chilean files of metacrafter-testdata (2024 snapshots of the research data
repositories of the Universidad de Chile, datos.uchile.cl, and the Universidad de Concepción, datav.udec.cl):
the 346 comunas by name, as tables of projects of the environmental assessment system (Lo Barnechea, Til Til,
Paine) and the place of birth of survey respondents (Santiago, Chillán, Temuco) give them.

The names are those of the Código Único Territorial of SUBDERE. Tables write them in capitals or without
accents, with other spellings (Aisén, Coihaique, Tiltil, Llaillay, Marchihue, Trehuaco, Paiguano) and by the
name of the seat (Puerto Natales, Puerto Saavedra, San Vicente de Tagua Tagua).
"""
import re
import unicodedata

CL_COMUNAS = (
    "Algarrobo", "Alhué", "Alto Biobío", "Alto Hospicio", "Alto del Carmen", "Ancud", "Andacollo", "Angol",
    "Antofagasta", "Antuco", "Antártica", "Arauco", "Arica", "Aysén", "Buin", "Bulnes", "Cabildo",
    "Cabo de Hornos", "Cabrero", "Calama", "Calbuco", "Caldera", "Calera de Tango", "Calle Larga", "Camarones",
    "Camiña", "Canela", "Carahue", "Cartagena", "Casablanca", "Castro", "Catemu", "Cauquenes", "Cañete",
    "Cerrillos", "Cerro Navia", "Chaitén", "Chanco", "Chañaral", "Chiguayante", "Chile Chico", "Chillán",
    "Chillán Viejo", "Chimbarongo", "Cholchol", "Chonchi", "Chépica", "Cisnes", "Cobquecura", "Cochamó",
    "Cochrane", "Codegua", "Coelemu", "Coihueco", "Coinco", "Colbún", "Colchane", "Colina", "Collipulli",
    "Coltauco", "Combarbalá", "Concepción", "Conchalí", "Concón", "Constitución", "Contulmo", "Copiapó",
    "Coquimbo", "Coronel", "Corral", "Coyhaique", "Cunco", "Curacautín", "Curacaví", "Curaco de Vélez",
    "Curanilahue", "Curarrehue", "Curepto", "Curicó", "Dalcahue", "Diego de Almagro", "Doñihue", "El Bosque",
    "El Carmen", "El Monte", "El Quisco", "El Tabo", "Empedrado", "Ercilla", "Estación Central", "Florida",
    "Freire", "Freirina", "Fresia", "Frutillar", "Futaleufú", "Futrono", "Galvarino", "General Lagos", "Gorbea",
    "Graneros", "Guaitecas", "Hijuelas", "Hualaihué", "Hualañé", "Hualpén", "Hualqui", "Huara", "Huasco",
    "Huechuraba", "Illapel", "Independencia", "Iquique", "Isla de Maipo", "Isla de Pascua", "Juan Fernández",
    "La Calera", "La Cisterna", "La Cruz", "La Estrella", "La Florida", "La Granja", "La Higuera", "La Ligua",
    "La Pintana", "La Reina", "La Serena", "La Unión", "Lago Ranco", "Lago Verde", "Laguna Blanca", "Laja",
    "Lampa", "Lanco", "Las Cabras", "Las Condes", "Lautaro", "Lebu", "Licantén", "Limache", "Linares",
    "Litueche", "Llanquihue", "Llay-Llay", "Lo Barnechea", "Lo Espejo", "Lo Prado", "Lolol", "Loncoche",
    "Longaví", "Lonquimay", "Los Andes", "Los Lagos", "Los Muermos", "Los Sauces", "Los Vilos", "Los Álamos",
    "Los Ángeles", "Lota", "Lumaco", "Machalí", "Macul", "Maipú", "Malloa", "Marchigüe", "Mariquina",
    "María Elena", "María Pinto", "Maule", "Maullín", "Mejillones", "Melipeuco", "Melipilla", "Molina",
    "Monte Patria", "Mostazal", "Mulchén", "Máfil", "Nacimiento", "Nancagua", "Natales", "Navidad", "Negrete",
    "Ninhue", "Nogales", "Nueva Imperial", "O'Higgins", "Olivar", "Ollagüe", "Olmué", "Osorno", "Ovalle",
    "Padre Hurtado", "Padre Las Casas", "Paihuano", "Paillaco", "Paine", "Palena", "Palmilla", "Panguipulli",
    "Panquehue", "Papudo", "Paredones", "Parral", "Pedro Aguirre Cerda", "Pelarco", "Pelluhue", "Pemuco",
    "Pencahue", "Penco", "Peralillo", "Perquenco", "Petorca", "Peumo", "Peñaflor", "Peñalolén", "Pica",
    "Pichidegua", "Pichilemu", "Pinto", "Pirque", "Pitrufquén", "Placilla", "Portezuelo", "Porvenir",
    "Pozo Almonte", "Primavera", "Providencia", "Puchuncaví", "Pucón", "Pudahuel", "Puente Alto",
    "Puerto Montt", "Puerto Octay", "Puerto Varas", "Pumanque", "Punitaqui", "Punta Arenas", "Puqueldón",
    "Purranque", "Purén", "Putaendo", "Putre", "Puyehue", "Queilén", "Quellón", "Quemchi", "Quilaco",
    "Quilicura", "Quilleco", "Quillota", "Quillón", "Quilpué", "Quinchao", "Quinta Normal", "Quinta de Tilcoco",
    "Quintero", "Quirihue", "Rancagua", "Rauco", "Recoleta", "Renaico", "Renca", "Rengo", "Requínoa", "Retiro",
    "Rinconada", "Romeral", "Ránquil", "Río Bueno", "Río Claro", "Río Hurtado", "Río Ibáñez", "Río Negro",
    "Río Verde", "Saavedra", "Sagrada Familia", "Salamanca", "San Antonio", "San Bernardo", "San Carlos",
    "San Clemente", "San Esteban", "San Fabián", "San Felipe", "San Fernando", "San Gregorio", "San Ignacio",
    "San Javier", "San Joaquín", "San José de Maipo", "San Juan de la Costa", "San Miguel", "San Nicolás",
    "San Pablo", "San Pedro", "San Pedro de Atacama", "San Pedro de La Paz", "San Rafael", "San Ramón",
    "San Rosendo", "San Vicente", "Santa Bárbara", "Santa Cruz", "Santa Juana", "Santa María", "Santiago",
    "Santo Domingo", "Sierra Gorda", "Talagante", "Talca", "Talcahuano", "Taltal", "Temuco", "Teno",
    "Teodoro Schmidt", "Tierra Amarilla", "Til Til", "Timaukel", "Tirúa", "Tocopilla", "Toltén", "Tomé",
    "Torres del Paine", "Tortel", "Traiguén", "Treguaco", "Tucapel", "Valdivia", "Vallenar", "Valparaíso",
    "Vichuquén", "Victoria", "Vicuña", "Vilcún", "Villa Alegre", "Villa Alemana", "Villarrica", "Vitacura",
    "Viña del Mar", "Yerbas Buenas", "Yumbel", "Yungay", "Zapallar", "Ñiquén", "Ñuñoa",
)

# Other spellings and the names of seats that stand for the comuna.
_VARIANTS = (
    "Aisén", "Puerto Aysén", "Puerto Aisén", "Coihaique", "Tiltil", "Llaillay", "Marchihue", "Trehuaco",
    "Paiguano", "Puerto Natales", "Puerto Saavedra", "Puerto Cisnes", "Puerto Williams",
    "San Vicente de Tagua Tagua", "San Francisco de Mostazal", "Calera", "Santiago Centro", "Alto Bío-Bío",
    "Chol Chol", "OHiggins", "Villa O'Higgins", "Hanga Roa", "Rapa Nui", "Antártica Chilena",
    "San Fabián de Alico",
)
_PUNCT = re.compile(r"[-‐-―.,;:()\[\]\"'’`/_*]+")


def _fold(value):
    """Lower case without accents (ñ becomes n), punctuation as spaces."""
    text = unicodedata.normalize("NFKD", str(value).lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return " ".join(_PUNCT.sub(" ", text).split())


_COMUNAS = frozenset(_fold(name) for name in CL_COMUNAS + _VARIANTS)
_NO_ANSWER = frozenset((
    "otra", "otro", "otras", "otra comuna", "sin informacion", "no sabe", "no responde", "ninguna", "no aplica",
    "sin dato", "extranjero", "fuera del pais", "total",
))
_PREFIX = re.compile(r"^(?:comuna|municipalidad|i municipalidad|ilustre municipalidad)(?: de)? ")


def validate_cl_comuna(value):
    """A comuna of Chile by name: Lo Barnechea, Til Til, CONCEPCION, Viña del Mar, Puerto Saavedra,
    Comuna de Maipú (not Cachapoal, Metropolitana, 13101 or Buenos Aires)."""
    text = _fold(value)
    if not text or len(text) > 40:
        return False
    return text in _COMUNAS or _PREFIX.sub("", text) in _COMUNAS


def validate_cl_comuna_or_none(value):
    """What a field named for comunas holds: a comuna or a marker of no comuna (Otra, Sin información)."""
    return validate_cl_comuna(value) or _fold(value) in _NO_ANSWER
