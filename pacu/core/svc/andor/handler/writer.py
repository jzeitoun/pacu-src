import re
import os

import numpy
from matplotlib import pyplot
from tifffile import TiffWriter

from pacu.util.path import Path
from pacu.core.svc.andor.handler.base import BaseHandler
from pacu.util.compat import str

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
    def ready(self):
        if self.tiffpath.is_file() or self.metapath.is_file():
            raise Exception('Filename already exists. Please provide new one...')
    def enter(self):
        print 'enter'
        self.tiff = TiffWriter(self.tiffpath.str, bigtiff=True)
        self.csv = self.metapath.open('w')
    def exposure_end(self, frame, ts):
        # rgba = pyplot.cm.jet(data, bytes=True)
        self.tiff.save(frame)
        self.csv.write(u'{}\n'.format(ts))
    def exit(self):
        print 'exit'
        self.tiff.close()
        self.csv.close()