import os

import atexit
import time

from u3 import U3

# u3.configIO(TimerCounterPinOffset=4, NumberOfTimersEnabled=0,
#     EnableCounter0=False, EnableCounter1=False, FIOAnalog=0)
# atexit.register(u3.close)

# while 1:
#     print time.time(), 'FIO6:', u3.getFIOState(6)
#     time.sleep(0.1)

from pacu.util.path import Path
from pacu.core.svc.andor.handler.base import BaseHandler

class Chunk(object):
    tif = None
    csv = None
    is_rising = False
    def __init__(self, path, u3, did_refresh):
        self.path = path
        self.u3 = u3
        self.refresh() # to have initial chunk
        self.did_refresh = did_refresh
    def tick(self):
        is_rising = self.u3.getFIOState(6)
        if is_rising:
            self.refresh() # first
        self.is_rising = is_rising
    def save(self, frame):
        if self.is_rising:
            return
        self.tif.save(frame)
        self.csv.write(u'{}\n'.format(time.time()))
    def refresh(self):
        if self.is_rising:
            return
        self.close()
        self.nudge_path()
        self.open()
        self.did_refresh(self.tifpath)
    def open(self):
        self.tif = TiffWriter(self.tifpath.str, bigtiff=True)
        self.csv = self.csvpath.open('w')
    def nudge_path(self):
        self.tifpath = self.path.joinpath('{}.tif'.format(time.time()))
        self.csvpath = self.path.joinpath('{}.csv'.format(time.time()))
    def close(self):
        if self.tif:
            tif.close()
        if self.csv:
            csv.close()
        self.is_rising = False

class WriterByTTLHandler(BaseHandler):
    u3 = U3(debug=False, autoOpen=False)
    def check(self, dirname): # 1
        print 'WriterByTTLHandler check', dirname
        now = time.strftime('%Y-%m-%dT%H-%M-%S', time.localtime())
        self.path = Path(dirname, now)
        try:
            os.makedirs(self.path.str)
        except Exception as e:
            raise Exception('Failed creating a base directory: ' + str(e))
    def ready(self):
        print 'WriterByTTLHandler ready'
    def enter(self):
        print 'WriterByTTLHandler enter, chunk made'
        self.chunk = Chunk(self.path, self.u3, did_refresh=self.did_refresh)
    def exit(self):
        print 'WriterByTTLHandler exit'
        self.chunk.close()
        self.chunk = None
    def exposure_start(self):
        self.chucnk.tick()
    def exposure_end(self, frame, _ts):
        self.chunk.save(frame)
    def did_refresh(self, tifpath):
        print 'ONREF', tifpath.str
