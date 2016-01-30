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
    on_refresh = False
    def __init__(self, path):
        self.path = path
        self.refresh() # to have initial chunk
    def save(self, frame):
        self.on_refresh = False
        self.tif.save(frame)
        self.csv.write(u'{}\n'.format(time.time()))
    def refresh(self):
        self.on_refresh = True
        self.close()
        # self.tif = TiffWriter(self.tifpath.str, bigtiff=True)
        # self.csv = self.csvpath.open('w')
    def close(self):
        if self.tif:
            tif.close()
        if self.csv:
            csv.close()

class WriterByTTLHandler(BaseHandler):
    u3 = U3(debug=False, autoOpen=False)
    def check(self, dirname): # 1
        print 'WriterByTTLHandler check', dirname
        now = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime())
        self.path = Path(dirname, now)
        try:
            os.makedirs(self.path.str)
        except Exception as e:
            raise Exception('Failed creating directory: ' + str(e))
    def ready(self):
        print 'WriterByTTLHandler ready'
    def enter(self):
        print 'WriterByTTLHandler enter'
        self.chunk = Chunk(self.path)
    def exit(self):
        print 'WriterByTTLHandler exit'
        self.chunk.close()
        self.chunk = None
    def exposure_start(self):
        if u3.getFIOState(6): # pulse rising
            print 'refresh'
            self.chucnk.refresh()
        # else: # falling
        #     if self.chunk.on_refresh:
        #         print 'start'
    def exposure_end(self, frame, _ts):
        self.chunk.save(frame)
