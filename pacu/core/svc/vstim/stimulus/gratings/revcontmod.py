from __future__ import division

from itertools import product

import numpy as np
from scipy import signal
from psychopy import core
from psychopy import misc
from psychopy import event
from psychopy.core import MonotonicClock

from pacu.ext.psychopy import logging
from pacu.util.prop.memoized import memoized_property
from pacu.core.svc.impl.exc import UserAbortException
from pacu.core.svc.impl.exc import ServiceRuntimeException
from pacu.core.svc.impl.resource import Resource
from pacu.core.svc.impl.component import Component
from pacu.core.svc.vstim.stimulus.base import StimulusBase
from pacu.core.svc.vstim.stimulus.orientation import Orientation
from pacu.core.svc.vstim.stimulus.sfrequency import SFrequency
from pacu.core.svc.vstim.stimulus.tfrequency import TFrequency
from pacu.core.svc.vstim.stimulus.width import Width
from pacu.core.svc.vstim.stimulus.duration import OnDuration
from pacu.core.svc.vstim.stimulus.contrast_cycle import ContrastCycle
from pacu.core.svc.vstim.stimulus.phase_cycle import PhaseCycle
from pacu.core.svc.vstim.stimulus.gratings.condition import RevContModCondition
from pacu.core.svc.vstim.stimulus.gratings.trial import Trial

# Reverse Contrast Modulating Stim

class StimulusResource(Resource):
    should_stop = False
    def __enter__(self):
        from psychopy.visual import GratingStim # eats some time
        from psychopy.visual import TextStim
        win = self.window.instance
        self.textstim = TextStim(win, text='')
        # for some reason x, y were swapped..
        #
        width, height = misc.pix2deg(win.size, win.monitor)
        if self.component.width:
            width = self.component.width
        self.instance = GratingStim(win=win, tex='sin',
            units='deg',
            size = (height, width)
            # size = misc.pix2deg(win.size, win.monitor)
        )
        print 'win size', win.size
        print 'mon size', win.monitor.getSizePix()
        print 'size as deg', misc.pix2deg(win.size, win.monitor)
        print 'size as deg * 2', misc.pix2deg(win.size, win.monitor) * 2
        try:
            self.interval = self.window.get_isi()
        except Exception as e:
            raise ServiceRuntimeException(
                'Could not acquire window object. Please try again')
        return self
    @memoized_property
    def trials(self):
        from psychopy.data import TrialHandler # eats some time
        conditions = [RevContModCondition(
            self.component.orientation,
            self.component.sfrequency,
            self.component.tfrequency,
        )]
        ts = [Trial(self, cond, self.component.on_duration, self.interval)
            for cond in conditions]
        return TrialHandler(ts,
            nReps=1, method='random')
    @property
    def synced(self):
        self.clock.synchronize(self)
        return iter(self)
    def __iter__(self):
        for trial in self.trials:
            index = self.trials.thisN
            logging.msg('Entering trial #%s...' % index)
            self.update_trial(trial)
            self.trials.addData('on_time', self.clock.getTime())
            yield trial.start()
            self.trials.addData('off_time', self.clock.getTime())
            self.flip_blank()
            # core.wait(self.component.off_duration)
            self.instance.opacity = 1.0
    def update_trial(self, trial):
        self.instance.ori = trial.condition.ori
        self.instance.sf = trial.condition.sf
        self.instance.tf = trial.condition.tf
    def update_phase(self, trial):
        if self.should_stop:
            logging.msg('UserAbortException raised!')
            raise UserAbortException()
        ctstate = (
            1 + np.cos(trial.frameCount/self.component.ct_cycle)
        ) / 2
        phstate = (
            signal.square(trial.frameCount/self.component.ph_cycle) / 4
        ) + 0.25
        self.instance.contrast = ctstate
        self.instance.phase = phstate
        self.instance.draw()
        self.window.flip()
    def flip_text(self, text):
        self.textstim.setText(text)
        self.textstim.draw()
        self.window.flip()
    def flip_blank(self):
        self.instance.opacity = 0.0
        self.instance.draw()
        self.window.flip()

class RevContModGratingsStimulus(Component):
    sui_icon = 'align justify'
    package = __package__
    orientation = 270 # Orientation(270)
    sfrequency = SFrequency(0.5)
    tfrequency = TFrequency(1)
    on_duration = OnDuration(30)
    ct_cycle = ContrastCycle(15)
    ph_cycle = PhaseCycle(6)
    width = Width(0)
    __call__ = StimulusResource.bind('window', 'clock', 'projection')
