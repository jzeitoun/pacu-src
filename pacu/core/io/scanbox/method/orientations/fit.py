__package__ = '' # unicode package name error

import numpy as np

from pacu.core.io.scanimage import util
from pacu.core.io.scanbox.method.fit.sogfit import SumOfGaussianFit
#
# SORT SORT SORT SORT SORT SORT SORT SORT SORT SORT SORT SORT SORT
# DID YOU SORT DATTAG?
def main(workspace, condition, roi, datatag):
    trials = roi.dttrialdff0s.filter_by(
        trial_sf=datatag.trial_sf,
        trial_blank=False,
        trial_flicker=False,
    )
    best_pref_ori = roi.dtorientationbestpref.value
    oris = []
    for ori in condition.orientations:
        reps_by_ori = trials.filter_by(trial_ori=ori)
        arr = np.array([rep.value['on'] for rep in reps_by_ori])
        meantrace_for_ori = arr.mean(0)
        oris.append(meantrace_for_ori)
    mat = np.array(oris).mean(1)
    fit = SumOfGaussianFit(condition.orientations, mat, best_pref_ori)
    return util.nan_for_json(dict(
        orientations = condition.orientations,
        osi = fit.osi,
        dsi = fit.dsi,
        sigma = fit.sigma,
        o_pref = fit.o_pref,
        r_max = fit.r_max,
        residual = fit.residual,
        x = fit.stretched.x.tolist(),
        y_meas = fit.stretched.y.tolist(),
        y_fit = fit.y_fit.tolist()))

if __name__ == '__sbx_main__':
    datatag.value = main(workspace, condition, roi, datatag)
