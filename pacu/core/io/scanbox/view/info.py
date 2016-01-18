from collections import namedtuple

import numpy as np
from scipy import io

from pacu.core.io.view.zero_dimension_array import ZeroDimensionArrayView

Dimension = namedtuple('Dimension', 'height, width')

class ScanboxInfoView(ZeroDimensionArrayView):
    def __init__(self, filename):
        array = io.loadmat(filename, squeeze_me=True).get('info')
        super(ScanboxInfoView, self).__init__(array)
    @property
    def nchan(self):
        return 2 if self.channels is 1 else 1
    @property
    def factor(self):
        return 1 if self.channels is 1 else 2
    @property
    def framerate(self):
        return self.resfreq / self.recordsPerBuffer
    @property
    def recordsPerBuffer(self):
        rpb = self._namedtuple.recordsPerBuffer
        return rpb * 2 if self.scanmode is 0 else rpb
    @property
    def sz(self):
        try:
            dimension = self._namedtuple.sz
        except:
            dimension = np.array([1000,  775], dtype=np.uint16)
        finally:
            return Dimension(*dimension)
    def __dir__(self): # quick and dirty: need to use descriptor set
        return super(ScanboxInfoView, self).__dir__() + \
            'nchan factor framerate recordsPerBuffer sz'.split()
