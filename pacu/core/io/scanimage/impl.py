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
from pacu.core.io.scanimage.roi.impl import ROI
from pacu.core.io.scanimage.response.impl import Response
from pacu.core.io.scanimage.response.main import MainResponse
from pacu.core.io.scanimage.response.roi import ROIResponse
from pacu.core.io.scanimage.response.orientation import Orientation

class ScanimageIO(object):
    session_name = 'main'
    def __init__(self, path):
        self.path = Path(path).with_suffix('.imported')
    @classmethod
    def get_record(cls, rec_path):
        return ScanimageRecord(rec_path)
    @property
    def exists(self):
        return self.path.is_dir()
    @memoized_property
    def tiff(self):
        tiffpath = self.path.with_suffix('.tif')
        print 'Import from {}...Please allow a few minutes.'.format(tiffpath.name)
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
            self.convert_channel(nchan, index)
    def convert_channel(self, nchan, chan):
        tiff = self.tiff[chan::nchan]
        print 'Converting channel {}...({} frames.)'.format(chan, len(tiff))
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
    def channel(self):
        chan = self.session.opt.setdefault('channel', 0)
        return getattr(self, 'ch{}'.format(chan))
    @channel.invalidator
    def set_channel(self, channel):
        self.session.opt['channel'] = channel
        return self
    @property
    def sfrequency(self):
        return self.db.locator.sfrequencies.current
        # return self.session.opt.setdefault(#  'sfrequency', )
    @property
    def sfrequency_index(self):
        return self.sfrequencies.index(self.sfrequency)
    @property
    def sfrequencies(self):
        return self.db.locator.sfrequencies
    # @sfrequency.invalidator
    def set_sfrequency_index(self, sfreq_index):
        self.sfrequencies.set_cursor(sfreq_index)
        self.session.opt['sfrequency'] = self.sfrequencies.current
        self.session.opt.save()
        return dict(index=sfreq_index, value=self.sfrequency)
    @memoized_property
    def db(self):
        return ScanimageDBAdaptor(self.session.ed)
    @property
    def main_response(self):
        return MainResponse.from_adaptor(self.channel.stat.MEAN, self.db)
    @property
    def sessions(self):
        return map(ScanimageSession, sorted(self.path.ls('*.session')))
    @memoized_property
    def session(self):
        return ScanimageSession(
            self.path.joinpath(self.session_name).with_suffix('.session'))
    @session.invalidator
    def set_session(self, session_name):
        self.session_name = session_name
        return self
    def upsert_roi(self, roi_kwargs):
        return self.session.roi.upsert(ROI(**roi_kwargs))
    def invalidate_rois(self):
        for roi in self.session.roi.values():
            roi.invalidated = True
            roi.blank = None
            roi.flicker = None
            roi.responses = {}
        self.session.roi.save()
    def make_trace(self, roi): # checked same function
        extras = self.session.roi.values()
        extras.remove(roi)
        main_trace, main_mask = roi.trace(self.channel.mmap)
        neur_trace, neur_mask = roi.neuropil_trace(self.channel.mmap, extras)
        # neuropil_mask, roi_mask = roi.trim_bounding_mask(neur_mask, main_mask)
        # roi.masks = dict(
        #     neuripil = neuropil_mask.tolist(),
        #     roi = roi_mask.tolist())
        return main_trace - neur_trace*0.7
    def update_responses(self, id):
        roi = self.session.roi[id]
        trace = self.make_trace(roi)
        with self.session.roi.bulk_on:
            try:
                if self.db.locator.override_blank(True):
                    roi.blank = Orientation.from_adaptor('blank', trace, self.db)
                if self.db.locator.override_flicker(True):
                    roi.flicker = Orientation.from_adaptor('flicker', trace, self.db)
            finally:
                self.db.locator.override()
            for sf in self.db.locator.sfrequencies.loop():
                response = ROIResponse.from_adaptor(roi, trace, self.db)
                roi.responses[self.sfrequency] = response
            roi.update_with_adaptor(self.db)
            for sf, resp in roi.sorted_responses:
                print '\tudpate fit and decay for', sf
                resp.update_fit_and_decay(roi, self.db)
            roi.invalidated = False
            return self.session.roi.upsert(roi)


# from pacu.core.io.scanimage.response.orientation import Orientation
# path = 'tmp/Dario/2015.12.02/x.151101.2/bV1_Contra_004'
# path = 'tmp/Dario/2016.02.26/x.151114.1/DM3_RbV1_Contra_00002'

path = 'tmp/Dario/2016.01.27/r.151117.3/DM9_RbV1_Contra004004'
qwe = ScanimageIO(path)
roi = qwe.session.roi.one().val
# for sf, re in roi.sorted_responses:
#     print re.normalfit.gaussian.r_max
#     print re.normalfit.gaussian.o_peaks


class ScanimageRecord(object):
    """
    For `compatible_path`,
    the path should be formed like below. For example,
    '/Volumes/Data/Recordings/2P1/Dario/2015.11.20/x.151101.4/ref_p19_005.tif',
    This will be considered as,
    {whatever_basepath}/{experimenter}/{date}/{mousename}/{imagename}
    So the directory structure always will matter.
    """
    def __init__(self, compatible_path):
        self.tiff_path = Path(compatible_path).with_suffix('.tif')
        self.package_path = Path(compatible_path).with_suffix('.imported')
        self.mouse, self.date, self.user = self.tiff_path.parts[::-1][1:4]
    def toDict(self):
        return dict(
            user = self.user,
            mouse = self.mouse,
            date = self.date,
            desc = self.desc,
            name = self.tiff_path.stem,
            package = self.package
       )
    @memoized_property
    def package(self):
        return ScanimageIO(self.package_path)
    @property
    def desc(self):
        return '{}'.format(
            tifffile.format_size(self.tiff_path.stat().st_size)
        )

def testdump():
    path = 'tmp/Dario/2015.12.02/x.151101.2/bV1_Contra_004'
    qwe = ScanimageIO(path)
    qwe.session.roi.clear()
    qwe.session.opt.clear()
    from pacu.util.identity import path
    rois = path.cwd.ls('*pickle')[0].load_pickle().get('rois')
    pgs = [[dict(x=x, y=y) for x, y in roi] for roi in rois]
    kws = [dict(polygon=p) for p in pgs]
    for kw in kws:
        qwe.session.roi.upsert(ROI(**kw))

def testdump2():
    path = 'tmp/Dario/2016.01.27/r.151117.3/DM9_RbV1_Contra004004'
    qwe = ScanimageIO(path)
    qwe.session.roi.clear()
    qwe.session.opt.clear()
    rois = [
        ([75,27], [71,27], [69,30], [69,34], [71,36], [75,36], [78,35], [79,32], [78,29]),
        ([60,72], [57,72], [55,75], [56,78], [58,79], [62,79], [64,76], [63,73]),
        ([53,47], [51,44], [48,43], [45,43], [43,46], [43,49], [46,51], [50,51], [52,50]),
        ([53, 104], [55, 108], [59, 110], [64, 109], [65, 105], [63, 101], [58, 100], [55, 101])
    ]
    pgs = [[dict(x=x, y=y) for x, y in roi] for roi in rois]
    kws = [dict(polygon=p) for p in pgs]
    for kw in kws:
        roi = qwe.session.roi.upsert(ROI(**kw))
        qwe.update_responses(roi.id)

def ScanimageIOFetcher(year, month, day, mouse, image, session):
    root = manager.instance('opt').scanimage_root
    date = '{}.{:2}.{:2}'.format(year, month, day)
    path = Path(root).joinpath(date, mouse, image)
    return ScanimageIO(path).set_session(session)
