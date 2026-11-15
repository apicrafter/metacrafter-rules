"""Option codes of survey forms. KoboToolbox, ODK and similar tools store the chosen option of a question by
its name, which they make from the label: lower case, spaces and punctuation as underscores and every
non-ASCII letter as an underscore too, cut at some length (soltero_a for Soltero/a, educaci_n_media_completa
for Educación media completa, m_s_de_5_a_os for Más de 5 años). Found in the NEMS-P-Ch pilot survey of the
Universidad de Chile (datos.uchile.cl, a 2024 snapshot; metacrafter-testdata)."""
import re
import unicodedata

_SPLIT = re.compile(r"[\s_/,;:()\[\]+&.¿?¡!-]+")
_LOST = "aeioun"


def fold(value):
    """Lower case without accents."""
    text = unicodedata.normalize("NFKD", str(value).strip().lower().replace("’", "'"))
    return "".join(c for c in text if not unicodedata.combining(c))


def form_words(value, known=frozenset()):
    """The words of a label or of an option code. Two pieces around a lost accented letter are joined
    when the whole is a known word (educaci + n: educacion, b + sico: basico, m + s: mas, dej +
    nothing: deje)."""
    tokens = [t for t in _SPLIT.split(fold(value)) if t]
    if not known:
        return tokens
    words = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token not in known:
            if i + 1 < len(tokens):
                joined = next((token + c + tokens[i + 1] for c in _LOST if token + c + tokens[i + 1] in known), None)
                if joined:
                    words.append(joined)
                    i += 2
                    continue
            ended = next((token + c for c in _LOST if token + c in known), None)
            if ended and i == len(tokens) - 1:
                token = ended
        words.append(token)
        i += 1
    return words


def form_text(value, known=frozenset()):
    """The words of form_words joined by spaces."""
    return " ".join(form_words(value, known))
