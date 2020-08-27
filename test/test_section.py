from medical_history.medical_history import get_medical_history, MedicalHistoryFlag


def test_family_history_section():
    text = 'Review of patient\'s family history indicates: PCOS daughter'
    results, data = get_medical_history(text, 'pcos')
    assert set(results) == {MedicalHistoryFlag.FAMILY, MedicalHistoryFlag.DEGREE1}
    assert set(data) == {'pcos', 'family history indicates:', 'daughter'}


def test_family_history_section_difficult():
    text = 'Review of patient\'s family history indicates:\n asthma daughter\n pcos aunt'
    results, data = get_medical_history(text, 'pcos')
    assert set(results) == {MedicalHistoryFlag.FAMILY, MedicalHistoryFlag.DEGREE2}
    assert set(data) == {'pcos', 'family history indicates:', 'aunt'}


def test_personal_history_section_intervening_section():
    text = 'Past Medical History: ADHD Comment: medication asthma Comment: 1980 Current prescriptions: ... pcos'
    results, data = get_medical_history(text, 'pcos')
    assert set(results) == {MedicalHistoryFlag.UNKNOWN}
    assert set(data) == set()


def test_personal_history_section():
    text = 'Past Medical History: ADHD Comment: medication PCOS Comment: 1980'
    results, data = get_medical_history(text, 'pcos')
    assert results == (MedicalHistoryFlag.PERSONAL,)
    assert data == ('pcos', 'past medical history:')