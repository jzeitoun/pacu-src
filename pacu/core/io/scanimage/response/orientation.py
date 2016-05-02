import numpy as np

from pacu.core.io.scanimage.trace.whole import WholeTrace

class Orientation(object):
    capture_frequency = 6.1 # default
    def __init__(self, value, ontimes, offtimes, baselines):
        self.value = value
        self.ontimes = ontimes
        self.offtimes = offtimes
        self.baselines = baselines
    @classmethod
    def from_adaptor(cls, value, trace, adt):
        trace = WholeTrace(trace.copy())
        ontimes = trace.zip_slice(adt.indice.ontimes)
        baselines = trace.zip_slice(adt.indice.baselines)
        offtimes = trace.zip_slice(adt.indice.offtimes)
        for ontime, baseline in zip(ontimes, baselines):
            ontime.compensate(baseline, adt.frame.baseline)
        self = cls(value, ontimes, offtimes, baselines)
        self.capture_frequency = adt.capture_frequency
        return self
    def __repr__(self):
        return '{}({})'.format(type(self).__name__, self.value)
    @property
    def mean(self):
        return self.meantrace.mean()
    @property
    def meantrace(self):
        return np.array([rep.array for rep in self.ontimes]).mean(0)
    @property
    def windowed_mean_for_ontimes(self):
        return [trial.array[
            int(1*self.capture_frequency):int(2*self.capture_frequency)
            # :
        ].mean() for trial in self.ontimes]
    @property
    def regular_mean_for_ontimes(self):
        return [trial.array[:].mean() for trial in self.ontimes]
    def toDict(self):
        return vars(self)
