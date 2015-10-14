import traceback

from pacu.core.svc.impl import spec
from pacu.core.svc.impl import specs
from pacu.core.svc.impl.exc import UserAbortException
from pacu.core.svc.impl.exc import ServiceRuntimeException
from pacu.core.svc.impl.exc import TimeoutException
from pacu.core.svc.impl.exc import ComponentNotFoundError
from pacu.core.svc.impl.service import Service
from pacu.core.svc.impl.component_dependency import ComponentDependency
from pacu.core.svc.impl.deps import Dependency

from pacu.core.svc.analysis.i3d.files.impl import Files
from pacu.core.svc.analysis.i3d.stack.impl import Stack
from pacu.core.svc.analysis.i3d.rois.impl import ROIs
from pacu.util.descriptor.set import DescriptorSet

import numpy as np
from joblib import Parallel, delayed
from joblib.pool import has_shareable_memory

p = Parallel(n_jobs=-1, max_nbytes=False) #, verbose=5)

# scanbox data should take complementary number (inverse)
def gml(mmap, x1, x2, y1, y2):
    return mmap[
        :, y1:y2, x1:x2
    ].mean(axis=(1, 2))

get_mean_lazy = delayed(gml)

# can reduce
import tifffile
class I3DAnalysisService(object):
    files = Dependency(Files)
    stack = Dependency(Stack).on(files, 'mat.memmap')
    rois = Dependency(ROIs)
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
    deps = DescriptorSet(Dependency)
    def get_frame(self, index):
        return self.stack.get_frame(index)
    def get_mean(self, x1, x2, y1, y2):
        jobs = [get_mean_lazy(arr, x1, x2, y1, y2)
                for arr in np.split(self.stack.raw, 8)]
        res = p(jobs)
        return np.concatenate(res).tolist()
        # return self.stack.mmap[
        #     :, y1:y2, x1:x2
        # ].mean(axis=(1,2)).tolist()

jz5 = '/Volumes/Users/ht/tmp/pysbx-data/JZ5/JZ5_000_003'
jz6 = '/Volumes/Users/ht/tmp/pysbx-data/JZ6/JZ6_000_003'
qwe = I3DAnalysisService(files=jz5)
# X1:333, X2:357, Y1:122, Y2:145
x1 = 338
x2 = 360
y1 = 125
y2 = 145
# print x1, x2, y1, y2

# larger
# x1=262
# x2=381
# y1=94
# y2=164
# q1 = qwe.stack.raw[:, y1:y2, x1:x2].mean(axis=(1,2))
# q2 = qwe.stack.raw[:, y1:y2, x1:x2].mean(axis=(2,1))
# q2 = qwe.stack.raw[:, 0:10, 0:10]  #.mean()
# s=time.time();np.concatenate(p(js));print time.time()-s

# 
# s=time.time();multi=np.concatenate(p(js));print time.time()-s
# s=time.time();multi=np.concatenate(p(js));print time.time()-s
# s=time.time();single=get_mean(qwe.stack.mmap);print time.time()-s

# q = Parallel(n_jobs=2, max_nbytes=1e6)(
#     [delayed(np.ones)(10)]
# )
# qwe.rois
# print I3DAnalysisService.file.bindings.items()


# dict(
#     pkgname='a.b.c',
#     clsname='Something',
#     args=(),
#     kwargs=dict(
#         deeper=dict(
#             pkgname='b.c.d',
#             clsname='Yeah',
#             args=(),
#             kwargs=()
#         )
#     )
# )

# pickles
#     for
#     O2MORM
#     O2OORM
#     M2MORM
