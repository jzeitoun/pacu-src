import numpy as np

from pacu.util.prop.memoized import memoized_property
from pacu.core.io.scanimage.response.orientation import Orientation

class OrientationsResponse(object):
    def toDict(self):
        return self.data
    @classmethod
    def from_adaptor(cls, response, adaptor):
        self = cls()
        self.responses = [
            Orientation.from_adaptor(ori, response.trace, adaptor)
            for ori in adaptor.locator.orientations.loop()
        ]
        return self
    @property
    def names(self):
        return [ori.value for ori in self.responses]
    @memoized_property
    def bss(self):
        return [np.vstack(trace.array for trace in ori.baselines)
            for ori in self.responses]
    @memoized_property
    def ons(self):
        return [np.vstack(trace.array for trace in ori.ontimes)
            for ori in self.responses]
    @property
    def data(self): #TODO use Repetition class
        # bss = [np.vstack(trace.array for trace in ori.baselines)
        #     for ori in self.responses]
        # ons = [np.vstack(trace.array for trace in ori.ontimes)
        #     for ori in self.responses]
        bss_ons = np.array([self.bss, self.ons])
        n_reps, n_frames = bss_ons.shape[2:]
        bss_ons_interleaved = 1, 0, 2, 3
        bss_ons_merged = -1, n_reps, n_frames
        orientation_interleaved = 1, 0, 2
        orientation_merged = n_reps, -1
        traces = (bss_ons
        ).transpose(
            *bss_ons_interleaved
        ).reshape(
            bss_ons_merged
        ).transpose(
            *orientation_interleaved
        ).reshape(
            orientation_merged
        )
        return dict(traces=traces,
            mean=traces.mean(axis=0),
            indices=self.orientation_indices(n_frames))
    def orientation_indices(self, n_frames):
        return {int((index*2 + 1.5)*n_frames): ori.value
            for index, ori in enumerate(self.responses)}
