from pacu.core.andor.feature.base import BaseFeature, AbstractMeta

class EnumMeta(AbstractMeta):
    @property
    def range(self):
        return self.enums

class EnumFeature(BaseFeature):
    Meta = EnumMeta
    def __get__(self, inst, type):
        return inst.handle.get_enumstr(self.feature) if inst else self
    def __set__(self, inst, val):
        inst.handle.enum(self.feature, val)
