from pacu.util.spec.float import PositiveFloatSpec
from pacu.core.svc.impl.pacu_attr import PacuAttr
from pacu.core.svc.impl.ember_attr import EmberAttr

class Contrast(PacuAttr, PositiveFloatSpec):
    component = 'x-svc-comp-input-text'
    description = EmberAttr('description for contrast')
    placeholder = EmberAttr('place for contrast')
    title = EmberAttr('Contrast')
    tip = EmberAttr('tooltip for contrast')
