import pytest

from medical_history.medical_history import MedicalHistoryFlag, get_medical_history


@pytest.mark.parametrize(('text', 'exp_flag'), [
    ('pcos dx 2012', MedicalHistoryFlag.PERSONAL,),
    ('dx of pcos 2012', MedicalHistoryFlag.PERSONAL,),
    ('dx pcos 2012', MedicalHistoryFlag.PERSONAL,),
    ('pcos dx at 22', MedicalHistoryFlag.PERSONAL,),
    ('pcos dx at age 22', MedicalHistoryFlag.PERSONAL,),
    ('pcos dx at age 22yo', MedicalHistoryFlag.PERSONAL,),
    ('pcos dxd 2012', MedicalHistoryFlag.PERSONAL,),
    ('pcos dx\'d around 2012-13', MedicalHistoryFlag.PERSONAL,),
    ('prior pcos dx', MedicalHistoryFlag.PERSONAL,),
    ('past dx of pcos', MedicalHistoryFlag.PERSONAL,),
    ('possible pcos dx', MedicalHistoryFlag.PERSONAL_MAYBE,),
])
def test_past_dx_of(text, exp_flag):
    flags, data = get_medical_history(text, 'pcos')
    assert flags[0] == exp_flag
