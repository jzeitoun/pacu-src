import atexit
import time
import tifffile
import numpy as np

from pacu.util import logging
from pacu.core.andor.ctypes.library import ctypes
from pacu.core.andor.ctypes.callback import c_feat_cb
from pacu.core.andor.instrument.zyla import ZylaInstrument
from pacu.core.andor.instrument.system import SystemInstrument
from pacu.core.andor.acquisition import helper

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
# si = SystemInstrument()
# qwe = si.acquire(ZylaInstrument)
# frames = qwe.acquisition()
# frame = next(frames)
# frame = next(frames)
# frame = next(frames)

# context = 181818
# 
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





# frames = qwe.acquisition()

## # commented out
## # qwe.exposure_time = 0.005 # 0.0001 makes fixed frame rate range
## # qwe.frame_rate = 30
## # qwe.aoi_binning = 1
## # qwe.frame_count = 10 not writable when cyclemode is 1 (contigious)
## # cam = qwe.acquisition()
## # length = 512
## # print 'capturing', length
## # _, frames = zip(*[cam.capture() for i in range(length)])
## # print 'shaping'
## # stack = np.concatenate(frames).reshape(length, qwe.aoi_width, qwe.aoi_height)
## # print 'make tiff'
## # tifffile.imsave('a.tif', stack)
## # print 'done !'
## 
import itertools
import matplotlib.pyplot as plt
cms = itertools.cycle([plt.cm.gray, plt.cm.jet])

CONTEXTS = {}
import time

@c_feat_cb
def exposure_start(handle, feature, context):
    self = CONTEXTS[context]
    if not self.inst.camera_acquiring:
        return 0
    # print 's',
    self.inst.acquisition.queue_buffer(self.rawbuf)
    return 0
@c_feat_cb
def exposure_end(handle, feature, context):
    self = CONTEXTS[context]
    if not self.inst.camera_acquiring:
        return 0
    print '.',
    # print 'e',
    # st = time.time()
    # time.sleep(1)
    # f.write(rawbuf)
    buf = self.inst.acquisition.wait_buffer(3000, matching_buf=self.rawbuf)
    ts = self.inst.acquisition.extract_timestamp(self.rawbuf)
    frame, pointer = helper.get_contigious(self.inst.aoi_height, self.inst.aoi_width)
    self.inst.acquisition.convert_buffer(buf, pointer)
    self.currentFrame = frame
    # print 'conv latency', time.time() - st
    # print frame[:3]
    # tifffile.imsave('a.tiff', frame)
    return 0
@c_feat_cb
def buf_overflow(handle, feature, context):
    self = CONTEXTS[context]
    if not self.inst.camera_acquiring:
        return 0
    print 'buf overflowed. cancel everything'
    return 0


l = logging.get_default()

class AndorBindingService(object):
    currentFrame = None
    inst = None
    # very rough and magic implementation.
    # no reason to be `files` argument.
    def __init__(self, files=-1):
        print 'INIT with id', id(self)
        self.index = int(files)
    def raiseAfter1Sec(self):
        time.sleep(1)
        raise Exception('test raise!!!!!!!!')
    def return1(self):
        return 1
    def acquire(self):
        print 'ACQ'
        try:
            self.inst = SystemInstrument().acquire(ZylaInstrument, self.index)
            self.inst.aoi_height = 512
            self.inst.aoi_width = 512
            self.inst.accumulate_count = 1
            self.inst.frame_rate = 60
            self.inst.exposure_time = 0.01
            self.inst.cycle_mode = 1 # continuous
            self.inst.electronic_shuttering_mode = 1 # global
            self.inst.metadata_enable = 1


            # self.setup_feature_callback()
            return dict(error=None, detail=self.features)
        except Exception as e:
            return dict(error=True, detail='Fail: ' + str(e))
    def release(self):
        try:
            self.inst.release()
        except Exception as e:
            print 'exception raised within release.', type(e), e
        finally:
            self.inst = None
    @property
    def state(self):
        return bool(self.inst)
    @property
    def features(self):
        return [self.inst.meta[key].export()
                for key in list(self.inst.feat)]
    def set_feature(self, feature):
        try:
            print 'SET FEATURE'
            table = dict(IntMeta=int, EnumMeta=int, FloatMeta=float, BoolMeta=bool)
            origin = getattr(self.inst, feature['key'])
            key = feature['key']
            type = feature['type']
            marshalling = table.get(type, lambda x:x)
            value = feature['value']
            typed_value = marshalling(value)
            setattr(self.inst, key, typed_value)
            print '%s => %s' % (key, typed_value)
            return dict(error=False)
        except Exception as e:
            print str(e.__class__)
            print str(e)
            return dict(error=True, detail=str(e), value=origin)
    def get_faeture(self, feature_name):
        print 'GET FEATURE'
        print str(feature_name)
    def setup_feature_callback(self):
        @c_feat_cb
        def feat_changed(handle, feature, context):
            print '\n', 'CALLBACK: `{}` CHANGED!'.format(feature), context
            # print '\n', 'CALLBACK: `{}` => `{}`'.format(feature, cam.get(feature))
            return 0 # meaning callback handled successful.
        context = ctypes.cast(ctypes.byref(ctypes.c_int(id(self))), ctypes.c_void_p)
        for feat in map(unicode,
            'AOIWidth AOIHeight AOIBinning ReadoutTime ImageSizeBytes ExposureTime AOIStride FrameRate CameraAcquiring'.split()):
            self.inst.handle.core('RegisterFeatureCallback',
                feat,
                feat_changed,
                context
            )
    def getDebugOneFrame(self):
        # print 'GET debug frame backend'
        with self.inst.acquisition as frames:
            ts, frame = frames.capture()
        rgba = plt.cm.gray(frame.view('uint8')[1::2, ...], bytes=True).tostring()
        return rgba
    def getTiming(self, epoch):
        epoch = int(epoch)
        cur = time.time()
        print 'GET timing', epoch - cur
        print 'EPH', epoch, 'CUR', cur
    def getDebugFrame(self):
        print 'GET debug frame backend'
        # s = time.time()
        if self.currentFrame is not None:
            # return plt.cm.gray(self.currentFrame, bytes=True).tostring()
            # print 'GET RGBA...'
            # cm = next(cms)
            data = plt.cm.gray(self.currentFrame.view('uint8')[1::2, ...], bytes=True).tostring()
            # print time.time() - s, 'Elapsed...'
            return data
        else:
            return ''
    def getDebugStream(self):
        print 'stream mode needs cyclemode to be 1'
        print self.inst.image_size_bytes, 'SIZE'
        context = id(self)
        CONTEXTS[context] = self
        self.inst.event_selector = 0 #'ExposureStartEvent'
        self.inst.event_enable = 1
        self.inst.handle.core('RegisterFeatureCallback',
            u'ExposureStartEvent',
            exposure_start,
            context)
        self.inst.event_selector = 1 # 'ExposureEndEvent'
        self.inst.event_enable = 1
        self.inst.handle.core('RegisterFeatureCallback',
            u'ExposureEndEvent',
            exposure_end,
            context)
        self.inst.event_selector = 5 # 'BufferOverflowEvent'
        self.inst.event_enable = 1
        self.inst.handle.core('RegisterFeatureCallback',
            u'BufferOverflowEvent',
            buf_overflow,
            context)
        self.rawbuf = self.inst.acquisition.alloc_buffer()
        self.frames = self.inst.acquisition()
        return 'READY!'
    def delDebugStream(self):
        print 'stream mode release'
        context = id(self)

        self.inst.event_selector = 0 #'ExposureStartEvent'
        self.inst.event_enable = 0
        self.inst.handle.core('UnregisterFeatureCallback',
            u'ExposureStartEvent',
            exposure_start,
            context)
        self.inst.event_selector = 1 # 'ExposureEndEvent'
        self.inst.event_enable = 0
        self.inst.handle.core('UnregisterFeatureCallback',
            u'ExposureEndEvent',
            exposure_end,
            context)
        self.inst.event_selector = 5 # 'BufferOverflowEvent'
        self.inst.event_enable = 0
        self.inst.handle.core('UnregisterFeatureCallback',
            u'BufferOverflowEvent',
            buf_overflow,
            context)

        self.frames = self.inst.acquisition()
        self.rawbuf = None
        del CONTEXTS[context]
        print 'self.frames', self.frames
        return 'OK!'
    def getStreamFrame(self):
        ts, frame = self.frames.capture()
        rgba = plt.cm.gray(frame.view('uint8')[1::2, ...], bytes=True).tostring()
        print frame[0][:16]
        return rgba













