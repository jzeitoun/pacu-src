__package__ = '' # unicode package name error

import numpy as np
from scipy import stats

from pacu.core.io.scanimage import util

def main(workspace, condition, roi, datatag):
    bls = roi.datatags.filter_by(method='dff0', trial_blank=True)
    fls = roi.datatags.filter_by(method='dff0', trial_flicker=True)
    flicker = [np.array(f.value['on']).mean() for f in fls]
    blank = [np.array(b.value['on']).mean() for b in bls]
    all_oris = [
        [np.array(rep.value['on']).mean() for rep in reps]
        for sf, oris in roi.dt_ori_by_sf.items()
        for ori, reps in oris.items()
    ]
    matrix = np.array([blank, flicker] + all_oris).T
    f, p = stats.f_oneway(flicker, blank, *all_oris)
    return util.nan_for_json(dict(f=f, p=p, matrix=matrix))

if __name__ == '__sbx_main__':
    datatag.value = main(workspace, condition, roi, datatag)

