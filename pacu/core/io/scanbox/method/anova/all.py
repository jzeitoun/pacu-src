__package__ = '' # unicode package name error

import numpy as np
from scipy import stats

from pacu.core.io.scanimage import util

def main(workspace, condition, roi, datatag, dff0s=None):
    n_panes = condition.info.get('focal_pane_args', {}).get('n', 1)
    pane_offset = workspace.cur_pane or 0

    if not dff0s:
        dff0s = roi.dttrialdff0s

    bls = dff0s.filter_by(trial_blank=True)
    fls = dff0s.filter_by(trial_flicker=True)
    flicker = [np.nanmean(np.array(f.value['on'][pane_offset::n_panes])) for f in fls]
    blank = [np.nanmean(np.array(b.value['on'][pane_offset::n_panes])) for b in bls]
    all_oris = [
        [np.nanmean(np.array(rep.value['on'][pane_offset::n_panes])) for rep in reps]
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

if __name__ == '__sbx_stitch__':
    datatag.value = main(workspace, condition, roi, datatag, dff0s)
