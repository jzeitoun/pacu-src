import os
import inspect
import cPickle as pickle

from ..compat.pathlib import Path

def ls(self, glob='*'):
    return list(self.glob(glob))
def lsmodule(self, glob='*'):
    return [path.parent for path in self.glob('%s/__init__.py' % glob)]
def has_file(self, filename):
    return (self / filename).is_file()
def read(self, mode='r'):
    with self.open(mode) as f:
        return f.read()
def load_pickle(self):
    with self.open('rb') as f:
        return pickle.load(f)
def peak(self):
    try:
        return self.read()
    except:
        return ''
def write(self, content, mode='w'):
    with self.open(mode) as f:
        return f.write(content)
def here(cls, *paths):
    """
    Since it uses inspect module to access caller's frame,
    it should not be wrapped by any other functions.
    """
    cur = inspect.currentframe()
    out = inspect.getouterframes(cur)[1][0]
    path = os.path.dirname(os.path.abspath(
        inspect.getfile(out)
    ))
    return cls(path).joinpath(*paths)
def absdir(cls, path):
    return cls(os.path.dirname(os.path.abspath(path)))
def with_suffixes(self, *suffixes):
    return map(self.with_suffix, suffixes)
# def path_without_suffixes(self):
#     return Path(self.str[:-len(''.join(self.suffixes))])
def stempath(self):
    return Path(self.str[:-len(''.join(self.suffixes))])
    # return Path(self.stem)
def mkdir_if_none(self, mode=511, parents=True):
    if not self.is_dir():
        self.mkdir(mode=mode, parents=parents)
    return self

Path.__floordiv__ = Path.with_name
Path.str = property(Path.__str__)
Path.ls = ls
Path.lsmodule = lsmodule
Path.has_file = has_file
Path.read = read
Path.load_pickle = load_pickle
Path.peak = peak
Path.write = write
Path.here = classmethod(here)
Path.absdir = classmethod(absdir)
Path.with_suffixes = with_suffixes
# Path.path_without_suffixes = property(path_without_suffixes)
Path.stempath = property(stempath)
Path.mkdir_if_none = mkdir_if_none
