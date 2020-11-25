from enum import Enum


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
    NONE = 11
    PERSONAL_MAYBE = 12
    PERSONAL_CURRENT = 13
    PERSONAL_CURRENT_MAYBE = 14


class ExcludeFlag(Enum):
    INCLUDE = 0
    EXCLUDE = 1
    NOT_RELEVANT = 2
    DIFFERENT_SECTION = 3
    DIFFERENT_SENTENCE = 4
    CLOSER_MENTION = 5
