import cv2
import operator
import numpy as np
from sqlalchemy import Column, Integer, Boolean, Float
from sqlalchemy.types import PickleType
from sqlalchemy.orm import object_session

from pacu.core.io.scanbox.model.base import SQLite3Base
from sqlalchemy import inspect

origet = operator.attrgetter('ori')
TRIAL_ATTRS = 'on_time off_time ori sf tf sequence order ran flicker blank'.split()

class ROI(SQLite3Base):
    __tablename__ = 'rois'
    polygon = Column(PickleType, default=[])
    centroid = Column(PickleType, default=dict(x=-1, y=-1))
    neuropil_ratio = Column(Float, default=4.0, nullable=False)
    neuropil_factor = Column(Float, default=0.7, nullable=False)
    neuropil_polygon = Column(PickleType, default=[])
    neuropil_enabled = Column(Boolean, default=True)
    active = Column(Boolean, default=False)
    @property
    def contours(self):
        return np.array([[p['x'], p['y']] for p in self.polygon])
    @property
    def neuropil_contours(self):
        return np.array([[p['x'], p['y']] for p in self.neuropil_polygon])
    @property
    def dt_overall(self):
        for dt in self.datatags:
            if dt.category == 'overall':
                return dt
    @property
    def dt_best_preferred(self):
        for dt in self.datatags:
            if dt.method == 'best_pref':
                return dt
    @property
    def dt_reps(self):
        for dt in self.datatags:
            if dt.method == 'dff0':
                return dt
    @property
    def dt_fit_sumof(self):
        return self.datatags.find_by('method', 'sumof')
    @property
    def dt_fit_diffof(self):
        return self.datatags.find_by('method', 'diffof').first

    def before_flush_dirty(self, session, context): # before attached to session
        pass
        # if inspect(self).attrs.polygon.history.has_changes():
        #     for tag in self.datatags:
        #         if not inspect(tag).attrs.value.history.has_changes():
        #             tag.invalidate()
    def before_flush_new(self, session, context):
        self.initialize_datatags()
    def refresh_all(self):
        for tag in self.datatags:
            tag.refresh()
    def initialize_datatags(self): # order is very important.
        from pacu.core.io.scanbox.model.datatag import Datatag
        Datatag(roi=self, category=u'overall', method=u'mean')
        for trial in self.workspace.condition.trials:
            dt = Datatag(roi=self, trial=trial,
                category=u'orientation', method=u'dff0')
            for attr in TRIAL_ATTRS:
                setattr(dt, u'trial_' + attr, getattr(trial, attr))
        Datatag(roi=self, category=u'orientation', method=u'best_pref')
        for sf in self.workspace.condition.sfrequencies:
            Datatag(roi=self, category=u'fit', method=u'sumof', trial_sf=sf)
        Datatag(roi=self, category=u'fit', method=u'diffof')
