import tifffile
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
        self.path = Path(filename)
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
    def io0(self):
        return np.memmap(self.data.file,
            dtype='uint16', mode='r', shape=self.shape, order='F'
        ).transpose(3, 1, 0, 2)[..., 0]
    @memoized_property
    def io1(self):
        return np.memmap(self.data.file,
            dtype='uint16', mode='r', shape=self.shape, order='F'
        ).transpose(3, 1, 0, 2)[..., 1]
    @memoized_property
    def ch0(self):
        x, y, c, z = self.shape
        return np.memmap(self.data.file, dtype='uint16', mode='r', order='F'
            )[0::self.info.nchan].reshape((z, y, x))
    @memoized_property
    def ch1(self):
        x, y, c, z = self.shape
        return np.memmap(self.data.file, dtype='uint16', mode='r', order='F'
            )[1::self.info.nchan].reshape((z, y, x))
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

# testpath = Path('/Volumes/Data/Recordings/scanbox-jack/Dario/test')
def conv(path, nchan=2):
    sbx = ScanboxIO(path)
    x, y, _, z = sbx.shape
    rgb = np.zeros((z, y, x, 3), dtype=sbx.io.dtype)
    if nchan == 2:
        rgb[..., 1] = ~sbx.ch0
        rgb[..., 0] = ~sbx.ch1
    elif nchan == 1:
        rgb[..., 1] = ~sbx.ch0
    tiffpath = sbx.path.with_name('tiff').mkdir_if_none()
    dest = tiffpath.joinpath(sbx.path.name).with_suffix('.tiff')
    tifffile.imsave(dest.str, rgb)
def conv_all(path, nchan=2, ls='*.sbx'):
    for sbxpath in Path(path).ls(ls):
        print 'converting...', sbxpath
        conv(sbxpath, nchan=nchan)

# testpath = Path('/Volumes/Data/Recordings/scanbox-jack/Dario/test2/test2_000_002')

def combine(tiffpath, dest, ls='*.tiff'):
    path = Path(tiffpath)
    # movie = np.concatenate([
    #     tifffile.imread(filename.str).mean(axis=0)[np.newaxis, ...]
    #     for filename in path.ls(ls)
    # ])
    movie = np.stack(
        tifffile.imread(filename.str).mean(axis=0)
        for filename in path.ls(ls)
    )
    tifffile.imsave(path.joinpath(dest).with_suffix('.tiff').str, movie)
    # consider using just stack instead of concatenate

def conv_comb(path, lspath='*', nchan=2):
    """
    path = '/media/Data/Recordings/scanbox-jack/Dario/Convert Please/Tox 3 D3'
    ls = 'D3_000_*'
    nchan = 2
    """
    path = Path(path)
    lspath = Path(lspath)
    print 'path', path
    print 'for', lspath
    tiffpath = path.joinpath('tiff')
    print 'conv all first'
    conv_all(path, nchan=nchan, ls=lspath.with_suffix('.sbx').str)
    print 'combine...'
    combine(tiffpath, '{}.mean.tiff'.format(lspath.str), ls=lspath.stem)


# from pacu.core.io.scanbox import impl as sbx

# testpath = Path('/Volumes/Users/ht/Desktop/test2/test2_000_001')
# s1 = ScanboxIO(testpath)
# testpath = Path('/Volumes/Users/ht/Desktop/test2/test2_000_002')
# s2 = ScanboxIO(testpath)
# get_ipython().magic('pylab')

# testpath = Path('/Volumes/Data/Recordings/scanbox-jack/Dario/tox3')
# conv_all(testpath, nchan=2, ls='Tox3_000_*.sbx')

# from pacu.util.path import Path
# from pacu.util.path import Path
#
#
# from pacu.core.io.scanbox import impl as sbx
# sbx.conv_all('/media/Data/Recordings/scanbox-jack/Dario/Tox3', nchan=2, ls='Tox3_000_*')
# sbx.conv_all('/media/Data/Recordings/scanbox-jack/Dario/Tox3', nchan=2, ls='Tox3_001_*')
# get_ipython().magic(u'ed ')
# combine('/media/Data/Recordings/scanbox-jack/Dario/Tox3/tiff', nchan='001.mean.tiff', ls='Tox3_001_*')
# combine('/media/Data/Recordings/scanbox-jack/Dario/Tox3/tiff', '001.mean.tiff', ls='Tox3_001_*')
# get_ipython().magic(u'ed -p')
# combine('/media/Data/Recordings/scanbox-jack/Dario/Tox3/tiff', '001.mean.tiff', ls='Tox3_001_*')
# get_ipython().magic(u'ed -p')
# combine('/media/Data/Recordings/scanbox-jack/Dario/Tox3/tiff', '001.mean.tiff', ls='Tox3_001_*')
# get_ipython().magic(u'ed -p')
# combine('/media/Data/Recordings/scanbox-jack/Dario/Tox3/tiff', '001.mean.tiff', ls='Tox3_001_*')
# combine('/media/Data/Recordings/scanbox-jack/Dario/Tox3/tiff', '000.mean.tiff', ls='Tox3_000_*')
# get_ipython().magic(u'ed 0-14')
