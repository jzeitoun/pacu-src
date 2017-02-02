from pacu.core.io.scanbox.model.variant.type import VariantBaseType
from pacu.core.io.scanbox.model.variant.type import Variant

class VTSoGParams(VariantBaseType):
    # default values
    a1_min = Variant(0)
    a1_max = Variant(1)
    a2_min = Variant(0)
    a2_max = Variant(1)
    sigma_min = Variant(15)
    sigma_max = Variant(60)
    offset_min = Variant(0)
    offset_max = Variant(0.01)