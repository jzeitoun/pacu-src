from pacu.core.andor.ctypes.callback import c_feat_cb
from weakref import WeakValueDictionary

CONTEXTS = WeakValueDictionary()

@c_feat_cb
def exposure_start(handle, feature, context):
    self = CONTEXTS[context]
    self.exposure_start()
    return 0
@c_feat_cb
def exposure_end(handle, feature, context):
    self = CONTEXTS[context]
    self.exposure_end()
    return 0
@c_feat_cb
def buf_overflow(handle, feature, context):
    self = CONTEXTS[context]
    self.buf_overflow()
    return 0

entry = [
    (0, u'ExposureStartEvent' , exposure_start),
    (1, u'ExposureEndEvent'   , exposure_end  ),
    (5, u'BufferOverflowEvent', buf_overflow  ),
]

class BaseHandler(object):
    rawbuf = None
    acquisition = None
    frame_gathered = 0
    def __init__(self, inst, *args):
        err = self.check(*args)
        if err:
            raise Exception(err)
        self.inst = inst
        self.context = id(self)
        CONTEXTS[self.context] = self
    def check(self, *args):
        return NotImplemented
    def _event_selecting(self, onoff):
        for selector, feature, callback in entry:
            self.inst.event_selector = selector
            self.inst.event_enable = onoff
            self.inst.handle.core('RegisterFeatureCallback',
                feature, callback, self.context)
    def register(self):
        self._event_selecting(1)
        self.rawbuf = self.inst.acquisition.alloc_buffer()
        self.acquisition = self.inst.acquisition()
    def rollback(self):
        self._event_selecting(0)
        self.rawbuf = None
        self.acquisition = None
    def ready(self):
        raise NotImplementedError
    def exposure_start(self):
        print 's'
    def exposure_end(self):
        print 'e'
    def buf_overflow(self):
        print 'o'
    def enter(self):
        pass
    def exit(self):
        pass
