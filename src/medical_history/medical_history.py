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
    'history of': MedicalHistoryFlag.PERSONAL,
    'history': MedicalHistoryFlag.PERSONAL,
    'hx of': MedicalHistoryFlag.PERSONAL,
    'hx': MedicalHistoryFlag.PERSONAL,
    'no medical history': MedicalHistoryFlag.NEGATED,
    'no significant medical history': MedicalHistoryFlag.NEGATED,
    'family history': MedicalHistoryFlag.FAMILY,
    'significant family history': MedicalHistoryFlag.FAMILY,
    'family medical history': MedicalHistoryFlag.FAMILY,
    'famhx': MedicalHistoryFlag.FAMILY,
    'family hx': MedicalHistoryFlag.FAMILY,
    'no family history': MedicalHistoryFlag.FAMILY_NEG,
    'no significant family history': MedicalHistoryFlag.FAMILY_NEG,
    'no significant family medical history': MedicalHistoryFlag.FAMILY_NEG,
}

RELATIVES = {
    'mother': MedicalHistoryFlag.DEGREE1,
    'mom': MedicalHistoryFlag.DEGREE1,
    'father': MedicalHistoryFlag.DEGREE1,
    'dad': MedicalHistoryFlag.DEGREE1,
    'brother': MedicalHistoryFlag.DEGREE1,
    'sister': MedicalHistoryFlag.DEGREE1,
    'sibling': MedicalHistoryFlag.DEGREE1,
    'siblings': MedicalHistoryFlag.DEGREE1,
    'grandfather': MedicalHistoryFlag.DEGREE2,
    'grandpa': MedicalHistoryFlag.DEGREE2,
    'grandmother': MedicalHistoryFlag.DEGREE2,
    'grandma': MedicalHistoryFlag.DEGREE2,
    'grandparent': MedicalHistoryFlag.DEGREE2,
    'grandparents': MedicalHistoryFlag.DEGREE2,
    'aunt': MedicalHistoryFlag.DEGREE2,
    'uncle': MedicalHistoryFlag.DEGREE2,
    'niece': MedicalHistoryFlag.DEGREE2,
    'nephew': MedicalHistoryFlag.DEGREE2,
    'half-brother': MedicalHistoryFlag.DEGREE2,
    'half brother': MedicalHistoryFlag.DEGREE2,
    'half-sister': MedicalHistoryFlag.DEGREE2,
    'half sister': MedicalHistoryFlag.DEGREE2,
    'half-sibling': MedicalHistoryFlag.DEGREE2,
    'half sibling': MedicalHistoryFlag.DEGREE2,
    'half-siblings': MedicalHistoryFlag.DEGREE2,
    'half siblings': MedicalHistoryFlag.DEGREE2,
}

NEGATE = {  # how to negate all the flags
    MedicalHistoryFlag.UNKNOWN: MedicalHistoryFlag.UNKNOWN,
    MedicalHistoryFlag.NEGATED: MedicalHistoryFlag.NEGATED,
    MedicalHistoryFlag.PERSONAL: MedicalHistoryFlag.NEGATED,
    MedicalHistoryFlag.DEGREE1: MedicalHistoryFlag.DEGREE1_NEG,
    MedicalHistoryFlag.DEGREE1_NEG: MedicalHistoryFlag.DEGREE1_NEG,
    MedicalHistoryFlag.DEGREE2: MedicalHistoryFlag.DEGREE2_NEG,
    MedicalHistoryFlag.DEGREE2_NEG: MedicalHistoryFlag.DEGREE2_NEG,
    MedicalHistoryFlag.OTHER: MedicalHistoryFlag.OTHER_NEG,
    MedicalHistoryFlag.OTHER_NEG: MedicalHistoryFlag.OTHER_NEG,
    MedicalHistoryFlag.FAMILY: MedicalHistoryFlag.FAMILY_NEG,
    MedicalHistoryFlag.FAMILY_NEG: MedicalHistoryFlag.FAMILY_NEG,
}


def is_negated(text):
    pat = Pattern('no ((?:past|medical) )* history')
    if m := pat.matches(text):
        return m.group().lower()
    return None


def _extract_terms(text, d):
    pat = re.compile('|'.join(d.keys()), re.ENHANCEMATCH | re.I)
    for m in pat.finditer(text):
        match = ' '.join(m.group().lower().split())
        yield m.start(), m.end(), match, d[match]


def extract_medical_history_terms(text):
    yield from _extract_terms(text, MEDICAL_HISTORY_TERMS)


def extract_relatives(text):
    yield from _extract_terms(text, RELATIVES)


def _span_is_negated(span):
    pat = re.compile(r'\b(not?)\b', re.I)
    if m := pat.search(span):
        return m.group().lower()
    return None


def relhist_results(m, span, label, match):
    if neg := _span_is_negated(span):
        return NEGATE[label], [m.group().lower(), match, neg]
    return label, [m.group().lower(), match]


def _contains_separators(text, seps, max_count=0):
    cnt = 0
    for sep in seps:
        if sep in text:
            cnt += 1
            if cnt > max_count:
                return True
    return False


def get_medical_history(text, *targets):
    results = []
    data = []
    target_pat = re.compile(f'({"|".join(targets)})', re.I)
    # if term := is_negated(text):
    #     return (MedicalHistoryFlag.UNKNOWN,), term
    medhist = list(extract_medical_history_terms(text))
    relhist = list(extract_relatives(text))
    if not medhist and not relhist:
        return (MedicalHistoryFlag.UNKNOWN,), ('no medical history mention',)
    for m in target_pat.finditer(text):
        for start, end, match, label in medhist:
            if start > m.end():  # medical history should not occur after
                continue
            if _contains_separators(text[end + 2: m.start()], '.:;'):
                continue
            if neg := _span_is_negated(text[start - 10:start]):
                results.append(NEGATE[label])
                data += [m.group().lower(), match, neg]
            else:
                results.append(label)
                data += [m.group().lower(), match]
        for start, end, match, label in relhist:
            if end < m.start():
                if m.start() - end > 100:
                    continue
                result, datum = relhist_results(m, text[end:m.start()], label, match)
                if neg := _span_is_negated(text[start - 10:start]):
                    result = NEGATE[result]
                    datum.append(neg)
                results.append(result)
                data += datum
            else:
                if start - m.end() > 100:
                    continue
                result, datum = relhist_results(m, text[m.end():start], label, match)
                if neg := _span_is_negated(text[m.start() - 10:m.start()]):
                    result = NEGATE[result]
                    datum.append(neg)
                results.append(result)
                data += datum

    if results:
        return tuple(results), tuple(data)
    else:
        return (MedicalHistoryFlag.UNKNOWN,), ()
