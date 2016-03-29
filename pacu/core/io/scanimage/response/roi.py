import numpy as np

from pacu.core.io.scanimage.response.base import BaseResponse

class ROIResponse(BaseResponse):
    cv = None
    @property
    def stats(self):
        g = self.normalfit.gaussian
        return dict(
            osi = g.osi,
            dsi = g.dsi,
            sigma = g.sigma,
            o_pref = g.o_pref,
            r_max = g.r_max,
            residual = g.residual,
            cv = self.cv)
    @property
    def cv(self):
        angles = self.orientations.names
        sqrt, sin, cos, sum = np.sqrt, np.sin, np.cos, np.sum
        two_thetas = 2*(np.array(angles)/360)*2*np.pi
        r_thetas = self.normalfit.measure
        return sqrt(
            sum((r_thetas * sin(two_thetas)))**2 +
            sum((r_thetas * cos(two_thetas)))**2
        ) / sum(r_thetas)

# stats['blank_m'] = self.response.blank.meantrace.mean() if self.response.blank else None
# stats['fff_m'] = self.response.flicker.meantrace.mean() if self.response.flicker else None
# stats['tau'] = self.tiffFig.responseFig.tau
