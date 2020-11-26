import regex as re


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
