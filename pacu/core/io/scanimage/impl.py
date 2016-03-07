import shutil
import ujson
import struct
from collections import namedtuple

import tifffile
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

from pacu.util.path import Path
from pacu.util.prop.memoized import memoized_property
from pacu.core.io.scanimage.legacy.cfaan import driftcorrect

from ipdb import set_trace

class ScanimageIO(object):
    def __init__(self, path):
        self.path = Path(path).with_suffix('.imported')
    @property
    def exists(self):
        return self.path.is_dir()
    def import_raw(self):
        print 1
        if self.exists:
            return False
        self.path.mkdir()
        print 'DONE!'
        return self.toDict()
    def remove_package(self):
        shutil.rmtree(self.path.str)
        return self.toDict()
    def toDict(self):
        return dict(
            exists = self.exists,
            path = self.path.str
        )
# gene = '6s3I'
# Meta = namedtuple('ScanimageMeta', 'dtype z y x')
# Pathz = namedtuple('Pathz', 'ch1mmp str rec')
# suffixes = '.ch1.mmp', '.str', '.rec.npy'
# 
# class ScanimageIO(object):
#     @classmethod
#     def import_raw(cls, path):
#         path = Path(path).resolve()
#         tiff = tifffile.imread(path.str)
#         chan1 = tiff[0::2, ...] # green?
#         drift = driftcorrect.getdrift3(chan1)
#         corr = driftcorrect.driftcorrect2(chan1, drift)
#         record = struct.pack(gene, corr.dtype.name, *corr.shape)
#         meta = Meta(*struct.unpack(gene, record))
#         max = corr.max(axis=(1,2))
#         min = corr.min(axis=(1,2))
#         mean = corr.mean(axis=(1,2))
#         std = corr.std(axis=(1,2))
#         rec = np.rec.fromarrays([max, min, mean, std], names='MAX, MIN, MEAN, STD')
#         mmppath, strpath, recpath = path.with_suffixes(*suffixes)
#         mmp = np.memmap(mmppath.str,
#             mode='w+', dtype=corr.dtype, shape=corr.shape)
#         mmp[:] = corr[:]
#         strpath.write(record, mode='wb')
#         np.save(recpath.str, rec)
#         return cls(recpath.stempath)
#     @classmethod
#     def can_resolve(cls, filename):
#         try   : cls.resolve_path(filename)
#         except: return False
#         else  : return True
#     @classmethod
#     def resolve_path(cls, stempath):
#         return Pathz(*[
#             path.resolve() for path
#             in Path(stempath).with_suffixes(*suffixes)
#         ])
#     def __init__(self, stempath):
#         self.pathz = self.resolve_path(stempath)
#         self.meta = Meta(*struct.unpack(gene, self.pathz.str.read('rb')))
#         stat = np.load(self.pathz.rec.str)
#         self.stat = np.rec.fromrecords(stat, dtype=stat.dtype)
#         shape = self.meta.z, self.meta.y, self.meta.x
#         self.io = np.memmap(self.pathz.ch1mmp.str,
#                 dtype=self.meta.dtype, mode='r', shape=shape)
#     @memoized_property
#     def io8bit(self):
#         return self.io.view('uint8')[..., 1::2]
#     @property
#     def dimension(self):
#         return dict(width=self.meta.x, height=self.meta.y, depth=self.meta.z)
#     @property
#     def max_index(self):
#         return self.meta.z - 1
#     def grand_trace(self):
#         return self.stat.MEAN
#     def request_frame(self, index):
#         return self.smap.to_rgba(self.io8bit[index], bytes=True)
#     def trace(self, x1, x2, y1, y2):
#         return (self.io[:, y1:y2, x1:x2]).mean(axis=(1,2))
#     @memoized_property
#     def smap(self): # bad practice - change name
#         norm = Normalize(vmin=0, vmax=self.stat.MAX.max()/256)
#         return ScalarMappable(norm=norm, cmap=plt.get_cmap('jet'))
# 
# def test():
#     test ='/Volumes/Gandhi Lab - HT/sci/2014.12.20/x.140801.1/field004.tif'
#     # qwe = ScanimageIO.import_raw(test)
#     qwe = ScanimageIO(test)
#     from matplotlib.pyplot import imshow
#     get_ipython().magic('pylab')
#     imshow(qwe.request_frame(0))
#     return qwe

test ='/Volumes/Gandhi Lab - HT/sci/2014.12.20/x.140801.1/field004.tif'
# qwe = ScanimageIO(test)
# from matplotlib.pyplot import *
# get_ipython().magic('pylab')
# 
# import matplotlib.pyplot as plt
# from matplotlib.colors import Normalize
# from matplotlib.cm import ScalarMappable
# 
# norm = Normalize(vmin=0, vmax=53)
# smap = ScalarMappable(norm=norm, cmap=plt.get_cmap('jet'))
# imshow(smap.to_rgba(qwe.io8bit[0], bytes=True))
