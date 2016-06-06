from pacu.util.spec.float import PositiveFloatSpec
from pacu.core.svc.impl.pacu_attr import PacuAttr
from pacu.core.svc.impl.ember_attr import EmberAttr

class SFrequency(PacuAttr, PositiveFloatSpec):
    component = 'x-svc-comp-input-array'
    description = EmberAttr('description for sfreq')
    placeholder = EmberAttr('place for sfreq')
    title = EmberAttr('Spatial Frequency')
