
from medical_history.medical_history import get_medical_history, MedicalHistoryFlag


def test_separators():
    text = 'Family history of diabetes mellitus (DM) • PCOS'
    flags, data = get_medical_history(text, 'pcos')
    assert len(flags) == 1
    assert flags[0] == MedicalHistoryFlag.UNKNOWN
    assert len(data) == 0
