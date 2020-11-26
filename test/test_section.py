from medical_history.medical_history import get_medical_history
from medical_history.flags import MedicalHistoryFlag


def test_family_history_section():
    text = 'Review of patient\'s family history indicates: PCOS daughter'
    results = get_medical_history(text, 'pcos')
    assert set(results.iter_flags()) == {MedicalHistoryFlag.FAMILY, MedicalHistoryFlag.DEGREE1}
    assert set(results.iter_terms(include_all=True)) == {'pcos', 'family history', 'daughter'}


def test_family_history_section_difficult():
    text = 'Review of patient\'s family history indicates:\n asthma daughter\n pcos aunt'
    results = get_medical_history(text, 'pcos')
    assert set(results.iter_flags()) == {MedicalHistoryFlag.FAMILY, MedicalHistoryFlag.DEGREE2}
    assert set(results.iter_terms()) == {'pcos', 'aunt'}


def test_personal_history_section_intervening_section():
    text = 'Past Medical History: ADHD Comment: medication asthma Comment: 1980 Current prescriptions: ... pcos'
    results = get_medical_history(text, 'pcos')
    assert set(results.iter_flags()) == {MedicalHistoryFlag.UNKNOWN}
    assert set(results.iter_terms()) == set()


def test_personal_history_section():
    text = 'Past Medical History: ADHD Comment: medication PCOS Comment: 1980'
    results = get_medical_history(text, 'pcos')
    assert set(results.iter_flags()) == {MedicalHistoryFlag.PERSONAL}
    assert set(results.iter_terms()) == {'pcos', 'past medical history:'}


def test_ignore_assessment():
    text = 'Assessment: family history of pcos'
    results = get_medical_history(text, 'pcos')
    assert set(results.iter_flags()) == {MedicalHistoryFlag.UNKNOWN}
    assert set(results.iter_terms()) == {}


def test_ignore_problem_list():
    text = 'Problem List: PCOS Mother of same blood type'
    results = get_medical_history(text, 'pcos')
    assert set(results.iter_flags()) == {MedicalHistoryFlag.UNKNOWN}
    assert set(results.iter_terms()) == {}
