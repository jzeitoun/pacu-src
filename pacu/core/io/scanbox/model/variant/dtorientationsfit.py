from pacu.core.io.scanbox.model.variant.type import VariantBaseType
from pacu.core.io.scanbox.model.variant.type import Variant

class VTSoGParams(VariantBaseType):
    a1_start = Variant(0)
    a1_stop = Variant(1)
    a2_start = Variant(0)
    a2_stop = Variant(1)
    sigma_start = Variant(15)
    sigma_stop = Variant(60)
    offset_start = Variant(0)
    offset_stop = Variant(0.01)
