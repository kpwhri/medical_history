from medical_history.flags import MedicalHistoryFlag

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
