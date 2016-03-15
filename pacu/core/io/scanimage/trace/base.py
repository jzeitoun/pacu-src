class BaseTrace(object):
    start = 0
    end = -1
    def compensate(self, baseline, n_frames):
        early_index = len(baseline.array) - n_frames
        f_0 = baseline.array[early_index:].mean()
        if f_0 != 0:
            self.array[:] = (self.array - f_0)/f_0
            baseline.array[:] = (baseline.array - f_0)/f_0
