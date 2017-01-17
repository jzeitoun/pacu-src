__package__ = '' # unicode package name error

import numpy as np

from pacu.core.io.scanbox.method.fit.dogfit import SpatialFrequencyDogFit
# did you sort datatag?
def main(workspace, condition, roi, datatag):
    dts = roi.dtorientationsfits.filter_by(trial_contrast=datatag.trial_contrast)
    bls = roi.dttrialdff0s.filter_by(trial_blank=True)
    fls = roi.dttrialdff0s.filter_by(trial_flicker=True)
    sf_rmax_set = [(dt.trial_sf, dt.value['r_max']) for dt in dts]
    blank = np.nanmean(np.array([[bl.value['on']] for bl in bls]), axis=0).mean()
    flicker = np.nanmean(np.array([[fl.value['on']] for fl in bls]), axis=0).mean()
    fit = SpatialFrequencyDogFit(sf_rmax_set, flicker, blank)
    return fit.toDict()

if __name__ == '__sbx_main__':
    datatag.value = main(workspace, condition, roi, datatag)
# cutoff repvalue on [capture frq
