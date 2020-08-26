import pytest

from medical_history.medical_history import get_medical_history, MedicalHistoryFlag


@pytest.mark.parametrize('text', [
    'medical history of fertility problem secondary to PCOS',
])
def test_medical_history(text):
    flags, data = get_medical_history(text, 'pcos', 'polycystic ovarian')
    assert len(flags) == 1
    assert flags[0] == MedicalHistoryFlag.PERSONAL
    assert data == ('pcos', 'medical history')
