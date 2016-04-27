import numpy as np
from scipy import stats

from pacu.core.io.scanimage.response.base import BaseResponse
from pacu.core.io.scanimage import util

class ROIResponse(BaseResponse):
    cv = None
    @property
    def stats(self):
        if not self.normalfit:
            return {}
        g = self.normalfit.gaussian
        return util.nan_for_json(dict(
            tau = self.decay.tau,
            osi = g.osi,
            dsi = g.dsi,
            sigma = g.sigma,
            o_pref = g.o_pref,
            r_max = g.r_max,
            residual = g.residual,
            anova = self.anova,
            cv = self.cv))
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

    @property
    def anova(self):
        try:
            oris = [
                [ont.array.mean() for ont in ori.ontimes]
                for ori in self.orientations.responses]
            if self.flicker and self.blank:
                f_reps = [ont.array.mean() for ont in self.flicker.ontimes]
                b_reps = [ont.array.mean() for ont in self.blank.ontimes]
                f, p = stats.f_oneway(b_reps, f_reps, *oris)
                return dict(f=f, p=p)
        except Exception as e:
            return {}
