from medical_history.medical_history import get_medical_history, MedicalHistoryFlag, extract_relatives


def test_separators():
    text = 'Family history of diabetes mellitus (DM) • PCOS'
    flags, data = get_medical_history(text, 'pcos')
    assert len(flags) == 1
    assert flags[0] == MedicalHistoryFlag.UNKNOWN
    assert len(data) == 0


def test_does_not_match_internal():
    text = 'comparison'  # son should not be found
    assert len(list(extract_relatives(text))) == 0


def test_period_as_immediate_divider():
    text = 'Aunt. Has pcos'
    flags, data = get_medical_history(text, 'pcos')
    assert len(flags) == 1
    assert flags[0] == MedicalHistoryFlag.UNKNOWN
    assert len(data) == 0
