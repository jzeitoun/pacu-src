__package__ = '' # unicode package name error

import numpy as np
from scipy import stats

from pacu.core.io.scanimage import util

def main(workspace, condition, roi, datatag):
    bls = roi.dttrialdff0s.filter_by(trial_blank=True)
    fls = roi.dttrialdff0s.filter_by(trial_flicker=True)
    flicker = [np.nanmean(np.array(f.value['on'])) for f in fls]
    blank = [np.nanmean(np.array(b.value['on'])) for b in bls]
    all_oris = [
        [np.nanmean(np.array(rep.value['on'])) for rep in reps]
        for sf, oris in roi.dt_ori_by_sf(datatag.trial_contrast).items()
        for ori, reps in oris.items()
    ]
    matrix = np.array([blank, flicker] + all_oris).T
    flicker_non_nans = list(filter(np.isfinite, flicker))
    blank_non_nans = list(filter(np.isfinite, blank))
    all_oris_non_nans = [list(filter(np.isfinite, trial)) for trial in all_oris]
    f, p = stats.f_oneway(flicker_non_nans, blank_non_nans, *all_oris_non_nans)
    return util.nan_for_json(dict(f=f, p=p, matrix=matrix.tolist()))

if __name__ == '__sbx_main__':
    datatag.value = main(workspace, condition, roi, datatag)

