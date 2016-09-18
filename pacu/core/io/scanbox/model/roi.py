import cv2
import operator
import numpy as np
from collections import OrderedDict
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
    active = Column(Boolean, default=False) # do not use for a while
    @property
    def contours(self):
        return np.array([[p['x'], p['y']] for p in self.polygon])
    @property
    def neuropil_contours(self):
        return np.array([[p['x'], p['y']] for p in self.neuropil_polygon])
    @property
    def dt_ori_by_sf(self):
        sfs = self.workspace.condition.sfrequencies
        oris = self.workspace.condition.orientations
        trials = self.datatags.filter_by(trial_flicker=False, trial_blank=False)
        return OrderedDict([
            (
                sf,
                OrderedDict([
                (
                    ori,
                    trials.filter_by(trial_sf=sf, trial_ori=ori)
                )
                for ori in oris])
            ) for sf in sfs])

    def before_flush_dirty(self, session, context): # before attached to session
        pass
        # if inspect(self).attrs.polygon.history.has_changes():
        #     for tag in self.datatags:
        #         if not inspect(tag).attrs.value.history.has_changes():
        #             tag.invalidate()
    def before_flush_new(self, session, context):
        self.initialize_datatags()
    def initialize_datatags(self): # order is very important.
        from pacu.core.io.scanbox.model.datatag import Datatag
        Datatag(roi=self, category=u'overall', method=u'mean')
        for trial in self.workspace.condition.trials:
            dt = Datatag(roi=self, # trial=trial,
                category=u'orientation', method=u'dff0')
            for attr in TRIAL_ATTRS:
                setattr(dt, u'trial_' + attr, getattr(trial, attr))
        Datatag(roi=self, category=u'orientation', method=u'best_pref')
        for sf in self.workspace.condition.sfrequencies:
            Datatag(roi=self, category=u'fit', method=u'sumof', trial_sf=sf)
        Datatag(roi=self, category=u'fit', method=u'diffof')
        Datatag(roi=self, category=u'anova', method=u'all')
        Datatag(roi=self, category=u'bootstrap', method=u'sf')
    def refresh_all(self):
        dts0 = self.datatags.filter_by(category='overall', method='mean')
        dts1 = self.datatags.filter_by(category='orientation', method='dff0')
        dts2 = self.datatags.filter_by(category='orientation', method='best_pref')
        dts3 = self.datatags.filter_by(category='fit', method='sumof')
        dts4 = self.datatags.filter_by(category='fit', method='diffof')
        dts5 = self.datatags.filter_by(category='anova', method='all')
        dts6 = self.datatags.filter_by(category='bootstrap', method='sf')
        print 'REFRESH TRACE'
        for tag in dts0: tag.refresh()
        print 'REFRESH df/f0'
        for tag in dts1: tag.refresh()
        print 'REFRESH best pref'
        for tag in dts2: tag.refresh()
        print 'REFRESH SoG'
        for tag in dts3: tag.refresh()
        print 'REFRESH DoG'
        for tag in dts4: tag.refresh()
        print 'Anova All'
        for tag in dts5: tag.refresh()
        # print 'Bootstrap SF'
        # for tag in dts6: tag.refresh()





















