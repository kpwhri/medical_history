from medical_history.flags import MedicalHistoryFlag, ExcludeFlag, NEGATE
from medical_history.span_funcs import span_is_negated, span_is_not_relevant, contains_separators, contains_period
from medical_history.results import Result


def find_in_personal_history(m, medhist, found_relatives, results, section, text):
    not_fam_hx_section = 'family history' not in section and not found_relatives
    for match, label in medhist:
        result = Result(target=m, secondary=match, section=section)
        if not not_fam_hx_section and label != MedicalHistoryFlag.FAMILY:
            continue
        if match.start() > m.end():  # medical history should not occur after
            continue
        result = _find_history_in_section(result, match.start(), match.end(), m.start(), text, label)
        results.append(result)


def _find_history_in_section(result: Result, start_first, end_first, start_second, text, label,
                             *, section_seps=':;•*', max_range=None):
    if max_range and start_second - end_first > max_range:
        return
    elif contains_period(text[end_first: start_second]):
        result.exclude_flag = ExcludeFlag.DIFFERENT_SENTENCE
    elif contains_separators(text[end_first + 2: start_second], section_seps):
        result.exclude_flag = ExcludeFlag.DIFFERENT_SECTION
    elif contains_separators(text[end_first: start_second], '\n'):
        result.exclude_flag = ExcludeFlag.DIFFERENT_SECTION
    elif span_is_not_relevant(text[end_first: start_second]):
        result.exclude_flag = ExcludeFlag.NOT_RELEVANT

    if neg := span_is_negated(text[end_first: start_second]):
        result.medical_history_flag = NEGATE[label]
        result.qualifier = neg
    elif neg := span_is_negated(text[max(0, start_first - 10): start_first]):
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
            result = _find_history_in_section(
                result, match.start(), match.end(), m.start(), text, label,
                section_seps=';•*',
                max_range=max_range
            )
        else:
            result = _find_history_in_section(
                result, m.start(), m.end(), match.start(), text, label,
                max_range=max_range)
        if result:
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
        if contains_separators(text[m.start(): match.start()], ';•*'):
            continue
        if contains_period(text[m.start(): match.start()]):
            continue
        if not contains_separators(text[m.start(): match.start()], ':', max_count=1):
            if 'family history' in section:
                result = Result(medical_history_flag=MedicalHistoryFlag.FAMILY_NEG)
            else:
                result = Result(medical_history_flag=MedicalHistoryFlag.NEGATED)
            result.set_targets(text, target=match, qualifier=m)
            results.append(result)
            return True
    return False
