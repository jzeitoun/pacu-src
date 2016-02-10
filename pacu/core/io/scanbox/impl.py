import numpy as np
from scipy import io

from pacu.util.path import Path
from pacu.util.prop.memoized import memoized_property
from pacu.core.io.scanbox.view.info import ScanboxInfoView
from pacu.core.io.scanbox.view.data import ScanboxDataView

max_uint16 = np.iinfo(np.uint16).max

class ScanboxIO(object):
    """
    # looking up availability
    availability = ScanboxIO.can_resolve('something')

    # opening file
    sbx = ScanboxIO('filename_without_suffix') # preferred way
    sbx = ScanboxIO('filename_with_suffix.mat') # also works
    sbx = ScanboxIO('filename_with_suffix.sbx') # also works

    # accessing metadata
    metadata_summary = list(sbx.info) # as list
    metadata_summary = sbx.info.items() # works as well but in dictionary

    # accessing frames
    # SUBTRACT the returned from max_uint16 to get the actual value
    # or apply `~` function to the frame
    first_frame = sbx[0]
    indexed_frame = sbx[10:20]
    entire_frame = list(sbx) # but you don't want to do this.
    """
    @classmethod
    def can_resolve(cls, filename):
        try   : cls.resolve_path(filename)
        except: return False
        else  : return True
    @classmethod
    def resolve_path(cls, filename):
        return {
            path.suffix: path.resolve()
            for path in Path(filename).with_suffixes('.mat', '.sbx')
        }
    def __init__(self, filename):
        pathz = ScanboxIO.resolve_path(filename)
        self.info = ScanboxInfoView(pathz.get('.mat'))
        self.data = ScanboxDataView(pathz.get('.sbx'))
    @property
    def nframes(self):
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
        return (self.info.sz.width, self.info.recordsPerBuffer, self.info.nchan, self.nframes)
    @memoized_property
    def io(self):
        return np.memmap(self.data.file,
            dtype='uint16', mode='r', shape=self.shape, order='F'
        ).transpose(3, 1, 0, 2)[..., 0]
    @memoized_property
    def io8bit(self):
        return self.io.view('uint8')[..., 1::2]
    def __getitem__(self, key):
        return self.io.__getitem__(key)

    # interface methods with i3d analysis
    @property
    def dimension(self):
        height, width = map(int, self.info.sz) # from numpy int
        return dict(width=width, height=height)
    @property
    def max_index(self):
        return self.nframes - 1
    def request_frame(self, index):
        return ~self.io8bit[index]
    def grand_trace(self):
        value = ~self.io
        return value.io.mean(axis=(1,2))
    def trace(self, x1, x2, y1, y2):
        return (~self.io[:, y1:y2, x1:x2]).mean(axis=(1,2))
