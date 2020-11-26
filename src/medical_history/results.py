from collections.abc import MutableSequence
from typing import re
from dataclasses import dataclass

from medical_history.flags import MedicalHistoryFlag, ExcludeFlag


@dataclass
class Result:
    METADATA = dict()

    target: re.Match = None
    secondary: re.Match = None
    snippet: str = None
    qualifier: re.Match = None
    qualifier2: re.Match = None
    section: str = None
    medical_history_flag: MedicalHistoryFlag = MedicalHistoryFlag.UNKNOWN
    exclude_flag: ExcludeFlag = ExcludeFlag.INCLUDE

    def __len__(self):
        return len(self.snippet) if self.snippet else 0

    def set_targets(self, text, target: re.Match = None, secondary: re.Match = None,
                    qualifier: re.Match = None, qualifier2: re.Match = None,
                    lowercase=True, window=10):
        if target:
            self.target = target
        if secondary:
            self.secondary = secondary
        if qualifier:
            self.qualifier = qualifier
        if qualifier2:
            self.qualifier2 = qualifier2
        self.set_context(text, window=window)

    def set_context(self, text, window=10):
        args = [t for t in (self.target, self.secondary, self.qualifier, self.qualifier2) if t]
        min_value = max(0, min(m.start() for m in args if m) - window)
        max_value = max(m.start() for m in args if m) + window
        self.snippet = text[min_value: max_value]

    @property
    def terms(self):
        terms = set(x.group().lower() for x in [self.target, self.secondary, self.qualifier, self.qualifier2] if x)
        # if self.section:
        #     terms.add(self.section)
        return terms

    def to_dict(self):
        return {**self.METADATA,
                'target': self.target.group() if self.target else None,
                'secondary': self.secondary.group() if self.secondary else None,
                'snippet': self.snippet,
                'qualifier': self.qualifier.group() if self.qualifier else None,
                'qualifier2': self.qualifier2.group() if self.qualifier2 else None,
                'medical_history_flag': self.medical_history_flag.name,
                'excluded_flag': self.exclude_flag.name,
                'section': self.section,
                'terms': ','.join(self.terms)
                }

    def to_json(self):
        return str(self.to_dict())


class ResultList(MutableSequence):

    def __init__(self, *, metadata=None):
        self.data = []
        if metadata:
            Result.METADATA = metadata
        else:
            Result.METADATA = {}

    def insert(self, index: int, result: Result) -> None:
        self.data.insert(index, result)

    def __len__(self) -> int:
        return len(self.data)

    def __delitem__(self, i):
        self.data.__delitem__(i)

    def __getitem__(self, i):
        return self.data.__getitem__(i)

    def __setitem__(self, i, val):
        self.data.__setitem__(i, val)

    def append(self, result: Result):
        self.data.append(result)

    def __iter__(self):
        yield from self.data

    def __iadd__(self, other):
        self.data += other

    def to_jsonl(self):
        return '\n'.join(self.iter_json())

    def iter_dict(self):
        for result in self.data:
            yield result.to_dict()

    def iter_json(self):
        for result in self.data:
            yield result.to_json()

    def iter_included(self, *, include_all=False):
        for result in self.data:
            if include_all or result.exclude_flag == ExcludeFlag.INCLUDE:
                yield result

    def iter_terms(self, *, include_all=False, include_section=False):
        for result in self.data:
            if include_all or result.exclude_flag == ExcludeFlag.INCLUDE:
                yield from result.terms
            if result.section and (include_all or include_section):
                yield result.section

    def iter_flags(self, *, include_all=False):
        for result in self.data:
            if include_all or result.exclude_flag == ExcludeFlag.INCLUDE:
                yield result.medical_history_flag
