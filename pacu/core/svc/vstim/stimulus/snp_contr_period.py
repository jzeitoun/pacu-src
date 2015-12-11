from pacu.util.spec.float import PositiveFloatSpec
from pacu.core.svc.impl.pacu_attr import PacuAttr
from pacu.core.svc.impl.ember_attr import EmberAttr

class SNPContrPeriod(PacuAttr, PositiveFloatSpec):
    component = 'x-svc-comp-input-text'
    description = EmberAttr('sigma')
    placeholder = EmberAttr('')
    title = EmberAttr('Contr Period')
    tip = EmberAttr('')
