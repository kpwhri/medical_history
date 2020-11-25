import pytest

from medical_history.medical_history import get_medical_history
from medical_history.flags import MedicalHistoryFlag


@pytest.mark.parametrize(('text', 'exp_data'), [
    ('No past medical history on file', ()),
    ('', ()),
])
def test_no_medical_history(text, exp_data):
    results = get_medical_history(text, 'pcos', 'polycystic')
    assert len(results) == 1
    assert results[0].medical_history_flag == MedicalHistoryFlag.UNKNOWN
    assert len(results.iter_terms()) == 0
