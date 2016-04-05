from scipy import stats

from pacu.core.io.scanimage import util
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
    blank = None
    flicker = None
    anova = None
    def __init__(self, trace):
        self.trace = trace
    @classmethod
    def from_adaptor(cls, roi, trace, adaptor):
        self = cls(trace)
        self.blank = roi.blank
        self.flicker = roi.flicker
        self.sfreq = adaptor.locator.sfrequencies.current
        self.overview = OverviewResponse.from_adaptor(self, adaptor)
        self.orientations = OrientationsResponse.from_adaptor(self, adaptor)
        return self
    def toDict(self):
        return dict(
            sfreq = self.sfreq,
            overview = self.overview,
            orientations = self.orientations,
            fit = self.normalfit,
            decay = self.decay,
            stats = self.stats)
    def update_fit_and_decay(self, roi, adaptor):
        self.normalfit = NormalfitResponse.from_adaptor(
            self, adaptor, roi.best_o_pref)
        self.decay = DecayResponse.from_adaptor(self, adaptor)
