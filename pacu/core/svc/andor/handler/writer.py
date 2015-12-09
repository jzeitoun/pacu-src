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
ip1_datapath = Path('D:', 'data')

extratags = [('datetime', 'f', 1, 18.18, False)]

class WriterHandler(BaseHandler):
    def sync_name(self, member, filedir, filename):
        path = ip1_datapath.joinpath(member, filedir)
        if not path.is_dir():
            os.makedirs(path.str)
        self.tifpath = path.joinpath(filename).with_suffix('.tif')
        self.csvpath = path.joinpath(filename).with_suffix('.csv')
        return True # self.ready()
    def check(self, filename):
        pass
    def ready(self):
        if self.tifpath.is_file() or self.csvpath.is_file():
            raise Exception('Filename already exists. Please provide new one...')
        else:
            return True
    def enter(self):
        print 'enter'
        self.tif = TiffWriter(self.tifpath.str, bigtiff=True)
        self.csv = self.csvpath.open('w')
    def exposure_end(self, frame, ts):
        # rgba = pyplot.cm.jet(data, bytes=True)
        self.tif.save(frame, extratags=extratags)
        self.csv.write(u'{}\n'.format(ts))
    def exit(self):
        print 'exit'
        self.tif.close()
        self.csv.close()
