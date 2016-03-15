from __future__ import division
import shutil
import ujson

import tifffile
import numpy as np

from pacu.profile import manager
from pacu.util.path import Path
from pacu.util.prop.memoized import memoized_property
from pacu.core.io.scanimage.channel import ScanimageChannel
from pacu.core.io.scanimage.session import ScanimageSession
from pacu.core.io.scanimage.adaptor.db import ScanimageDBAdaptor
from pacu.core.io.scanimage import util
from pacu.core.io.scanimage.roi import ROI
from pacu.core.io.scanimage.response.impl import Response
from pacu.core.io.scanimage.response.main import MainResponse
from pacu.core.io.scanimage.response.roi import ROIResponse
from pacu.core.io.scanimage.response.orientation import Orientation

from ipdb import set_trace

class ScanimageIO(object):
    session = None
    channel = None
    def __init__(self, path):
        self.path = Path(path).with_suffix('.imported')
    @property
    def exists(self):
        return self.path.is_dir()
    @memoized_property
    def tiff(self):
        tiffpath = self.path.with_suffix('.tif')
        print 'Import from {}...'.format(tiffpath)
        return tifffile.imread(tiffpath.str)
    def import_raw(self):
        if self.exists:
            return False
        nchan = util.infer_nchannels(self.tiff)
        if nchan:
            self.create_package_path()
            self.convert_channels(nchan)
        else:
            print 'Unable to import data.'
        print 'Import done!'
        return self.toDict()
    def create_package_path(self):
        self.path.mkdir()
        print 'Path `{}` created.'.format(self.path.str)
    def remove_package(self):
        shutil.rmtree(self.path.str)
        return self.toDict()
    def convert_channels(self, nchan):
        for index in range(nchan):
            self.convert_channel(index)
    def convert_channel(self, chan):
        print 'Converting channel {}...'.format(chan)
        tiff = self.tiff[chan::2]
        return getattr(self, 'ch{}'.format(chan)).import_raw(tiff)
    def toDict(self):
        return dict(exists=self.exists, path=self.path.str, sessions=self.sessions)
    @memoized_property
    def ch0(self):
        return ScanimageChannel(self.path.joinpath('ch0'))
    @memoized_property
    def ch1(self):
        return ScanimageChannel(self.path.joinpath('ch1'))
    @memoized_property
    def db(self):
        return ScanimageDBAdaptor(self.session.ed)
    @property
    def sessions(self):
        sessions = self.path.ls('*.session')
        return [ScanimageSession(path) for path in sorted(sessions)]
    def create_session(self, name):
        path = self.path.joinpath(name).with_suffix('.session')
        ScanimageSession(path).data.create()
    def remove_session(self, name):
        path = self.path.joinpath(name).with_suffix('.session')
        ScanimageSession(path).data.remove()
    def with_session(self, name):
        path = self.path.joinpath(name).with_suffix('.session')
        self.session = ScanimageSession(path)
        return self
    def with_channel(self, chan=0):
        self.channel = getattr(self, 'ch{}'.format(chan))
        return self
    def upsert_roi(self, roi):
        return self.session.upsert(ROI(**roi))
    def remove_roi(self, roi):
        return self.session.remove(ROI(**roi))
    def make_response(self, roi):
        roi = ROI(**roi)
        trace = roi.trace(self.channel.mmap)
        response = ROIResponse.from_adaptor(trace, self.db)
        return self.session.upsert(roi, response=response)
    @property
    def main_response(self):
        return MainResponse.from_adaptor(self.channel.stat.MEAN, self.db)

def testdump():
    path = 'tmp/Dario/2015.12.02/x.151101.2/bV1_Contra_004'
    qwe = ScanimageIO(path).with_session('main').with_channel(1)
    qwe.session.data.purge().save()
    from pacu.util.identity import path
    rois = path.cwd.ls('*pickle')[0].load_pickle().get('rois')

# oneroi = rois[0]
# pgs = [dict(x=x, y=y) for x, y in oneroi]
# roi = ROI(polygon=pgs)
# atrace = roi.trace(qwe.channel.mmap)

    pgs = [[dict(x=x, y=y) for x, y in roi] for roi in rois]
    pgs = [dict(polygon=p) for p in pgs]
    import time
    for pg in pgs:
        time.sleep(0.01)
        qwe.upsert_roi(pg)

def ScanimageIOFetcher(year, month, day, mouse, image, session):
    root = manager.instance('opt').scanimage_root
    date = '{}.{:2}.{:2}'.format(year, month, day)
    path = Path(root).joinpath(date, mouse, image)
    return ScanimageIO(path).with_session(session).with_channel(1)
