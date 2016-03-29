from pacu.core.io.scanimage.response.overview import OverviewResponse
from pacu.core.io.scanimage.response.orientations import OrientationsResponse
from pacu.core.io.scanimage.response.normalfit import NormalfitResponse
from pacu.core.io.scanimage.response.decay import DecayResponse

class BaseResponse(object):
    sfreq = None
    overview = None
    orientations = None
    normalfit = None
    decay = None
    stats = None
    comment = None
    def __init__(self, trace):
        self.trace = trace
    @classmethod
    def from_adaptor(cls, trace, adaptor):
        self = cls(trace)
        self.overview = OverviewResponse.from_adaptor(self, adaptor)
        self.orientations = OrientationsResponse.from_adaptor(self, adaptor)
        self.normalfit = NormalfitResponse.from_adaptor(self, adaptor)
        self.decay = DecayResponse.from_adaptor(self, adaptor)
        self.sfreq = adaptor.locator.sfrequencies.current
        return self
    def toDict(self):
        return dict(
            overview = self.overview,
            orientations = self.orientations,
            fit = self.normalfit,
            decay = self.decay,
            stats = self.stats
        )

    # <p>OSI: {{model.response.stats.osi}}</p>
    # <p>DSI: {{model.response.stats.dsi}}</p>
    # <p>Sigma: {{model.response.stats.sigma}}</p>
    # <p>OPref: {{model.response.stats.o_pref}}</p>
    # <p>RMax: {{model.response.stats.r_max}}</p>
    # <p>Residual: {{model.response.stats.residual}}</p>
    # <p>CV: {{model.response.stats.cv}}</p>
