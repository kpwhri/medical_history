from regexify import Pattern
import regex as re

from medical_history.flags import MedicalHistoryFlag, ExcludeFlag
from medical_history.results import Result, ResultList


class Sectioner:
    """What section are we in?"""

    SECTION_RX = re.compile(
        r'('
        r'past medical history'
        r'|family history (indicates|includes)'
        r'|past surgical history'
        r'|problem list'
        r'|family history'
        r'|pmhx'
        r'|mhx'
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
                return idx, label.lower()
        return None, ''


MEDICAL_HISTORY_TERMS = {
    'medical history': MedicalHistoryFlag.PERSONAL,
    'history of': MedicalHistoryFlag.PERSONAL,
    'history': MedicalHistoryFlag.PERSONAL,
    'hx of': MedicalHistoryFlag.PERSONAL,
    'h/o': MedicalHistoryFlag.PERSONAL,
    'hx': MedicalHistoryFlag.PERSONAL,
    'mhx': MedicalHistoryFlag.PERSONAL,
    'pmhx': MedicalHistoryFlag.PERSONAL,
    'pmh': MedicalHistoryFlag.PERSONAL,
    'phx': MedicalHistoryFlag.PERSONAL,
    'no medical history': MedicalHistoryFlag.NEGATED,
    'no significant medical history': MedicalHistoryFlag.NEGATED,
    'family history': MedicalHistoryFlag.FAMILY,
    'significant family history': MedicalHistoryFlag.FAMILY,
    'family medical history': MedicalHistoryFlag.FAMILY,
    'famhx': MedicalHistoryFlag.FAMILY,
    'fmhx': MedicalHistoryFlag.FAMILY,
    'fhx': MedicalHistoryFlag.FAMILY,
    'family hx': MedicalHistoryFlag.FAMILY,
    'no family history': MedicalHistoryFlag.FAMILY_NEG,
    'fh': MedicalHistoryFlag.FAMILY,
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
        yield m, d[match]


def extract_none(text):
    yield from _extract_terms(text, {'none': MedicalHistoryFlag.NONE})


def extract_medical_history_terms(text):
    yield from _extract_terms(text, MEDICAL_HISTORY_TERMS)


def extract_relatives(text):
    yield from _extract_terms(text, RELATIVES)


def _span_is_negated(span):
    pat = re.compile(r'\b(not?|denie(s|d)|none|neg(ative)?)\b', re.I)
    if m := pat.search(span):
        return m
    return None


def _span_is_not_relevant(span):
    pat = re.compile(r'(about|\bbut\b|assess|evaluat|suspect|possib|suspicious|check|please|\?|for|test)', re.I)
    if m := pat.search(span):
        return m
    return None


def _contains_separators(text, seps, max_count=0):
    cnt = 0
    for sep in seps:
        if sep in text:
            cnt += 1
            if cnt > max_count:
                return True
    return False


def _contains_period(text, max_count=0):
    """Exclude dx codes"""
    pat = re.compile(r'[A-Z0-9]\.[A-Z0-9]')  # no ignore case
    text = pat.sub('', text)
    return text.count('.') > max_count


def get_medical_history(text, *targets, max_range=100, metadata=None):
    if metadata:
        Result.METADATA = metadata
    results = ResultList()
    target_pat_str = f'({"|".join(targets)})'
    dx_str = r'(dx|diagnosis|dx\W?d|diagnosed)'
    target_pat = re.compile(fr'\b{target_pat_str}\b', re.I)
    dx_pat = re.compile(
        '('
        fr'({dx_str}\s*(of\s*)?{target_pat_str})'
        fr'|({target_pat_str}\s*{dx_str})'
        fr')',
        re.I
    )
    # if term := is_negated(text):
    #     return (MedicalHistoryFlag.UNKNOWN,), term
    medhist = list(extract_medical_history_terms(text))
    relhist = list(extract_relatives(text))
    nonehist = list(extract_none(text))
    sectioner = Sectioner(text)
    if medhist or relhist:
        for m in target_pat.finditer(text):
            section_idx, section = sectioner.get_section(m.start())
            if 'problem list' in section or section in ['assessment:']:  # recent items
                continue

            # negated patterns
            if find_negated_history_patterns(results, m, max_range, nonehist, section, text):
                continue

            # family history
            found_relatives = False
            if 'family history' in section or 'history' not in section:
                found_relatives = find_in_family_history_section(m, max_range, results, relhist, text)

            # personal history
            find_in_personal_history(m, medhist, found_relatives, results, section, text)

            # determine if in medical history section
            if section:
                result = Result(target=m, section=section, snippet=text[min(0, section_idx - 10):m.end() + 10])
                if 'family history' in section:
                    result.medical_history_flag = MedicalHistoryFlag.FAMILY
                    results.append(result)
                if 'medical history' in section:
                    result.medical_history_flag = MedicalHistoryFlag.PERSONAL
                    results.append(result)

    # look for 'past dx of pcos'
    for m in dx_pat.finditer(text):
        past = find_past_qualifier(m, text)
        maybe = find_maybe_dx(m, text)
        negated = find_negated_dx(m, text)
        result = Result(target=m, secondary=past, qualifier=maybe, qualifier2=negated)
        result.set_context(text)
        if negated:
            result.medical_history_flag = MedicalHistoryFlag.NEGATED
        elif past:
            if maybe:
                result.medical_history_flag = MedicalHistoryFlag.PERSONAL_MAYBE
            else:
                result.medical_history_flag = MedicalHistoryFlag.PERSONAL
        else:
            if maybe:
                result.medical_history_flag = MedicalHistoryFlag.PERSONAL_CURRENT_MAYBE
            else:
                result.medical_history_flag = MedicalHistoryFlag.PERSONAL_CURRENT
    return results


def find_maybe_dx(m, text):
    """Look for any qualification (e.g., 'maybe') related to dx"""
    offset = 20
    target = text[max(0, m.start() - offset): m.end() + offset]
    if m := _span_is_not_relevant(target):
        return m


def find_negated_dx(m, text):
    """Look for any qualification (e.g., 'maybe') related to dx"""
    offset = 20
    target = text[max(0, m.start() - offset): m.end() + offset]
    if m := _span_is_negated(target):
        return m


def find_past_qualifier(m, text):
    """Look for qualification of 'dx condition' to 'past', 'in 2012', etc."""
    offset = 20
    target = text[max(0, m.start() - offset): m.end() + offset]
    past_pat = re.compile(
        r'\b('
        r'\d{4}'  # year mentioned
        r'|prior|past|former|previous'
        r'|age'
        r'|at \d{2}'
        r')\b',
        re.I
    )
    return past_pat.search(target)


def find_in_personal_history(m, medhist, found_relatives, results, section, text):
    not_fam_hx_section = 'family history' not in section and not found_relatives
    for match, label in medhist:
        result = Result(target=m, secondary=match, section=section)
        if not not_fam_hx_section and label != MedicalHistoryFlag.FAMILY:
            continue
        if match.start() > m.end():  # medical history should not occur after
            continue
        result = _find_history_in_section(result, match.end(), m.start(), text, label)
        results.append(result)


def _find_history_in_section(result: Result, start, end, text, label, *, section_seps=':;•*', max_range=None):
    if max_range and end - start > max_range:
        return
    elif _contains_period(text[start: end]):
        result.exclude_flag = ExcludeFlag.DIFFERENT_SENTENCE
    elif _contains_separators(text[start + 2: end], section_seps):
        result.exclude_flag = ExcludeFlag.DIFFERENT_SECTION
    elif _span_is_not_relevant(text[start: end]):
        result.exclude_flag = ExcludeFlag.NOT_RELEVANT

    if neg := _span_is_negated(text[start - 10: end]):
        result.medical_history_flag = NEGATE[label]
        result.qualifier = neg
    else:
        result.medical_history_flag = label
    result.set_context(text)
    return result


def find_in_family_history_section(m, max_range, results, relhist, text):
    curr = []
    for match, label in relhist:
        result = Result(target=m, secondary=match)
        if match.end() < m.start():
            result = _find_history_in_section(result, match.end(), m.start(), text, label,
                                              section_seps=';•*',
                                              max_range=max_range)
        else:
            result = _find_history_in_section(result, m.end(), match.start(), text, label,
                                              max_range=max_range)
        curr.append(result)
    if len(curr) > 2:  # get closest -- minimum snippet length
        for i, val in enumerate(sorted(curr, key=lambda x: -len(x))):
            if i > 0:  # keep only the closest value
                val.exclude_flag = ExcludeFlag.CLOSER_MENTION
    results += curr
    return len(curr) > 0


def find_negated_history_patterns(results, m, max_range, nonehist, section, text):
    for match, label in nonehist:
        if match.end() < m.start() or match.start() - m.start() > max_range:
            continue
        if _contains_separators(text[m.start(): match.start()], ';•*'):
            continue
        if _contains_period(text[m.start(): match.start()]):
            continue
        if not _contains_separators(text[m.start(): match.start()], ':', max_count=1):
            if 'family history' in section:
                result = Result(medical_history_flag=MedicalHistoryFlag.FAMILY_NEG)
            else:
                result = Result(medical_history_flag=MedicalHistoryFlag.NEGATED)
            result.set_targets(text, target=match, qualifier=m)
            results.append(result)
            return True
    return False
