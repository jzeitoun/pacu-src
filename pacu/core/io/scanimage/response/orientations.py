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
            for ori in adaptor.locator.orientations.loop()]
        return self
    @property
    def names(self):
        return [ori.value for ori in self.responses]
    @memoized_property
    def bss(self):
        return np.array([np.vstack(
            trace.array for trace in ori.baselines
        ) for ori in self.responses])
    @memoized_property
    def ons(self):
        return np.array([np.vstack(
            trace.array for trace in ori.ontimes
        ) for ori in self.responses])
    # @property
    # def data(self): #TODO use Repetition class
    #     bss_ons = np.array([self.bss, self.ons])
    #     n_reps, n_frames = bss_ons.shape[2:]
    #     bss_ons_interleaved = 1, 0, 2, 3
    #     bss_ons_merged = -1, n_reps, n_frames
    #     orientation_interleaved = 1, 0, 2
    #     orientation_merged = n_reps, -1
    #     traces = (bss_ons
    #     ).transpose(
    #         *bss_ons_interleaved
    #     ).reshape(
    #         bss_ons_merged
    #     ).transpose(
    #         *orientation_interleaved
    #     ).reshape(
    #         orientation_merged
    #     )
    #     return dict(traces=traces,
    #         mean=traces.mean(axis=0),
    #         indices=self.orientation_indices(n_frames))
    @property
    def data(self):
        bss_ons = np.concatenate([
            self.bss, self.ons
        ], axis=2).transpose(1, 0, 2) #.reshape((8, 360))
        n_rep, n_ori, n_frm = bss_ons.shape
        traces = bss_ons.reshape((n_rep, n_ori*n_frm))
        return dict(traces=traces,
            mean=traces.mean(axis=0),
            indices=self.orientation_indices(n_frm/2))
    def orientation_indices(self, n_frames):
        return {int((index*2 + 1.5)*n_frames): ori.value
            for index, ori in enumerate(self.responses)}

# test
# np.concatenate([np.array(range(-3*2*5,0)[::-1]).reshape((3,2,5)), np.array(range(1, 3*2*4+1)).reshape((3,2,4))], axis=2)

# traces = np.concatenate([
#     np.array(range(-3*2*5,0)[::-1]).reshape((3,2,5)),
#     np.array(range(1, 3*2*4+1)).reshape((3,2,4))
# ], axis=2).transpose(1, 0, 2).reshape((2, 27))

