from __future__ import division

import numpy as np
import scipy.ndimage.interpolation as i
from scipy.misc import imrotate
import tifffile

class SweepingNoiseGenerator():
    def __init__(self,
            max_spat_freq = 0.05,
            max_temp_freq = 4,
            contrast = 0.275,
            rotation = 0,
            duration = 10,
            bandwidth = 5,
            pixel_x = 1440,
            pixel_y = 900,
            framerate = 30,
            contr_period=10,
            imsize = 60,
            imageMag = 18, # movieMag
            screenWidthCm = 39.116, # for 15.4 inch MBPR 15
            screenDistanceCm = 25
        ):
        self.max_spat_freq = max_spat_freq
        self.max_temp_freq = max_temp_freq
        self.contrast = contrast
        self.rotation = rotation
        self.duration = duration
        self.bandwidth = bandwidth
        self.pixel_x = pixel_x
        self.pixel_y = pixel_y
        self.framerate = framerate
        self.contr_period = contr_period
        self.imsize = imsize
        self.imageMag = imageMag
        self.screenWidthCm = screenWidthCm
        self.screenDistanceCm = screenDistanceCm
    def stim_to_movie(self):
        imsize = self.imsize
        movieMag = self.imageMag
        print '======================parameters========================'
        print 'max sfreq', self.max_spat_freq
        print 'max tfreq', self.max_temp_freq
        print 'contrast', self.contrast
        print 'rotation', self.rotation
        print 'duration', self.duration
        print 'bandwidth', self.bandwidth
        print 'Pixel X', self.pixel_x,
        print 'Pixel Y', self.pixel_y,
        print 'framerate', self.framerate,
        print 'imsize', imsize,
        print 'imageMag', self.imageMag,
        print 'screen width cm ', self.screenWidthCm,
        print 'screen dist cm', self.screenDistanceCm,
        print '======================parameters========================'

        # degX could be # misc.pix2deg(self.pixel_x, monitor)
        nframes=int(np.ceil(self.duration*self.framerate))
        # frameT=np.divide(range(nframes), framerate)??

        # imageMag=np.floor(float(pixel_y)/imsize)
        # python way
        # degperpix=(degX/float(pixel_x))*imageMag
        # matalb way

        screenWidthDeg = 2*np.arctan(
            0.5*self.screenWidthCm/float(self.screenDistanceCm))*180/np.pi;
        degperpix = (screenWidthDeg/self.pixel_x)*self.imageMag;

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

        # Cutoffs in terms of frequency intervals
        tempCutoff = np.round(self.max_temp_freq/tempFreq_int)
        maxFreq_pix = self.max_spat_freq*degperpix
        spatCutoff = np.round(maxFreq_pix / freqInt_pix)

        # generate frequency spectrum (invFFT)
        alpha = -1
        offset = 3
        range_mult = 1

        # for noise that extends past cutoff parameter (i.e. if cutoff = 1sigma)

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

        invFFT = np.zeros([imsize,imsize,nframes],dtype=np.dtype('complex'))
        mu = np.zeros([spaceRange.shape[0], spaceRange.shape[0], tempRange.shape[0]])
        sig = np.ones([spaceRange.shape[0], spaceRange.shape[0], tempRange.shape[0]])


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

        imraw_comp = np.fft.ifftn(np.fft.ifftshift(invFFT))
        imraw = imraw_comp.real
        immax = (imraw.std())/self.contrast
        # print immax
        immin = -1*immax
        imscaled = (imraw-immin-imraw.mean())/(immax-immin)

        # Create Gaussian filter
        # sweepingbandwidth_control=5
        # sigma = sweepingbandwidth_control/degperpix

        sigma = self.bandwidth/degperpix/2 # we divided by 2 in order to
                                           # make compatible with the
                                           # calculation in PsychStimController.
                                           # I took off 2 again. should be correct.
                                           # added 2 for division again
        gauss_mask = np.array([
            1/(sigma * np.sqrt(2*np.pi)) * np.exp(-float(x)**2/(2*sigma**2))
            for x in np.arange(-(imsize/2),(imsize/2))
        ])
        mask1 = np.tile(gauss_mask/gauss_mask.max(),[imsize,1])
        # contr_period = 10
        for f in range(1, nframes+1, 1):
            mask = np.roll(
                np.transpose(mask1),
                int(np.round(f*imsize/(self.contr_period*self.framerate))),
                0
            )
            imscaled[:,:,f-1] = np.transpose(
                np.multiply((imscaled[:,:,f-1]-.5), np.transpose(mask))
            )
        moviedata = ((imscaled[0:imsize,0:imsize,:]+.5)*255)+1
        moviedata = np.uint8(np.floor(moviedata))
        moviedata = np.transpose(moviedata, (2,1,0))

        # setting viewport width is done from caller.

        self.shape = moviedata.shape # z, y, x
        print 'SHAPE', self.shape
        self.moviedata = moviedata
        return moviedata
    def generate(self):
        self.stim_to_movie()
        return self
    def rotate(self, direction=None):
        # 0 rotation= top to bottom (bar is going down)
        # 180 rotation= bottom to top (bar is going up)
        # 90 rotation= right to left
        # 270 rotation= left to right 
        arr = self.moviedata
        computed = {0:3, 1:2, 2:1, 3:0}.get(direction or self.rotation)
        for index, frame in enumerate(arr):
            arr[index] = np.rot90(frame, computed)
        return self
    def stim_to_file(self):
        if self.moviedata is None:
            self.moviedata = self.stim_to_movie()
        tifffile.imsave('/Volumes/Users/ht/Desktop/gaussianNoise.tif', self.moviedata)
        # tifffile.imsave('gaussianNoise.tif', movie)
        return self

def tempsave(data):
    tifffile.imsave('/Volumes/Users/ht/Desktop/gaussianNoise.tif', data)

# qwe = SweepingNoiseGenerator().generate().rotate(3)
# tempsave(qwe.moviedata)
# .stim_to_movie()
# SweepingNoiseGenerator().stim_to_file()
