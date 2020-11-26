import regex as re

from medical_history.span_funcs import span_is_negated, span_is_not_relevant


def find_maybe_dx(m, text):
    """Look for any qualification (e.g., 'maybe') related to dx"""
    offset = 20
    target = text[max(0, m.start() - offset): m.end() + offset]
    if m := span_is_not_relevant(target):
        return m


def find_negated_dx(m, text):
    """Look for any qualification (e.g., 'maybe') related to dx"""
    offset = 20
    target = text[max(0, m.start() - offset): m.end() + offset]
    if m := span_is_negated(target):
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
