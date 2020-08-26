import pytest

from medical_history.medical_history import get_medical_history, MedicalHistoryFlag


@pytest.mark.parametrize('text', [
    'No past medical history on file',
])
def test_no_medical_history(text):
    flag, data = get_medical_history(text, 'pcos', 'polycystic')
    assert flag == MedicalHistoryFlag.NEGATED
    assert data == 'no past medical history'
