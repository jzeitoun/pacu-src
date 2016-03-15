from pacu.core.io.scanimage.trace.whole import WholeTrace

class Orientation(object):
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
        return cls(value, ontimes, offtimes, baselines)
    def __repr__(self):
        return '{}({})'.format(type(self).__name__, self.value)
