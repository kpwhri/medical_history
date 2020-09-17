import pytest

from medical_history.medical_history import get_medical_history, MedicalHistoryFlag


@pytest.mark.parametrize(('text', 'exp_flags', 'exp_data'), [
    ('family history includes PCOS in her mother',
     (MedicalHistoryFlag.DEGREE1, MedicalHistoryFlag.FAMILY),
     ('pcos', 'mother', 'family history'),
     ),
    ('father does not have pcos (obviously)',
     (MedicalHistoryFlag.DEGREE1_NEG,),
     ('pcos', 'father', 'not'),
     ),
    ('PCOS Sister',
     (MedicalHistoryFlag.DEGREE1,),
     ('pcos', 'sister'),
     ),
    ('states no family history of PCOS',
     (MedicalHistoryFlag.FAMILY_NEG,),
     ('pcos', 'no family history'),
     ),
    ('patient\'s aunt does have history of polycystic ovaries',
     (MedicalHistoryFlag.DEGREE2,),
     ('polycystic ovaries', 'aunt'),
     ),
    ('No FH of PCOS',
     (MedicalHistoryFlag.FAMILY_NEG,),
     ('no fh', 'pcos'),
     ),
    ('Family History : History of poly cystic ovarian',
     (MedicalHistoryFlag.FAMILY,),
     ('poly cystic ovarian', 'family history :', 'family history'),
     ),
    ('Mother with history of PCOS',
     (MedicalHistoryFlag.DEGREE1,),
     ('mother', 'pcos'),
     ),
])
def test_family_history(text, exp_flags, exp_data):
    flags, data = get_medical_history(text, 'pcos', r'poly\s*cystic ovar\w+')
    assert set(flags) == set(exp_flags)
    assert set(data) == set(exp_data)
