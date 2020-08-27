import pytest

from medical_history.medical_history import get_medical_history, MedicalHistoryFlag


@pytest.mark.parametrize(('text', 'exp_flag', 'exp_data'), [
    ('medical history of fertility problem secondary to PCOS',
     MedicalHistoryFlag.PERSONAL,
     ('pcos', 'medical history'),
     ),
    ('there is not a history of PCOS',
     MedicalHistoryFlag.NEGATED,
     ('pcos', 'history of', 'not'),
     ),
    ('has hx of polycystic ovarian synd',
     MedicalHistoryFlag.PERSONAL,
     ('polycystic ovarian', 'hx of'),
     ),
    ('History : PCOS',
     MedicalHistoryFlag.PERSONAL,
     ('pcos', 'history'),
     ),
    ('No Medical History of PCOS',
     MedicalHistoryFlag.NEGATED,
     ('pcos', 'no medical history'),
     ),
])
def test_medical_history(text, exp_flag, exp_data):
    flags, data = get_medical_history(text, 'pcos', 'polycystic ovarian')
    assert len(flags) == 1
    assert flags[0] == exp_flag
    assert data == exp_data
