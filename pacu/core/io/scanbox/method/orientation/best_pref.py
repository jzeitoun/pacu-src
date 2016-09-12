__package__ = '' # unicode package name error

import cv2
import numpy as np

from pacu.core.io.scanbox.method.fit.sogfit import SumOfGaussianFit

def main(workspace, condition, roi, datatag):
    sfs = []
    oris = []
    trials = roi.datatags.find_by('method', 'dff0')
    for sf in condition.sfrequencies:
        sf_trials = trials.find_by('trial_sf', sf)
        for ori in condition.orientations:
            reps_by_ori = sf_trials.find_by('trial_ori', ori)
            arr = np.array([rep.value['on'] for rep in reps_by_ori])
            meantrace_for_ori = arr.mean(0)
            oris.append(meantrace_for_ori)
        sfs.append(np.array(oris))
    mat = np.array(sfs).mean(axis=(0,2))
    fit = SumOfGaussianFit(condition.orientations, mat)
    return fit.o_pref

if __name__ == '__sbx_main__':
    datatag.value = main(workspace, condition, roi, datatag)
# cfreq = adaptor.capture_frequency
# return np.array([
#     resp.orientations.ons[...,
#     int(1*cfreq):int(2*cfreq)
# ].mean(axis=(1, 2)) for sf, resp in self.sorted_responses]).mean(axis=0)
