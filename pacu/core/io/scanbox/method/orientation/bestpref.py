__package__ = '' # unicode package name error

import numpy as np

from pacu.core.io.scanbox.method.fit.sogfit import SumOfGaussianFit

def main(workspace, condition, roi, datatag):
    cfreq = workspace.condition.info['framerate']
    sfs = []
    trials = roi.dttrialdff0s.filter_by(trial_blank=False, trial_flicker=False)
    for sf in condition.sfrequencies:
        sf_trials = trials.filter_by(trial_sf=sf,
            trial_contrast=datatag.trial_contrast)
        oris = []
        for ori in condition.orientations:
            reps_by_ori = sf_trials.filter_by(trial_ori=ori)
            arr = np.array([
                rep.value['on'][int(1*cfreq):int(2*cfreq)]
            for rep in reps_by_ori])
            meantrace_for_ori = np.nanmean(arr, axis=0)
            oris.append(meantrace_for_ori)
        sfs.append(np.array(oris))
    mat = np.nanmean(np.array(sfs), axis=(0,2))
    fit = SumOfGaussianFit(condition.orientations, mat)
    return fit.o_pref

if __name__ == '__sbx_main__':
    datatag.value = main(workspace, condition, roi, datatag)
# cfreq = adaptor.capture_frequency
# return np.array([
#     resp.orientations.ons[...,
#     int(1*cfreq):int(2*cfreq)
# ].mean(axis=(1, 2)) for sf, resp in self.sorted_responses]).mean(axis=0)
