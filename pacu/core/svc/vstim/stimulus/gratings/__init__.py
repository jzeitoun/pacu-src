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
from pacu.core.svc.vstim.stimulus.gratings.condition import Condition
from pacu.core.svc.vstim.stimulus.gratings.trial import Trial
from pacu.core.svc.vstim.stimulus.gratings.revcontmod import RevContModGratingsStimulus

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
        # blank if blank
        # flicker if flicker
        conditions = [Condition(ori, sf, tf) for ori, sf, tf in product(
            self.component.orientations,
            self.component.sfrequencies,
            self.component.tfrequencies,
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
        for key, val in vars(trial.condition).items():
            setattr(self.instance, key, val)
    def update_phase(self, trial):
        now = trial.tick()
        self.instance.phase = now * trial.condition.tf
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

class GratingsStimulus(Component):
    sui_icon = 'align justify'
    package = __package__
    repetition = Repetition(2)
    orientations = Orientations([0, 120, 240])
    sfrequencies = SFrequencies([0.01, 0.05, 0.1])
    tfrequencies = TFrequencies([1.0])
    on_duration = OnDuration(0.1)
    off_duration = OffDuration(0)
    __call__ = StimulusResource.bind('window', 'clock', 'projection')
