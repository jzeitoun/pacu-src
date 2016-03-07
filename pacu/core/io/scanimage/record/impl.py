import ujson

from pacu.util.path import Path
from pacu.util.prop.memoized import memoized_property
from pacu.core.io.scanimage.impl import ScanimageIO

class ScanimageRecord(object):
    """
    For `compatible_path`,
    the path should be formed like below. For example,
    '/Volumes/Data/Recordings/2P1/Dario/2015.11.20/x.151101.4/ref_p19_005.tif',
    This will be considered as,
    {whatever_basepath}/{experimenter}/{date}/{mousename}/{imagename}
    So the directory structure always will matter.
    """
    def __init__(self, compatible_path):
        self.tiff_path = Path(compatible_path).with_suffix('.tif')
        self.package_path = Path(compatible_path).with_suffix('.imported')
        self.mouse, self.date, self.user = self.tiff_path.parts[::-1][1:4]
    def toDict(self):
        return dict(
            user = self.user,
            mouse = self.mouse,
            date = self.date,
            name = self.tiff_path.stem,
            package = self.package
        )
    @memoized_property
    def package(self):
        return ScanimageIO(self.package_path)

def test():
    test_path = '/Volumes/Data/Recordings/2P1/Dario/2015.11.20/x.151101.4/ref_p19_005.tif'
    return ScanimageRecord(test_path)

# qwe = test()
