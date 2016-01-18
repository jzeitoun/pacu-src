import numpy as np
from scipy import io

from pacu.util.prop.memoized import memoized_property
from pacu.core.io.scanbox.view.info import ScanboxInfoView
from pacu.core.io.scanbox.view.data import ScanboxDataView

max_uint16 = np.iinfo(np.uint16).max

class ScanboxIO(object):
    def __init__(self, name):
        self.info = ScanboxInfoView(name + '.mat')
        self.data = ScanboxDataView(name + '.sbx')
    @property
    def max_index(self):
        if self.info.scanbox_version > 1:
            return int(self.data.size/self.info.recordsPerBuffer
                /self.info.sz.width*self.info.factor/4)
        else:
            return int(self.data.size/self.info.bytesPerBuffer*self.info.factor)
    @property
    def nsamples(self): # bytes per record
        return self.info.sz.width * self.info.recordsPerBuffer * 2 * self.info.nchan
    @property
    def shape(self):
        return (self.info.sz.width, self.info.recordsPerBuffer, self.info.nchan, self.max_index)
    @memoized_property
    def io(self):
        return np.memmap(self.data.file,
            dtype='uint16', mode='r', shape=self.shape, order='F'
        ).transpose(3, 1, 0, 2)[..., 0]
    def __getitem__(self, key):
        return max_uint16 - self.io.__getitem__(key)
