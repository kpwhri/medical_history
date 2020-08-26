from enum import Enum

from regexify import Pattern
import regex as re


class MedicalHistoryFlag(Enum):
    UNKNOWN = 0
    NEGATED = 1
    PERSONAL = 2
    DEGREE1 = 3
    DEGREE1_NEG = 4
    DEGREE2 = 5
    DEGREE2_NEG = 6
    OTHER = 7
    OTHER_NEG = 8
    FAMILY = 9
    FAMILY_NEG = 10


MEDICAL_HISTORY_TERMS = {
    'medical history': MedicalHistoryFlag.PERSONAL,
    'no medical history': MedicalHistoryFlag.NEGATED,
    'family history': MedicalHistoryFlag.FAMILY,
    'family medical history': MedicalHistoryFlag.FAMILY,
    'no family history': MedicalHistoryFlag.FAMILY_NEG,
    'no family medical history': MedicalHistoryFlag.FAMILY_NEG,
}

RELATIVES = {
    'mother': MedicalHistoryFlag.DEGREE1,
    'father': MedicalHistoryFlag.DEGREE1,
}


def is_negated(text):
    pat = Pattern('no ((?:past|medical) )* history')
    if m := pat.matches(text):
        return m.group().lower()
    return None


def extract_medical_history_terms(text):
    medhist_pat = re.compile('|'.join(MEDICAL_HISTORY_TERMS.keys()), re.BESTMATCH | re.I)
    for m in medhist_pat.finditer(text):
        yield m.start(), m.end(), MEDICAL_HISTORY_TERMS[' '.join(m.group().lower().split())]


def get_medical_history(text, *targets):
    results = []
    data = []
    target_pat = re.compile(f'({"|".join(targets)})', re.I)
    if term := is_negated(text):
        return (MedicalHistoryFlag.UNKNOWN,), term
    medhist = list(extract_medical_history_terms(text))
    if not medhist:
        return (MedicalHistoryFlag.UNKNOWN,), ('no medical history mention', )
    for m in target_pat.finditer(text):
        for start, end, label in medhist:
            if start > m.end():  # medical history should not occur after
                continue
            if '.' in text[end + 2: m.start()] or ':' in text[end+2: m.start()]:
                continue
            results.append(label)
            data.append(text[start:end].lower())
            data.append(m.group().lower())
    if results:
        return tuple(results), tuple(data)
    else:
        return (MedicalHistoryFlag.UNKNOWN,), ()

