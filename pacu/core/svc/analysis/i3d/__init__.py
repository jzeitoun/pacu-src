import ujson
import math
import numpy.core.memmap as memmap
import matplotlib.pyplot as plt

from ipdb import set_trace

from pacu.util.path import Path
from pacu.profile import manager
from pacu.core.io.scanbox.impl import ScanboxIO
from pacu.core.io.scanbox.condition import ScanboxCondition
from pacu.core.model.ed.visstim2p import VisStim2P
from pacu.core.model.experiment import ExperimentV1
from pacu.core.model.analysis import AnalysisV1
from pacu.core.method.twophoton.tuning.parse import Response
from pacu.core.method.twophoton.frequency.spatial.meta import SpatialFrequencyMeta

DB = manager.get('db').as_resolved
ED = manager.get('db').section('ed')

jet = getattr(plt.cm, 'jet')

class I3DAnalysisService(object):
    sbx = None
    def debug(self):
        set_trace()
    def __init__(self, files): # analysis_v1 id will come in
        self.db, self.ed = DB(), ED()
        av1 = self.db.query(AnalysisV1).get(files)
        if av1.type == '0': # ScanImage
            self.condition = ScanImageCondition(
                **vars(self.ed.query(VisStim2P).get(av1.conditionid)))
        else: # Scanbox
            self.condition = ScanboxCondition(
                **vars(self.db.query(ExperimentV1).get(av1.conditionid)))
        self.av1 = av1
        self.sbx = ScanboxIO(av1.imagesrc)
        self.sfreq_meta = SpatialFrequencyMeta(self.condition)
    @property
    def dimension(self):
        height, width = map(int, self.sbx.info.sz) # from numpy int
        return dict(width=width, height=height)
    @property
    def max_index(self):
        return self.sbx.nframes - 1
    def request_frame(self, index):
        data = self.sbx.io8bit[index]
        return jet(~data, bytes=True).tostring()
    def get_grand_response(self):
        trace = self.get_grand_trace()
        # set_trace()
    def get_grand_trace(self):
        key = 'cache.grand_trace'
        if key not in self.av1.data:
            value = ~self.sbx.io
            trace = value.mean(axis=(1,2))
            self.av1.data[key] = trace.tolist()
            self.db.commit()
        return self.av1.data.get(key)
    def get_current_sfrequency(self):
        key = 'current_sfrequency'
        if key not in self.av1.data:
            value = 0
            self.av1.data[key] = value
            self.db.commit()
        return self.av1.data.get(key)
    def get_trace(self, x1, x2, y1, y2):
        # self.get_trace(377, 426, 167, 219)
        return (~self.sbx.io[:, y1:y2, x1:x2]).mean(axis=(1,2))
    def get_response(self, x1, x2, y1, y2):
        trace = self.get_trace(x1, x2, y1, y2)
        try:
            resp = Response(trace, self.condition, self.sfreq_meta)
        except Exception as e:
            raise Exception('Failed to get response: ' + str(e))
        rv = dict(
            OSI      = resp.OSI,
            CV       = resp.CV,
            DSI      = resp.DSI,
            sigma    = resp.sigma,
            OPref    = resp.Opref,
            RMax     = resp.Rmax,
            Residual = resp.Residual,
        )
        return {
            key: "NaN" if math.isnan(val) else float(val)
            for key, val in rv.items()
        }


# qwe = I3DAnalysisService(4)
# t = qwe.get_grand_trace()
# sfm = SpatialFrequencyMeta(qwe.condition)
# r = Response(t, qwe.condition, sfm)

#     def __init__(self, mmap):
#         if isinstance(mmap, memmap):
#             self.raw = mmap[..., 0]
#             # print 'invmin', 65535 - self.raw.max()
#             # print 'invmax', 65535 - self.raw.min()
#             self.mmap8 = 
#             self.shape = self.raw.shape
#         else:
#             self.error = TypeError(mmap)
#     def get_frame(self, index=0): # returns binary
#         return jet(~self.mmap8[index], bytes=True).tostring()

#     @property
#     def width(self):
#         return self.sbx.shape[0]
#     @property
#     def height(self):
#         return self.sbx.shape[1]
#     files = Dependency(Files)
#     stack = Dependency(Stack).on(files, 'mat.memmap')
#     rois = Dependency(ROIs)
#     def __init__(self, **kwargs):
#         for key, val in kwargs.items():
#             setattr(self, key, val)
#     deps = DescriptorSet(Dependency)
#     def get_frame(self, index):
#         return self.stack.get_frame(index)
#     def get_mean(self, x1, x2, y1, y2):
#         pass
        # jobs = [get_mean_lazy(arr, x1, x2, y1, y2)
        #         for arr in np.split(self.stack.raw, 8)]
        # res = p(jobs)
        # return np.concatenate(res).tolist()
        # return self.stack.mmap[
        #     :, y1:y2, x1:x2
        # ].mean(axis=(1,2)).tolist()

# jz5 = '/Volumes/Users/ht/tmp/pysbx-data/JZ5/JZ5_000_003'
# jz6 = '/Volumes/Users/ht/tmp/pysbx-data/JZ6/JZ6_000_003'
# # qwe = I3DAnalysisService(files=jz5)
# # X1:333, X2:357, Y1:122, Y2:145
# x1 = 338
# x2 = 360
# y1 = 125
# y2 = 145
# # print x1, x2, y1, y2
# 
# # larger
# # x1=262
# # x2=381
# # y1=94
# # y2=164
# # q1 = qwe.stack.raw[:, y1:y2, x1:x2].mean(axis=(1,2))
# # q2 = qwe.stack.raw[:, y1:y2, x1:x2].mean(axis=(2,1))
# # q2 = qwe.stack.raw[:, 0:10, 0:10]  #.mean()
# # s=time.time();np.concatenate(p(js));print time.time()-s
# 
# # 
# # s=time.time();multi=np.concatenate(p(js));print time.time()-s
# # s=time.time();multi=np.concatenate(p(js));print time.time()-s
# # s=time.time();single=get_mean(qwe.stack.mmap);print time.time()-s
# 
# # q = Parallel(n_jobs=2, max_nbytes=1e6)(
# #     [delayed(np.ones)(10)]
# # )
# # qwe.rois
# # print I3DAnalysisService.file.bindings.items()
# 
# 
# # dict(
# #     pkgname='a.b.c',
# #     clsname='Something',
# #     args=(),
# #     kwargs=dict(
# #         deeper=dict(
# #             pkgname='b.c.d',
# #             clsname='Yeah',
# #             args=(),
# #             kwargs=()
# #         )
# #     )
# # )
# 
# # pickles
# #     for
# #     O2MORM
# #     O2OORM
# #     M2MORM
