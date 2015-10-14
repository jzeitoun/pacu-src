from pacu.util.spec.str import StringSpec
from pacu.core.svc.impl.pacu_attr import PacuAttr
from pacu.core.svc.impl.ember_attr import EmberAttr

class ExpNote(PacuAttr, StringSpec):
    component = 'x-svc-comp-input-text'
    description = EmberAttr('description for note')
    placeholder = EmberAttr('place for note')
    title = EmberAttr('Experiment Note')
    tooltip = EmberAttr('tooltip for note')
