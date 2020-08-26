from enum import Enum

from regexify import Pattern


class MedicalHistoryFlag(Enum):
    UNKNOWN = 0


def is_negated(text):
    pat = Pattern('no ((?:past|medical) )* history')
    if m := pat.matches(text):
        return m.group().lower()
    return None


def get_medical_history(text, *targets):
    if term := is_negated(text):
        return MedicalHistoryFlag.NEGATED, term
