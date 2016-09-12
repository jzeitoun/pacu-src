__package__ = '' # unicode package name error

import numpy as np

from pacu.core.io.scanbox.method.fit.dogfit import SpatialFrequencyDogFit

def main(workspace, condition, roi, datatag):
    dts = roi.dt_fit_sumof
    sf_rmax_set = [(dt.trial_sf, dt.value['r_max']) for dt in dts]
    fit = SpatialFrequencyDogFit(sf_rmax_set, None, None)
    return fit.toDict()

if __name__ == '__sbx_main__':
    datatag.value = main(workspace, condition, roi, datatag)
# cutoff repvalue on [capture frq
