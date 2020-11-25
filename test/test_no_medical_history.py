import pytest

from medical_history.medical_history import get_medical_history, MedicalHistoryFlag


@pytest.mark.parametrize(('text', 'exp_data'), [
    ('No past medical history on file', ()),
    ('', ()),
])
def test_no_medical_history(text, exp_data):
    flags, data = get_medical_history(text, 'pcos', 'polycystic')
    assert len(flags) == 1
    assert flags[0] == MedicalHistoryFlag.UNKNOWN
    assert data == exp_data

