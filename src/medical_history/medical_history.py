from enum import Enum

from regexify import Pattern
import regex as re


class Sectioner:
    """What section are we in?"""

    SECTION_RX = re.compile(
        r'('
        r'past medical history'
        r'|family history indicates'
        r'|past surgical history'
        r'|problem list'
        r'|[a-z\-]+'
        r')\s?:', re.I
    )

    def __init__(self, text):
        self.sections = []
        for m in self.SECTION_RX.finditer(text):
            if m.group().lower() == 'comment:':
                continue
            self.sections.append((m.start(), m.group()))
        self.sections.reverse()

    def get_section(self, index):
        for idx, label in self.sections:
            if index > idx:
                return label.lower()


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
    'fh of': MedicalHistoryFlag.FAMILY,
    'no fh': MedicalHistoryFlag.FAMILY_NEG,
    'no significant family history': MedicalHistoryFlag.FAMILY_NEG,
    'no significant family medical history': MedicalHistoryFlag.FAMILY_NEG,
}

RELATIVES = {
    'mother': MedicalHistoryFlag.DEGREE1,
    'daughter': MedicalHistoryFlag.DEGREE1,
    'son': MedicalHistoryFlag.DEGREE1,
    'mom': MedicalHistoryFlag.DEGREE1,
    'father': MedicalHistoryFlag.DEGREE1,
    'dad': MedicalHistoryFlag.DEGREE1,
    'brother': MedicalHistoryFlag.DEGREE1,
    'sister': MedicalHistoryFlag.DEGREE1,
    'sibling': MedicalHistoryFlag.DEGREE1,
    'siblings': MedicalHistoryFlag.DEGREE1,
    'grandfather': MedicalHistoryFlag.DEGREE2,
    'grandfathers': MedicalHistoryFlag.DEGREE2,
    'grandpa': MedicalHistoryFlag.DEGREE2,
    'gpa': MedicalHistoryFlag.DEGREE2,
    'grandmother': MedicalHistoryFlag.DEGREE2,
    'gma': MedicalHistoryFlag.DEGREE2,
    'grandmothers': MedicalHistoryFlag.DEGREE2,
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
    'cousin': MedicalHistoryFlag.OTHER,
    'cousins': MedicalHistoryFlag.OTHER,
    'great aunt': MedicalHistoryFlag.OTHER,
    'great uncle': MedicalHistoryFlag.OTHER,
    'great grandfather': MedicalHistoryFlag.OTHER,
    'great grandfathers': MedicalHistoryFlag.OTHER,
    'great grandpa': MedicalHistoryFlag.OTHER,
    'great gpa': MedicalHistoryFlag.OTHER,
    'great grandmother': MedicalHistoryFlag.OTHER,
    'great gma': MedicalHistoryFlag.OTHER,
    'great grandmothers': MedicalHistoryFlag.OTHER,
    'great grandma': MedicalHistoryFlag.OTHER,
    'great grandparent': MedicalHistoryFlag.OTHER,
    'great grandparents': MedicalHistoryFlag.OTHER,
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
    pat = re.compile(rf'\b({"|".join(d.keys())})\b', re.ENHANCEMATCH | re.I)
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


def _span_is_not_relevant(span):
    pat = re.compile(r'\b(about|but)\b', re.I)
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
    target_pat = re.compile(fr'\b({"|".join(targets)})\b', re.I)
    # if term := is_negated(text):
    #     return (MedicalHistoryFlag.UNKNOWN,), term
    medhist = list(extract_medical_history_terms(text))
    relhist = list(extract_relatives(text))
    sectioner = Sectioner(text)
    if not medhist and not relhist:
        return (MedicalHistoryFlag.UNKNOWN,), ('no medical history mention',)
    for m in target_pat.finditer(text):
        section = sectioner.get_section(m.start())
        if section and 'problem list' in section or section in ['assessment:']:
            continue
        for start, end, match, label in medhist:
            if start > m.end():  # medical history should not occur after
                continue
            if _contains_separators(text[end: m.start()], '.'):
                continue
            if _contains_separators(text[end + 2: m.start()], ':;•*'):
                continue
            if _span_is_not_relevant(text[end: m.start()]):
                continue
            if neg := _span_is_negated(text[start - 10:start]):
                results.append(NEGATE[label])
                data += [m.group().lower(), match, neg]
            else:
                results.append(label)
                data += [m.group().lower(), match]
        relatives = []
        for start, end, match, label in relhist:
            if end < m.start():
                if m.start() - end > 100:
                    continue
                if _contains_separators(text[end: m.start()], '.'):
                    continue
                if _contains_separators(text[end + 2: m.start()], ':;•*'):
                    continue
                if _span_is_not_relevant(text[end: m.start()]):
                    continue
                result, datum = relhist_results(m, text[end:m.start()], label, match)
                if neg := _span_is_negated(text[start - 10:start]):
                    result = NEGATE[result]
                    datum.append(neg)
                relatives.append((result, datum, m.start() - end, 1))
            else:
                if start - m.end() > 100:
                    continue
                if _contains_separators(text[m.end(): start], '.'):
                    continue
                if _contains_separators(text[m.end() + 2: start], ':;•*'):
                    continue
                if _span_is_not_relevant(text[m.end(): start]):
                    continue
                result, datum = relhist_results(m, text[m.end():start], label, match)
                if neg := _span_is_negated(text[m.start() - 10:m.start()]):
                    result = NEGATE[result]
                    datum.append(neg)
                relatives.append((result, datum, m.start() - end, 0))
        if relatives:
            result, datum = sorted(relatives, key=lambda x: (x[2], x[3]))[0][:2]
            results.append(result)
            data += datum
        # determine if in medical history section
        if section:
            if 'family history' in section:
                results.append(MedicalHistoryFlag.FAMILY)
                data += [m.group().lower(), section]
            if 'medical history' in section:
                results.append(MedicalHistoryFlag.PERSONAL)
                data += [m.group().lower(), section]

    if results:
        return tuple(results), tuple(data)
    else:
        return (MedicalHistoryFlag.UNKNOWN,), ()
