from pacu.util.spec.float import PositiveFloatSpec
from pacu.core.svc.impl.pacu_attr import PacuAttr
from pacu.core.svc.impl.ember_attr import EmberAttr

class SNPBandwidth(PacuAttr, PositiveFloatSpec):
    component = 'x-svc-comp-input-text'
    description = EmberAttr('used to get sigma of Gaussian mask')
    placeholder = EmberAttr('')
    title = EmberAttr('Bandwidth')
    tip = EmberAttr('')
