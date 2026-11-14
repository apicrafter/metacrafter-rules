"""Validators of linguistic annotation: part-of-speech tags of annotated corpora and tagger output.

Found in a dataset of the Academic Data Repository of the Universidad Nacional de Rosario
(RDA-UNR, Argentina; metacrafter-testdata, 2026-11-14): a Spanish text tagged with the Smorph
tagger, one row per token with its tags in columns named ETIQUETA_1, ETIQUETA_CORRECTA.
"""
import re

# Universal Dependencies v2 (upos_tag).
UD_TAGS = frozenset("ADJ ADP ADV AUX CCONJ DET INTJ NOUN NUM PART PRON PROPN PUNCT SCONJ SYM VERB X".split())

# Penn Treebank, with its punctuation and bracket tags.
PENN_TAGS = frozenset(
    "CC CD DT EX FW IN JJ JJR JJS LS MD NN NNS NNP NNPS PDT POS PRP PRP$ RB RBR RBS RP SYM TO UH "
    "VB VBD VBG VBN VBP VBZ WDT WP WP$ WRB -LRB- -RRB- -NONE- HYPH NFP ADD AFX GW XX . , : `` '' $ #".split()
)

# Short lowercase tags of rule-based taggers and teaching tag sets: the Smorph tagger of
# Spanish (nom, det, prep, cl for clitics, cop for copulas, contr for contractions, npr for
# proper names, comill and guion for quotes and dashes, descon for unknown words), and the
# lowercase forms of common word classes in English, Spanish, French, German and Portuguese.
SHORT_TAGS = frozenset(
    "nom npr det art prep v aux cop adj adv pron rel cl sub cj conj ccong scong disy interr int_ab "
    "intj interj num numer cardin ordin numrom pun punct coma comill guion parent dosp puncom ray_ob "
    "contr descon abr pesos porcen prindf prdem prpers prpos indf "
    "noun verb propn adp det part sym cconj sconj "
    "nc np vb "
    "sust sus vrb vaux adjetivo adverbio preposicion conjuncion pronombre determinante articulo "
    "nome verbo adjetivo advérbio preposição conjunção pronome artigo numeral "
    "nom_propre nom_commun adjectif adverbe verbe pronom déterminant préposition conjonction "
    "nn ne vvfin vafin vmfin vvinf vvpp adja adjd appr apprart art kon kous pper ppos pdat pds "
    "prels ptkneg ptkvz ptkzu card itj xy".split()
)

# EAGLES tags of Spanish, Catalan and Portuguese corpora and FreeLing: a category letter and
# its attributes (NCMS000 common noun, VMIP3S0 main verb, SPS00 preposition, DA0MS0 article,
# Fc comma, Zm currency amount). Letters alone (I, W, Z) are left out: a column of
# single letters is a code.
_EAGLES = re.compile(
    r"A[OQ0][0ACS][MFC0][SPN0][PN0]?|C[CS]|D[ADEIPTNR0][0123][MFC0][SPN0][SP0]?|F[a-z]{1,4}|"
    r"N[CP][MFC0][SPN0][0-9A-Z]{0,3}|P[0DEIPRTX][0123][MFC0][SPN0][NAOD0][SP0]?[0A]?|R[GN]|"
    r"S[PS][SC0]?[MFC0]?[SPN0]?|V[MAS][INMGPS][PIFSC0][123][SP0][MF0]|Z[dmpu]"
)

# Placeholders of an empty second tag: S/E (sin etiqueta) in the Smorph tables.
NO_TAG = frozenset({"S/E", "s/e"})


def validate_pos_tag(value):
    """A part-of-speech tag of a known tag set: Universal Dependencies (NOUN, DET), Penn
    Treebank (NN, VBZ), EAGLES / FreeLing (NCMS000, VMIP3S0, Fc), short lowercase tags of
    rule-based taggers (nom, det, prep, cl, pun) and the S/E placeholder of a token without a
    second tag."""
    text = str(value).strip()
    if not text or len(text) > 12:
        return False
    if text in UD_TAGS or text in PENN_TAGS or text in NO_TAG:
        return True
    if text.lower() in SHORT_TAGS and (text.islower() or text.isupper() or text.istitle()):
        return True
    return bool(_EAGLES.fullmatch(text))
