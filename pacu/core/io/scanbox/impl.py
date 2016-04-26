from pacu.util.path import Path
from pacu.core.io.scanbox.view.sbx import ScanboxSBXView
from pacu.core.io.scanbox.view.mat import ScanboxMatView
from pacu.core.io.scanbox.channel import ScanboxChannel
from pacu.core.io.scanbox.session import ScanboxSession

class ScanboxIO(object):
    def __init__(self, path):
        self.path = Path(path).ensure_suffix('.io')
        self.sbxpath = self.path.with_suffix('.sbx')
        self.matpath = self.path.with_suffix('.mat')
    @property
    def mat(self):
        return ScanboxMatView(self.matpath)
    @property
    def sbx(self):
        return ScanboxSBXView(self.sbxpath)
    @property
    def meta(self):
        return dict(
            path = self.path.str,
            exists = self.path.is_dir(),
            mat = self.mat,
            sbx = self.sbx,
            sessions = sorted(self.path.ls('*.session')))
    def session(self, name):
        return ScanboxSession(self.path.joinpath('{}.session'.format(name)))
    def channel(self, number):
        return ScanboxChannel(self.path.joinpath('{}.chan'.format(number)))
    def remove_io(self):
        self.path.rmtree()
        return self.meta
    def import_raw(self):
        self.path.mkdir()
        for chan in range(s.mat.channels):
            self.channel(chan).import_with_io(self)
        return self.meta


# import numpy as np
# import ujson
# testpath = '/Volumes/Users/ht/dev/current/pacu/tmp/Jack/jc6/jc6_1_120_006.io'
# s = ScanboxIO(testpath)



#     x, y, _, z = sbx.shape
#     rgb = np.zeros((z, y, x, 3), dtype=sbx.io.dtype)
#     if nchan == 2:
#         rgb[..., 1] = ~sbx.ch0
#         rgb[..., 0] = ~sbx.ch1
#     elif nchan == 1:
#         rgb[..., 1] = ~sbx.ch0
#     tiffpath = sbx.path.with_name('tiff').mkdir_if_none()
#     dest = tiffpath.joinpath(sbx.path.name).with_suffix('.tiff')
#     tifffile.imsave(dest.str, rgb)











# print s.record.toDict()

#     @property
#     def datetime(self):
#         return datetime.fromtimestamp(
#             float(self.tiffpath.stem))
#     @property
#     def tiffpath(self):
#         return self.path.with_suffix('.tif')
#     def toDict(self):
#         return dict(exists=self.exists, path=self.path.str, sessions=self.sessions)
#     @memoized_property
#     def tiff(self):
#         tiffpath = self.path.with_suffix('.tif')
#         file_size = tiffpath.lstat().st_size
#         print 'Import from {}...'.format(tiffpath)
#         print 'File size {:,} bytes.'.format(file_size)
#         return tifffile.imread(tiffpath.str)
#     def create_package_path(self):
#         self.path.mkdir()
#         print 'Path `{}` created.'.format(self.path.str)
#     def remove_package(self):
#         shutil.rmtree(self.path.str)
#         return self.toDict()
#     @memoized_property
#     def channel(self):
#         tfilter = self.session.opt.get('filter')
#         if tfilter:
#             if tfilter._indices is not None:
#                 return TrajectoryChannel(self.path.joinpath('channel')
#                     ).set_indices(tfilter._indices)
#         return TrajectoryChannel(self.path.joinpath('channel'))
#     @property
#     def sessions(self):
#         return map(TrajectorySession, sorted(self.path.ls('*.session')))
#     @memoized_property
#     def session(self):
#         return TrajectorySession(
#             self.path.joinpath(self.session_name).with_suffix('.session'))
#     @session.invalidator
#     def set_session(self, session_name):
#         self.session_name = session_name
#         return self
#     @memoized_property
#     def alog(self): # aligned log in JSON format
#         return [
#             dict(e=e, x=x, y=y, v=v)
#             for e, x, y, v in self.channel.alog[['E', 'X', 'Y', 'V']]]
#     @property
#     def main_response(self):
#         return TrajectoryResponse(self.channel.stat.MEAN)
#     def upsert_roi(self, roi_kwargs):
#         return self.session.roi.upsert(ROI(**roi_kwargs))
#     def upsert_filter(self, filter_kwargs):
#         tfilter = TrajectoryFilter(**filter_kwargs)
#         tfilter._indices = tfilter.make_indices(self.channel.original_velocity)
#         rv = self.session.opt.upsert(tfilter)
#         for roi in self.session.roi.values():
#             roi.invalidated = True
#         self.session.roi.save()
#         return rv
#     def make_response(self, id):
#         roi = self.session.roi[id]
#         extras = self.session.roi.values()
#         extras.remove(roi)
#         main_trace, main_mask = roi.trace(self.channel.mmap)
#         neur_trace, neur_mask = roi.neuropil_trace(self.channel.mmap, extras)
#         trace = main_trace - neur_trace*0.7
#         roi.invalidated = False
#         roi.response = TrajectoryResponse(trace)
#         return self.session.roi.upsert(roi)
#     @memoized_property
#     def velocity_stat(self):
#         return dict(
#             max = self.channel.alog.V.max(),
#             mean = self.channel.alog.V.mean(),
#             min = self.channel.alog.V.min(),
#         )
