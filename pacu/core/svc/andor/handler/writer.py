import re
import os

import numpy
from matplotlib import pyplot
from tifffile import TiffWriter

from pacu.util.path import Path
from pacu.core.svc.andor.handler.base import BaseHandler

re_filename = re.compile(r'^\w+$')
users_desktop = Path(os.path.expanduser('~'), 'Desktop')

class WriterHandler(BaseHandler):
    def check(self, filename):
        if not filename:
            return 'Filename should not be blank.'
        if not re_filename.match(filename):
            return 'Filename contains invalid character.'
        self.tiffpath = users_desktop.joinpath(filename).with_suffix('.tiff')
        self.metapath = users_desktop.joinpath(filename).with_suffix('.csv')
        if self.tiffpath.isfile() or self.metapath.isfile():
            return 'Filename already exists. Please provide new one...'
    def enter(self):
        print 'enter'
        self.tiff = TiffWriter(self.tiffpath.str, bigtiff=True)
        self.csv = self.metapath.open('w')
    def exposure_end(self, frame, ts):
        # rgba = pyplot.cm.jet(data, bytes=True)
        print '.',
        self.tiff.save(frame)
        self.csv.write(ts)
    def exit(self):
        print 'exit'
        self.tiff.close()
        self.csv.close()
