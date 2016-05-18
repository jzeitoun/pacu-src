from itertools import product

from psychopy import core
from psychopy import misc
from psychopy.core import MonotonicClock

from pacu.ext.psychopy import logging
from pacu.util.prop.memoized import memoized_property
from pacu.core.svc.impl.exc import UserAbortException
from pacu.core.svc.impl.exc import ServiceRuntimeException
from pacu.core.svc.impl.resource import Resource
from pacu.core.svc.impl.component import Component
from pacu.core.svc.vstim.stimulus.base import StimulusBase
from pacu.core.svc.vstim.stimulus.repetition import Repetition
from pacu.core.svc.vstim.stimulus.orientations import Orientations
from pacu.core.svc.vstim.stimulus.sfrequencies import SFrequencies
from pacu.core.svc.vstim.stimulus.tfrequencies import TFrequencies
from pacu.core.svc.vstim.stimulus.duration import OnDuration
from pacu.core.svc.vstim.stimulus.duration import OffDuration
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
        self.instance = GratingStim(win=win, units='deg', tex='sin',
            size = misc.pix2deg(win.size, win.monitor)*2)
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
            self.component.tfrequency
        )]
        ts = [Trial(self, cond, self.component.on_duration, self.interval)
            for cond in conditions]
        return TrialHandler(ts,
            nReps=self.component.repetition, method='random')
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
            core.wait(self.component.off_duration)
            self.instance.opacity = 1.0
            if self.should_stop:
                logging.msg('UserAbortException raised!')
                raise UserAbortException()
    def update_trial(self, trial):
        self.instance.ori = trial.condition.ori
        self.instance.sf = trial.condition.sf
        self.instance.tf = trial.condition.tf
    def update_phase(self, trial):
        print trial.frameCount
        self.instance.phase = trial.frameCount * trial.condition.tf
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
    repetition = 2
    orientation = 270
    sfrequency = 0.1
    tfrequency = 0.1
    on_duration = 1
    off_duration = 1
    __call__ = StimulusResource.bind('window', 'clock', 'projection')
