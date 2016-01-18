from __future__ import division

import numpy as np
from scipy import integrate
from scipy import signal
# import matplotlib.pyplot as plt
from psychopy import misc
import matplotlib.colors as colors
import matplotlib.cm as cm
from ipdb import set_trace

class SweepingNoiseGenerator():
    def __init__(self,
            max_spat_freq = 0.05,
            max_temp_freq = 4,
            contrast = 0.275,
            rotation = 0,
            duration = 300,
            bandwidth = 5,
            viewwidth = 0,
            pixel_x = 1440,
            pixel_y = 900,
            # if framerate is given a float, generator will take forever.
            framerate = 30,
            contr_period=10,
            # imsize = 128,
            imageMag = 10, # movieMag
            screenWidthCm = 39.116, # for 15.4 inch MBPR 15
            screenDistanceCm = 25,
            # screenRatio = 0.625,
            eyepoint_x = 0.5
        ):
        self.max_spat_freq = max_spat_freq
        self.max_temp_freq = max_temp_freq
        self.contrast = contrast
        self.rotation = rotation
        self.duration = duration
        self.bandwidth = bandwidth
        self.viewwidth = viewwidth
        self.pixel_x = pixel_x
        self.pixel_y = pixel_y
        # self.screenRatio = screenRatio
        self.framerate = framerate
        self.contr_period = contr_period
        # self.imsize = imsize
        self.imageMag = imageMag
        self.screenWidthCm = screenWidthCm
        self.screenDistanceCm = screenDistanceCm
        # self.screenRatio = screenRatio
        self.eyepoint_x = eyepoint_x
        print '\n======================init params========================'
        print 'max sfreq', self.max_spat_freq
        print 'max tfreq', self.max_temp_freq
        print 'contrast', self.contrast
        print 'rotation', self.rotation
        print 'duration', self.duration
        print 'bandwidth', self.bandwidth
        print 'viewwidth', self.viewwidth
        print 'Pixel X', self.pixel_x
        print 'Pixel Y', self.pixel_y
        print 'framerate', self.framerate
        # print 'imsize', self.imsize
        print 'imageMag', self.imageMag
        print 'screen width cm ', self.screenWidthCm
        print 'screen dist cm', self.screenDistanceCm
        # print 'screen ratiom', self.screenRatio
        print 'eyepoint_x', self.eyepoint_x
        print 'nframes', int(np.ceil(self.duration*self.framerate))
        print '======================init params========================\n'
    def stim_to_movie(self):
        print '01/12'
        self.imsize = imsize = self.pixel_x / self.imageMag
        # imsize = self.imsize

        # degX could be # misc.pix2deg(self.pixel_x, monitor)
        nframes = int(np.ceil(self.duration*self.framerate))

        # this is how many frames before the stimulus to repeat
        frames_per_period = int(np.ceil(self.contr_period*self.framerate))

        # frameT=np.divide(range(nframes), framerate)??

        # imageMag=np.floor(float(pixel_y)/imsize)
        # python way
        # degperpix=(degX/float(pixel_x))*imageMag
        # matalb way

        screenWidthDeg = 2*np.arctan(
            0.5*self.screenWidthCm/float(self.screenDistanceCm))*180/np.pi
        self.full_width = screenWidthDeg
        degperpix = (screenWidthDeg/self.pixel_x)*self.imageMag

        print '02/12'
        # frequency intervals for FFT
        # in python way
        # nyq_pix = .5
        # freqInt_pix=nyq_pix/(.5*imsize)
        # nyq=self.framerate/2
        # tempFreq_int=nyq/(.5*nframes)

        # frequency intervals for FFT
        # in matlab way
        nyq_pix = 0.5
        nyq_deg=nyq_pix/degperpix
        freqInt_deg = nyq_deg / (0.5*imsize)
        freqInt_pix = nyq_pix / (0.5*imsize)
        nyq = self.framerate/2.0
        tempFreq_int = nyq/(0.5*nframes)

        print '03/12'
        # Cutoffs in terms of frequency intervals
        tempCutoff = np.round(self.max_temp_freq/tempFreq_int)
        maxFreq_pix = self.max_spat_freq*degperpix
        spatCutoff = np.round(maxFreq_pix / freqInt_pix)

        # generate frequency spectrum (invFFT)
        alpha = -1
        offset = 3
        range_mult = 1

        # for noise that extends past cutoff parameter (i.e. if cutoff = 1sigma)

        print '04/12'
        spaceRange = np.arange(
                imsize/2 - range_mult*spatCutoff-1,
                imsize/2 + range_mult*spatCutoff,
                1
        ) + 1
        tempRange = np.arange(
                nframes/2 - range_mult*tempCutoff-1,
                nframes/2 + range_mult*tempCutoff,
                1
        ) + 1
        [x,y,z] = np.meshgrid(
            np.arange(-range_mult*spatCutoff, range_mult*spatCutoff+1, 1),
            np.arange(-range_mult*spatCutoff, range_mult*spatCutoff+1, 1),
            np.arange(-range_mult*tempCutoff, range_mult*tempCutoff+1, 1)
        )

        print '05/12'
        # can put any other function to describe frequency spectrum in here,
        # e.g. gaussian spectrum
        # use = np.exp(-1*((0.5*x.^2/spatCutoff^2) + (0.5*y.^2/spatCutoff^2) + (0.5*z.^2/tempCutoff^2)));
        # use = np.single(((x.^2 + y.^2)<=(spatCutoff^2))& ((z.^2)<(tempCutoff^2)) );
        use = np.multiply(
            (
                ((x**2 + y**2) <= (spatCutoff**2))
                    &
                ((z**2) < (tempCutoff**2))
            ),
            (
                np.sqrt(np.add(x**2 + y**2, offset))**alpha
            )
        )
        print '06/12'

        invFFT = np.zeros([imsize,imsize,nframes],dtype=np.dtype('complex'))
        mu = np.zeros([spaceRange.shape[0], spaceRange.shape[0], tempRange.shape[0]])
        sig = np.ones([spaceRange.shape[0], spaceRange.shape[0], tempRange.shape[0]])


        print '07/12'
        complex_num = 0+1j
        mult1 = use*np.random.normal(mu,sig)
        mult2 = np.exp(2*np.pi*complex_num*np.random.random_sample([int(spaceRange.size),int(spaceRange.size),int(tempRange.size)]))
        invFFT[spaceRange[0]:spaceRange[-1]+1,spaceRange[0]:spaceRange[-1]+1,tempRange[0]:tempRange[-1]+1]=np.multiply(mult1,mult2)

        # in order to get real values for image, need to make spectrum symmetric
        fullspace = np.arange(-range_mult*spatCutoff-1,range_mult*spatCutoff,1)
        halfspace = np.arange(0,range_mult*spatCutoff,1)
        halftemp = np.arange(0,range_mult*tempCutoff,1)

        fullspace_add = imsize/2 + fullspace+1
        fullspace_sub = imsize/2 - fullspace+1
        halfspace_add = imsize/2 + halfspace+1
        halfspace_sub = imsize/2 - halfspace+1
        halftemp_add = np.round(nframes/2) + halftemp+1
        halftemp_sub = np.round(nframes/2) - halftemp+1

        print '08/12'
        invFFT[
            fullspace_add[0]:fullspace_add[-1]+1,
            fullspace_add[0]:fullspace_add[-1]+1,
            halftemp_add[0]:halftemp_add[-1]+1
        ] = np.conjugate(invFFT[
                fullspace_sub[-1]:fullspace_sub[0]+1,
                fullspace_sub[-1]:fullspace_sub[0]+1,
                halftemp_sub[-1]:halftemp_sub[0]+1])
        invFFT[
            fullspace_add[0]:fullspace_add[-1]+1,
            halfspace_add[0]:halfspace_add[-1]+1,
            nframes/2+1
        ] = np.conjugate(invFFT[
                fullspace_sub[-1]:fullspace_sub[0]+1,
                halfspace_sub[-1]:halfspace_sub[0]+1,
                nframes/2+1])
        invFFT[
            halfspace_add[0]:halfspace_add[-1]+1,
            imsize/2+1,
            nframes/2+1
        ] = np.conjugate(invFFT[
                halfspace_sub[-1]:halfspace_sub[0]+1,
                imsize/2+1,
                nframes/2+1])

        print '09/12'
        print '\t1/5'
        imraw_comp = np.fft.ifftn(np.fft.ifftshift(invFFT))
        print '\t2/5'
        imraw = imraw_comp.real
        print '\t3/5'
        immax = (imraw.std())/self.contrast
        print '\t4/5'
        immin = -1*immax
        print '\t5/5'
        imscaled = (imraw-immin-imraw.mean())/(immax-immin)

        # Create Gaussian filter
        print '10/12'
        frames = imscaled.transpose(2, 1, 0) # conventional shaping
        sigma = self.bandwidth/degperpix/2 # we divided by 2 in order to
                                           # make compatible with the
                                           # calculation in PsychStimController.
                                           # I took off 2 again. should be correct.
                                           # added 2 for division again
        self.gauss1d = signal.gaussian(imsize, sigma, sym=True)
        self.gauss2d = np.tile(self.gauss1d, (imsize, 1)) # Make it 2D
        # No need to have something like `gauss3d`. It is just overkill.

        print '11/12'

        # defines a period

        screenWidthDegEyePoint = np.arctan(
            (self.screenWidthCm * (1 - self.eyepoint_x)) / self.screenDistanceCm
        ) + np.arctan((self.screenWidthCm * self.eyepoint_x) / self.screenDistanceCm)

        # set_trace()

        self.theta = screenWidthDegEyePoint / frames_per_period
        self.space = np.linspace(0, nframes*self.theta, nframes)
        # self.thetas = self.space % screenWidthDegEyePoint
        self.thetas = np.fmod(self.space, screenWidthDegEyePoint) - (screenWidthDegEyePoint * (1 - self.eyepoint_x))
        # self.thetas = np.fmod(self.space, 0.5*screenWidthDegEyePoint) - (screenWidthDegEyePoint * (1 - self.eyepoint_x))
        self.offsets = (imsize * self.screenDistanceCm * np.tan(self.thetas) / self.screenWidthCm) - imsize / 2
        # self.offsets = (imsize * self.screenDistanceCm * np.tan(self.thetas) / self.screenWidthCm) - 3*imsize / 4

        for theta, frame, offset in zip(self.thetas, frames, self.offsets):
            frame[:] = (frame - 0.5) * np.roll(self.gauss2d, int(offset))

        # last_offset = (nframes * ((2 * np.pi) / screenWidthDeg)) / np.pi
        # off = np.cos(np.linspace(0, last_offset, nframes)) # 1 ~ -1
        # off_scaled = ((off + 1) / 2) + 0.5 # 1.5 ~ 0.5

        # self.factor = self.contr_period * self.framerate
        # self.offsets = (off_scaled * imsize * np.arange(nframes) / self.factor).round().astype(int)
        # for frame, offset in zip(frames, self.offsets):
        #     frame[:] = (frame - 0.5) * np.roll(self.gauss2d, offset)

        print '12/12'
        self.moviedata = cm.gray(frames + 0.5, bytes=True)
        self.shape = self.moviedata.shape # z, y, x
        return self.moviedata
    def viewmask(self):
        if not self.viewwidth:
            return
        ratio = ((self.full_width - self.viewwidth) / self.full_width * 100) / 2
        boundindex =  self.moviedata.shape[2] * (ratio/100)
        self.moviedata[:, :, -boundindex:] = 128
        self.moviedata[:, :, :boundindex] = 128
        return self
    def generate(self):
        self.stim_to_movie()
        return self
#     def crop(self):
#         amount = self.imsize - int(self.imsize*self.screenRatio)
#         if self.rotation in [0, 2]:
#             self.moviedata = self.moviedata[:, :, amount:]
#         else:
#             self.moviedata = self.moviedata[:, amount:, :]
#         return self
    def rotate(self, direction=None):
        #   0: top to bottom
        # 180: bottom to top
        #  90: right to left
        # 270: left to right
        arr = self.moviedata
        computed = {0:3, 1:2, 2:1, 3:0}.get(direction or self.rotation)
        for index, frame in enumerate(arr):
            arr[index] = np.rot90(frame, computed)
        return self
    def stim_to_file(self):
        import tifffile
        if self.moviedata is None:
            self.moviedata = self.stim_to_movie()
        tifffile.imsave('/Volumes/Users/ht/Desktop/gaussianNoise.tif', self.moviedata)
        # tifffile.imsave('gaussianNoise.tif', movie)
        return self

def tempsave(data):
    import tifffile
    tifffile.imsave('/Volumes/Users/ht/Desktop/gaussianNoise.tif', data)

# qwe = SweepingNoiseGenerator(duration=10, eyepoint_x=0.5, screenDistanceCm=20)
# qwe.generate()
# qwe.rotate()
# qwe.viewmask()
# qwe.crop()
# tempsave(qwe.moviedata)

# .stim_to_movie()
# SweepingNoiseGenerator().stim_to_file()
