from PIL import Image
from psychopy import event
from psychopy.core import CountdownTimer
from pacu.core.svc.impl.exc import UserAbortException

from ipdb import set_trace

class Trial(object):
    def __init__(self, stimulus, condition, duration, interval):
        self.frameCount = 0
        self.stimulus = stimulus
        self.condition = condition
        self.interval = interval
        self.duration = duration
    def start(self):
        inst = self.stimulus.instance
        for frame in self.stimulus.movie:
            if event.getKeys('escape'):
                raise UserAbortException()
            self.interval.start()
            inst.image = Image.fromarray(frame)
            inst.draw()
            self.stimulus.window.flip()
            self.stimulus.clock.flipped()
            self.interval.complete()
        # self.getTime = CountdownTimer(self.duration).getTime
        return self
    def __nonzero__(self):
        return False
        # if event.getKeys('escape'):
        #     self.stimulus.should_stop = True
        # return self.getTime() > 0
    def __enter__(self):
        pass
        # self.interval.start()
        # self.stimulus.update_phase(self)
    def __exit__(self, *args):
        pass
        # self.interval.complete()
        # self.frameCount += 1
