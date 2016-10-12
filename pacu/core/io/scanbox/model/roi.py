import cv2
import operator
import numpy as np
from collections import OrderedDict
from sqlalchemy import Column, Integer, Boolean, Float, UnicodeText
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
    draw_dtoverallmean = Column(Boolean, default=False)
    object_session = property(object_session)
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
        trials = self.dttrialdff0s.filter_by(trial_flicker=False, trial_blank=False)
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
        from pacu.core.io.scanbox.model.datatag import DTOverallMean
        from pacu.core.io.scanbox.model.datatag import DTTrialDff0
        from pacu.core.io.scanbox.model.datatag import DTOrientationsMean
        from pacu.core.io.scanbox.model.datatag import DTOrientationBestPref
        from pacu.core.io.scanbox.model.datatag import DTOrientationsFit
        from pacu.core.io.scanbox.model.datatag import DTSFreqFit
        from pacu.core.io.scanbox.model.datatag import DTAnovaAll
        from pacu.core.io.scanbox.model.datatag import DTAnovaEach
        condition = self.workspace.condition
        if not self.dtoverallmean:
            print 'Initialize Overall Mean'
            DTOverallMean(roi=self)
        if not condition.imported:
            return
        if not self.dttrialdff0s:
            print 'Initialize Trial DFF0'
            for trial in condition.trials:
                dt = DTTrialDff0(roi=self)
                for attr in TRIAL_ATTRS:
                    setattr(dt, u'trial_' + attr, getattr(trial, attr))
        if not self.dtorientationsmeans:
            print 'Initialize Orientations Mean'
            for sf in self.workspace.condition.sfrequencies:
                DTOrientationsMean(roi=self, trial_sf=sf)
        if not self.dtorientationbestpref:
            print 'Initialize Orientation Best Pref'
            DTOrientationBestPref(roi=self)
        if not self.dtorientationsfits:
            print 'Initialize Orientations Fit'
            for sf in condition.sfrequencies:
                DTOrientationsFit(roi=self, trial_sf=sf)
        if not self.dtanovaeachs:
            print 'Initialize Anova Each'
            for sf in condition.sfrequencies:
                DTAnovaEach(roi=self, trial_sf=sf)
        if not self.dtsfreqfit:
            print 'Initialize SFreq Fit'
            DTSFreqFit(roi=self)
        if not self.dtanovaall:
            print 'Initialize Anova All'
            DTAnovaAll(roi=self)
    def refresh_all(self):
        print 'REFRESH TRACE'
        self.dtoverallmean.refresh()
        print 'REFRESH df/f0'
        for tag in self.dttrialdff0s: tag.refresh()
        print 'REFRESH Orientations'
        for tag in self.dtorientationsmeans: tag.refresh()
        print 'REFRESH BEST PREF'
        if self.dtorientationbestpref:
            self.dtorientationbestpref.refresh()
        print 'REFRESH OriFit'
        for tag in self.dtorientationsfits: tag.refresh()
        print 'REFRESH SFreqFit'
        if self.dtsfreqfit:
            self.dtsfreqfit.refresh()
        print 'REFRESH Anova All'
        if self.dtanovaall:
            self.dtanovaall.refresh()
        print 'REFRESH Anova Each'
        for tag in self.dtanovaeachs: tag.refresh()
        # print 'Bootstrap SF'
        # for tag in dts6: tag.refresh()
    def export(self):
        fields = ('polygon', 'neuropil_ratio',
            'neuropil_enabled', 'neuropil_factor', 'neuropil_polygon')
        attrs = {f: getattr(self, f) for f in fields}
        return dict(id=self.id, attrs=attrs)


















