from medical_history.medical_history import get_medical_history, extract_relatives
from medical_history.flags import MedicalHistoryFlag, ExcludeFlag


def test_separators():
    text = 'Family history of diabetes mellitus (DM) • PCOS'
    results = get_medical_history(text, 'pcos')
    assert len(results) == 1
    assert results[0].exclude_flag == ExcludeFlag.DIFFERENT_SECTION
    assert results[0].medical_history_flag == MedicalHistoryFlag.FAMILY


def test_does_not_match_internal():
    text = 'comparison'  # son should not be found
    assert len(list(extract_relatives(text))) == 0


def test_period_as_immediate_divider():
    text = 'Aunt. Has pcos'
    results = get_medical_history(text, 'pcos')
    assert len(results) == 1
    assert results[0].exclude_flag == ExcludeFlag.DIFFERENT_SENTENCE
    assert results[0].medical_history_flag == MedicalHistoryFlag.DEGREE2


def test_read_about():
    text = 'Aunt read about pcos'
    results = get_medical_history(text, 'pcos')
    assert len(results) == 1
    assert results[0].exclude_flag == ExcludeFlag.NOT_RELEVANT
    assert results[0].medical_history_flag == MedicalHistoryFlag.DEGREE2
