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
])
def test_family_history(text, exp_flags, exp_data):
    flags, data = get_medical_history(text, 'pcos', 'polycystic ovarian')
    assert len(flags) == len(exp_flags)
    assert set(flags) == set(exp_flags)
    assert set(data) == set(exp_data)
