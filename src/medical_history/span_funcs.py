import regex as re


def span_is_negated(span):
    pat = re.compile(r'\b(not?|denie(s|d)|none|neg(ative)?)\b', re.I)
    if m := pat.search(span):
        return m
    return None


def span_is_not_relevant(span):
    pat = re.compile(r'(about|\bbut\b|assess|evaluat|suspect|possib|suspicious|check|please|\?|for|test)', re.I)
    if m := pat.search(span):
        return m
    return None


def contains_separators(text, seps, max_count=0):
    cnt = 0
    for sep in seps:
        if sep in text:
            cnt += 1
            if cnt > max_count:
                return True
    return False


def contains_period(text, max_count=0):
    """Exclude dx codes"""
    pat = re.compile(r'[A-Z0-9]\.[A-Z0-9]')  # no ignore case
    text = pat.sub('', text)
    return text.count('.') > max_count
