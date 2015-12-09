from PIL import Image
from psychopy import core
from psychopy import misc

from pacu.ext.psychopy import logging
from pacu.util.prop.memoized import memoized_property
from pacu.core.svc.impl.resource import Resource
from pacu.core.svc.impl.component import Component
from pacu.core.svc.vstim.stimulus.duration import OnDuration
from pacu.core.svc.vstim.stimulus.tex_size import TexSize
from pacu.core.svc.vstim.stimulus.contrast import Contrast
from pacu.core.svc.vstim.stimulus.sfrequencies import SFrequencies
from pacu.core.svc.vstim.stimulus.tfrequencies import TFrequencies
from pacu.core.svc.vstim.stimulus.sweeping_noise.trial import Trial
from pacu.core.svc.vstim.stimulus.sweeping_noise.generator import SweepingNoiseGenerator


class StimulusResource(Resource):
    should_stop = False
    def __enter__(self):
        from psychopy.visual import TextStim
        from psychopy.visual import ImageStim # eats some time
        win = self.window.instance
        self.textstim = TextStim(win, text='')
        x, y = win.size
        afr = win.getActualFrameRate() * 0.5
        logging.msg('Actual frame rate: ' + str(afr))
        self.flip_text('Generating stimulus...it may take a few minutes.')
        mgen = SweepingNoiseGenerator(
            # spat_freq=self.component.sfrequencies[0],
            temp_freq=self.component.tfrequencies[0]
        )
        # from ipdb import set_trace
        # set_trace()
        self.movie = mgen.stim_to_movie(
            duration=self.component.on_duration,
            framerate=afr,
            imsize=self.component.tex_size,
            pixel_x=x,
            pixel_y=y,
            contrast = self.component.contrast
        )
        self.instance = ImageStim(
            win   = win,
            image = Image.new('L', (self.component.tex_size, self.component.tex_size)),
            units = 'pix',
            size  = win.size,
            # units = 'deg',
            # size  = misc.pix2deg(self.window.instance.size, self.window.monitor.instance)*2,
        )
        try:
            self.interval = self.window.get_isi()
        except Exception as e:
            raise ServiceRuntimeException(
                'Could not acquire window object. Please try again')
        return self
    @memoized_property
    def trials(self):
        from psychopy.data import TrialHandler # eats some time
        ts = [Trial(self, cond, self.component.on_duration, self.interval)
            for cond in [self.movie]]
        return TrialHandler(ts, nReps=1, method='random')
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
            # self.instance.opacity = 1.0
            # if self.should_stop:
            #     logging.msg('UserAbortException raised!')
            #     raise UserAbortException()
    def update_trial(self, trial):
        pass
    def update_phase(self, trial):
        pass
    def flip_text(self, text):
        self.textstim.setText(text)
        self.textstim.draw()
        self.window.flip()
    def flip_blank(self):
        self.instance.opacity = 0.0
        self.instance.draw()
        self.window.flip()
class SweepingNoiseStimulus(Component):
    sui_icon = 'share alternate'
    package = __package__
    on_duration = OnDuration(10)
    off_duration = 0
    tex_size = TexSize(128)
    contrast = Contrast(0.25)
    sfrequencies = SFrequencies([0.05])
    tfrequencies = TFrequencies([4.0])
    __call__ = StimulusResource.bind('window', 'clock')
