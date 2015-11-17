import atexit
import tifffile
import numpy as np
import matplotlib.pyplot as plt

from pacu.core.andor.ctypes.library import ctypes
from pacu.core.andor.ctypes.callback import c_feat_cb
from pacu.core.andor.instrument.zyla import ZylaInstrument
from pacu.core.andor.instrument.system import SystemInstrument
from pacu.core.andor.acquisition import helper
from pacu.core.andor.feature import test
from pacu.core.svc.andor.handler.bypass import BypassHandler
from pacu.core.svc.andor.handler.writer import WriterHandler

# non-streaming
# from u3 import U3, Counter0, Counter1
# u3 = U3(debug=False)
# u3.configIO(TimerCounterPinOffset=4, NumberOfTimersEnabled=0,
#     EnableCounter0=False, EnableCounter1=False, FIOAnalog=0)
# atexit.register(u3.close)
# counter0 = Counter0()
# counter1 = Counter1()
# def fire(pin=0):
#     u3.setFIOState(pin, 1)
#     u3.setFIOState(pin, 0)
# def cnt():
#     c1, c2 = u3.getFeedback(counter0, counter1)
#     print c1, c2

# qwe.exposure_time = 0.001 # 0.0001 makes fixed frame rate range
# qwe.metadata_enable = 1
#### qwe.trigger_mode = 1 # internal, just run
#### qwe.trigger_mode = 4 # software trigger, no run when continues cycle
#### qwe.trigger_mode = 2 # External Start, run when contnues
#### qwe.trigger_mode = 3 # External Exposure Triggering tick-wise granular
#### qwe.overlap = 0 # if 1, takes start end at once. if 0, take start and end sequentially
#### overlap also unwritable when triggermode is 4, software, 6,external
# qwe.trigger_mode = 6 # External, no wanting to control exposure time
# qwe.cycle_mode = 0 # 0 for fixed 1 for contigious
# qwe.frame_count = 100
# qwe.electronic_shuttering_mode = 1 # global
# qwe.aoi_height = 1024
# qwe.aoi_width = 1024
# rawbuf = qwe.acquisition.alloc_buffer()
# f = open('deleteme.bin', 'wb')

HANDLERS = dict(bypass=BypassHandler, writer=WriterHandler)
class AndorBindingService(object):
    frame_gathered = 0
    _current_frame = None
    inst = None
    handler = None
    # very rough and magic implementation.
    # no reason to be `files` argument.
    def __init__(self, files=-1):
        self.index = int(files)
    def __dnit__(self):
        print 'prepare to be destroyed...'
        if self.inst and self.inst.camera_acquiring:
            print 'stop acquiring...'
            self.stop_recording()
        try:
            print 'handle...',
            self.release_handle()
        except:
            print 'already released'
        else:
            print 'handle released'
    def acquire_handle(self):
        print 'Acquire camera handle...'
        # return True
        try:
            self.inst = SystemInstrument().acquire(ZylaInstrument, self.index)
        except Exception as e:
            raise Exception('Failed to acquire camera: ' + str(e))
        self.inst.aoi_height = 512
        self.inst.aoi_width = 512
        self.inst.accumulate_count = 1
        self.inst.frame_rate = 30.0
        self.inst.exposure_time = 0.01
        self.inst.cycle_mode = 1 # continuous
        self.inst.electronic_shuttering_mode = 1 # global
        self.inst.metadata_enable = 1
        self.inst.simple_preamp_gain_control = 2 # 16bit !important

        return True
    def release_handle(self):
        print 'Release camera handle...'
        # return None
        if self.inst and self.inst.camera_acquiring:
            raise Exception('Camera is in recording session. Stop first...')
        try:
            self.inst.release()
        except Exception as e:
            raise e
        else:
            self.inst = None
            self.handler = None
            return None
    @property
    def features(self):
        # return test.features
        try:
            return [self.inst.meta[key].export()
                for key in list(self.inst.feat)]
        except:
            return []
    def set_handler(self, clsname, *args):
        if self.inst and self.inst.camera_acquiring:
            raise Exception('Camera is in recording session. Stop first...')
        self.handler = HANDLERS.get(clsname)(self, *args)
    def set_features(self, kwargs):
        for key, val in kwargs.items():
            self.set_feature(key, val)
    def set_feature(self, key, val):
        try:
            # for f in test.features:
            #     if f['key'] == key:
            #         f['value'] = val
            # return
            getattr(self.inst.meta, key).coerce(val)
        except Exception as e:
            raise Exception('Failed to update value: ' + str(e))
    def start_recording(self):
        if self.handler:
            self.handler.ready()
        else:
            raise Exception('Handler has not been assigned.')
        if not self.inst:
            raise Exception('Could not find camera.')
        if self.inst.camera_acquiring:
            raise Exception('Camera is still in recording session.')
        self.handler.enter()
        self.handler.register()
        self.inst.acquisition()
        return True
    def stop_recording(self):
        if not self.handler:
            raise Exception('Handler has gone.')
        if not self.inst:
            raise Exception('Could not find camera.')
        if not self.inst.camera_acquiring:
            raise Exception('Camera is not in recording session.')
        self.inst.acquisition()
        self.handler.rollback()
        self.handler.exit()
        return None
    @property
    def current_frame(self):
        if self.handler._current_frame is not None:
            return plt.cm.gray(self.handler._current_frame.view('uint8')[1::2, ...], bytes=True).tostring()
