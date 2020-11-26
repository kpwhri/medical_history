import pytest

from medical_history.medical_history import get_medical_history
from medical_history.flags import MedicalHistoryFlag


@pytest.mark.parametrize(('text', 'exp_flag', 'exp_data'), [
    ('medical history of fertility problem secondary to PCOS',
     MedicalHistoryFlag.PERSONAL,
     {'pcos', 'medical history'},
     ),
    ('there is not a history of PCOS',
     MedicalHistoryFlag.NEGATED,
     {'pcos', 'history of', 'not'},
     ),
    ('has hx of polycystic ovarian synd',
     MedicalHistoryFlag.PERSONAL,
     {'polycystic ovarian', 'hx of'},
     ),
    ('History : PCOS',
     MedicalHistoryFlag.PERSONAL,
     {'pcos', 'history'},
     ),
    ('No Medical History of PCOS',
     MedicalHistoryFlag.NEGATED,
     {'pcos', 'no medical history'},
     ),
    ('HISTORY: irregular periods/h/o PCOS',
     MedicalHistoryFlag.PERSONAL,
     {'pcos', 'history', 'pcos', 'h/o'}
     ),
    ('HISTORY: AMENORRHEA, PCOS:: amenorrhea, PCOS',
     MedicalHistoryFlag.PERSONAL,
     {'pcos', 'history'}
     ),
    ('HX POLYCYSTIC OVARIES',
     MedicalHistoryFlag.PERSONAL,
     {'polycystic ovaries', 'hx'}
     ),
    ('HISTORY: E28.2-Polycystic ovarian',
     MedicalHistoryFlag.PERSONAL,
     {'polycystic ovarian', 'history'}
     ),
])
def test_medical_history(text, exp_flag, exp_data):
    results = get_medical_history(text, 'pcos', r'polycystic ovar\w+')
    assert set(results.iter_flags()) == {exp_flag}
    assert set(results.iter_terms()) == exp_data


@pytest.mark.parametrize(('text', 'exp_flag', 'exp_data'), [
    ('HISTORY: E28.2-Polycystic ovarian',
     MedicalHistoryFlag.PERSONAL,
     {'e28.2', 'history', 'polycystic ovarian', 'history'}
     ),
])
def test_medical_history_dx_code(text, exp_flag, exp_data):
    results = get_medical_history(text, 'pcos', r'polycystic ovar\w+', 'e28.2')
    assert set(results.iter_flags()) == {exp_flag}
    assert set(results.iter_terms()) == exp_data
