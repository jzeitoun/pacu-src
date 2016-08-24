import runpy
import importlib
import cv2
import operator
import numpy as np
from sqlalchemy import Column, Integer, Boolean
from sqlalchemy.types import PickleType

from pacu.core.io.scanbox.model.base import SQLite3Base
from sqlalchemy import inspect

origet = operator.attrgetter('ori')

class ROI(SQLite3Base):
    __tablename__ = 'rois'
    polygon = Column(PickleType, default=[])
    centroid = Column(PickleType, default=dict(x=-1, y=-1))
    active = Column(Boolean, default=False)
    # @property
    # def meantrace(self):
    #     for trace in self.traces:
    #         if trace.category == 'mean':
    #             if not len(trace.array):
    #                 trace.refresh()
    #             return trace
    @property
    def contours(self):
        return np.array([[p['x'], p['y']] for p in self.polygon])
    def get_trace(self):
        frames = self.workspace.io.channel.mmap
        mask = np.zeros(frames.shape[1:], dtype='uint8')
        cv2.drawContours(mask, [self.contours], 0, 255, -1)
        return np.stack(cv2.mean(frame, mask)[0] for frame in frames)
    def before_flush_dirty(self, session, context): # before attached to session
        pass
        # if inspect(self).attrs.polygon.history.has_changes():
        #     for tag in self.datatags:
        #         if not inspect(tag).attrs.value.history.has_changes():
        #             tag.invalidate()
    def compute_orientations(self):
        workspace = self.workspace
        condition = workspace.condition
        cur_sfreq = workspace.cur_sfreq
        duration = condition.on_duration
        frate = workspace.io.mat.framerate # capture_frequency
        frames = int(frate * duration)
        sftrials = [t for t in condition.trials if t.sf == cur_sfreq]
        meantrace = self.meantrace.array
        oris = []
        for ori in condition.orientations:
            traces = []
            for trial in sftrials:
                if trial.ori == ori:
                    sindex = int(trial.on_time * frate)
                    traces.append(meantrace[sindex:sindex+frames])
            oris.append(np.vstack(traces))
        oris = np.concatenate(oris, axis=1)
        indices = {o: i*frames for i, o in enumerate(condition.orientations)}
        return dict(traces=oris, mean=oris.mean(0), indices=indices)
    def refresh_all(self):
        workspace=self.workspace
        condition=self.workspace.condition
        basemodule = 'pacu.core.io.scanbox.method'
        for tag in self.datatags:
            module = '.'.join((basemodule, tag.category, tag.method))
            runpy.run_module(module, run_name='__sbx_main__', init_globals=dict(
                workspace=workspace,
                condition=condition,
                roi=self,
                datatag=tag,
            ))
