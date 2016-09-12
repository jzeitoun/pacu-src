from pacu.util.spec.str import StringSpec
from pacu.core.svc.impl.pacu_attr import PacuAttr
from pacu.core.svc.impl.ember_attr import EmberAttr

class Keyword(PacuAttr, StringSpec):
    component = 'x-svc-comp-input-text'
    description = EmberAttr('filename')
    placeholder = EmberAttr('Recording information')
    title = EmberAttr('Scanbox Filename')
    tooltip = EmberAttr('For current version, this is only way to '
            'find an actual recording from a stimulus condition data. '
            'So please note recording information so that you can '
            'pick up your recording before having analysis session. '
            'Highly recommended to use descriptive and unique name. ')
