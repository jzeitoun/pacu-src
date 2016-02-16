import tifffile
import numpy as np

from pacu.util.path import Path

class ScanimageIO(object):
    @classmethod
    def prepare(cls, filepath):
        path = Path(filepath).resolve()
        tiff = tifffile.imread(path.str)
        mmp = np.memmap(path.with_suffix('.mmp').str,
            mode='w+', dtype=tiff.dtype, shape=tiff.shape)
        mmp[:] = tiff[:]
        return mmp
    # @classmethod
    # def can_resolve(cls, filename):
    #     try   : cls.resolve_path(filename)
    #     except: return False
    #     else  : return True
    # @classmethod
    # def resolve_path(cls, filename):
    #     return {
    #         path.suffix: path.resolve()
    #         for path in Path(filename).with_suffixes('.tif', '.npy')
    #     }
    # def __init__(self, filename):
    #     pathz = ScanboxIO.resolve_path(filename)
    #     self.tif = ScanboxInfoView(pathz.get('.tif'))
    #     self.npy = ScanboxDataView(pathz.get('.npy'))
    # @dimension(self)
    # @max_index(self)
    # request_frame(self, index)
    # grand_trace(self)
    # trace(self, x1, x2, y1, y2)

test ='/Volumes/Gandhi Lab - HT/sci/2014.12.20/x.140801.1/field004.tif'
qwe = ScanimageIO.prepare(test)
#shape = (7712, 128, 128)
 #qwe = ScanimageIO(test)
# mmp = np.memmap('tifstack.mmp', dtype=np.uint16, shape=shape)
