from pacu.util.spec.float import PositiveFloatSpec
from pacu.core.svc.impl.pacu_attr import PacuAttr
from pacu.core.svc.impl.ember_attr import EmberAttr

class Eyepoint(PacuAttr, PositiveFloatSpec):
    component = 'x-svc-comp-input-text'

class EyepointX(PacuAttr, PositiveFloatSpec):
    description = EmberAttr('description for eyepoint x')
    placeholder = EmberAttr('place for eyepoint x')
    title = EmberAttr('Eyepoint X')
    tooltip = EmberAttr('tooltip for eyepoint x')

class EyepointY(PacuAttr, PositiveFloatSpec):
    description = EmberAttr('description for eyepoint y')
    placeholder = EmberAttr('place for eyepoint y')
    title = EmberAttr('Eyepoint Y')
    tooltip = EmberAttr('tooltip for eyepoint y')
