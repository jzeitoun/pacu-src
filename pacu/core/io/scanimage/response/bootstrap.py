from __future__ import division
from __future__ import absolute_import

import sys

import numpy as np
import scikits.bootstrap as bootstrap

from pacu.util.prop.memoized import memoized_property
from pacu.core.io.scanimage.fit.gasussian.sumof import SumOfGaussianFit
from pacu.core.io.scanimage import util

bound_dtype = [('val', float), ('ori', float)]

class BootFit(object):
    def __init__(self):
        self.rvs = []
    def stat(self, data):
        vals = data['val']
        x_oris = data['ori'][0, :]
        y_meas = vals.mean(0)
        fit = SumOfGaussianFit(x_oris, y_meas)
        osi = fit.osi
        self.rvs.append(osi)
        print '.',
        return osi

class BootstrapResponse(object):
    n_samples = 500
    mean = None
    std = None
    interval = None
    def toDict(self):
        return util.nan_for_json(dict(
            mean=self.mean,
            std=self.std
        ))
    @classmethod
    def from_adaptor(cls, response, adaptor):
        self = cls()
        msg = ('Creating bootstrap response {} for {} samples. '
               'It may take few minutes.').format(response.sfreq, self.n_samples)
        print msg
        oris = response.orientations.names
        resps = response.orientations.windowed_ontimes
        bound = [
            [(value, ori) for value in values]
            for values, ori in zip(resps, oris)]
        bound_response = np.array(bound, dtype=bound_dtype).T
        bf = BootFit()
        try:
            self.interval = bootstrap.ci(
                data = bound_response,
                statfunction = bf.stat,
                n_samples = self.n_samples
            )
            stats = bf.rvs[:self.n_samples]
            self.mean, self.std = np.nanmean(stats), np.nanstd(stats)
        except Exception as e:
            sys.stderr.write(str(e))
            sys.stderr.flush()
        # print 'INTERVAL:{s.interval}, MEAN: {s.mean}, STD: {s.std}'.format(s=self)
        return self
