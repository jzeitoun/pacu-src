import numpy as np
from sqlalchemy import Column, Unicode, Integer
from sqlalchemy.types import PickleType

from pacu.core.io.scanbox.model.base import SQLite3Base

class EphysCorrelation(SQLite3Base):
    __tablename__ = 'ephys_correlations'
    traces = Column(PickleType, default=[])
    meantrace = Column(PickleType, default=[])
    rmeantrace = Column(PickleType, default=[])
    roi_ids = Column(PickleType, default=[])
    window = Column(Integer, default=100)
    def refresh(self):
        ws = self.workspace
        window = self.window
        rois = [roi for roi in ws.rois if roi.id in self.roi_ids]
        arrays = [r.traces[0].array for r in rois]
        peaks = np.flatnonzero(np.array(ws.io.ephys.trace))
        slices = [slice(s, e) for s, e in zip(peaks-window, peaks+window)
            if 0 <= s]
        traces = [array[sl] for array in arrays for sl in slices]
        if not traces:
            raise Exception('There is no ephys trace bound.')
        maxlen = max(map(len, traces))
        traces = np.array([t for t in traces if len(t) == maxlen])
        bases = traces.mean(1)
        traces = np.array([(trace-base)/base for trace, base in zip(traces, bases)])
        meantrace = traces.mean(0)
        rands = np.random.choice(
            np.arange(len(ws.io.ephys.trace)),len(peaks), replace=False)
        rslices = [slice(s, e) for s, e in zip(rands-window, rands+window)
            if 0 <= s]
        rtraces = [array[sl] for array in arrays for sl in rslices]
        rmaxlen = max(map(len, rtraces))
        rtraces = np.array([t for t in rtraces if len(t) == rmaxlen])
        rbases = rtraces.mean(1)
        rtraces = np.array([(t-b)/b for t, b in zip(rtraces, rbases)])
        rmeantrace = rtraces.mean(0)
        self.rmeantrace = rmeantrace
        self.meantrace = meantrace
        self.traces = traces
