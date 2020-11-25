import pytest

from medical_history.medical_history import get_medical_history
from medical_history.flags import MedicalHistoryFlag


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
    ('possible pcos dx', MedicalHistoryFlag.PERSONAL_CURRENT_MAYBE,),
    ('possible pcos dx in 2012', MedicalHistoryFlag.PERSONAL_MAYBE,),
    ('possible prior pcos dx', MedicalHistoryFlag.PERSONAL_MAYBE,),
    ('possible previous pcos dx', MedicalHistoryFlag.PERSONAL_MAYBE,),
    ('no previous pcos dx', MedicalHistoryFlag.NEGATED,),
])
def test_past_dx_of(text, exp_flag):
    results = get_medical_history(text, 'pcos')
    assert set(results.iter_flags()) == {exp_flag}
