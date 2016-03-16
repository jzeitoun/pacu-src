from pacu.core.io.scanimage.response.overview import OverviewResponse
from pacu.core.io.scanimage.response.orientations import OrientationsResponse
from pacu.core.io.scanimage.response.normalfit import NormalfitResponse
from pacu.core.io.scanimage.response.decay import DecayResponse

class BaseResponse(object):
    overview = None
    orientations = None
    normalfit = None
    decay = None
    def __init__(self, trace):
        self.trace = trace
    @classmethod
    def from_adaptor(cls, trace, adaptor):
        self = cls(trace)
        self.overview = OverviewResponse.from_adaptor(self, adaptor)
        self.orientations = OrientationsResponse.from_adaptor(self, adaptor)
        self.normalfit = NormalfitResponse.from_adaptor(self, adaptor)
        self.decay = DecayResponse.from_adaptor(self, adaptor)
        return self
    def toDict(self):
        return dict(
            overview = self.overview,
            orientations = self.orientations,
            fit = self.normalfit,
            decay = self.decay
        )
