__package__ = '' # unicode package name error

import numpy as np
from scipy import stats

from pacu.core.io.scanimage import util

def main(workspace, condition, roi, datatag):
    oris = roi.dttrialdff0s.filter_by(trial_sf=datatag.trial_sf)
    oris = [
        [np.array(rep.value['on']).mean()
        for rep in oris.filter_by(trial_ori=ori)]
    for ori in condition.orientations]
    bls = roi.dttrialdff0s.filter_by(trial_blank=True)
    fls = roi.dttrialdff0s.filter_by(trial_flicker=True)
    flicker = [np.array(f.value['on']).mean() for f in fls]
    blank = [np.array(b.value['on']).mean() for b in bls]
    try:
        return stats.f_oneway(blank, flicker, *oris)
    except Exception as e:
        print 'Error on making Anova Each', str(e)
        return None, None

if __name__ == '__sbx_main__':
    f, p = main(workspace, condition, roi, datatag)
    datatag.f = 'nan' if np.isnan(f) else f
    datatag.p = 'nan' if np.isnan(p) else p
