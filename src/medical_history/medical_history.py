from regexify import Pattern
import regex as re

from medical_history.find_history import find_in_personal_history, find_in_family_history_section, \
    find_negated_history_patterns
from medical_history.find_pastdx import find_maybe_dx, find_negated_dx, find_past_qualifier
from medical_history.flags import MedicalHistoryFlag
from medical_history.keywords import MEDICAL_HISTORY_TERMS, RELATIVES
from medical_history.results import Result, ResultList
from medical_history.sectioner import Sectioner


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


def get_medical_history(text, *targets, max_range=100, metadata=None) -> ResultList:
    results = ResultList(metadata=metadata)
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
        results.append(result)
    return results
