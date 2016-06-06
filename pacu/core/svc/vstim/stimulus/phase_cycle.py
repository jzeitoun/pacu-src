from pacu.util.spec.int import PositiveIntSpec
from pacu.core.svc.impl.pacu_attr import PacuAttr
from pacu.core.svc.impl.ember_attr import EmberAttr

class PhaseCycle(PacuAttr, PositiveIntSpec):
    component = 'x-svc-comp-input-text'
    description = EmberAttr('number')
    placeholder = EmberAttr('Gratings movement')
    title = EmberAttr('Phase Cycle')
    tooltip = EmberAttr('Higher is slower.')
