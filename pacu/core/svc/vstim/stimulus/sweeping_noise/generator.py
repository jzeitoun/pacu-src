from __future__ import division
from scipy import signal
import numpy as np
# import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm

asd = np.array([
    0,  0,  0,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  3,  3,  3,  3,
    3,  4,  4,  4,  4,  4,  5,  5,  5,  5,  5,  6,  6,  6,  6,  6,  7,
    7,  7,  7,  7,  8,  8,  8,  8,  8,  9,  9,  9,  9,  9, 10, 10, 10,
    10, 10, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13,
    14, 14, 14, 14, 14, 15, 15, 15, 15, 15, 16, 16, 16, 16, 16, 17, 17,
    17, 17, 17, 18, 18, 18, 18, 18, 19, 19, 19, 19, 19, 20, 20, 20, 20,
    20, 21, 21, 21, 21, 21, 22, 22, 22, 22, 22, 23, 23, 23, 23, 23, 24,
    24, 24, 24, 24, 25, 25, 25, 25, 25, 26, 26, 26, 26, 26, 27, 27, 27,
    27, 27, 28, 28, 28, 28, 28, 29, 29, 29, 29, 29, 30, 30, 30, 30, 30,
    31, 31, 31, 31, 31, 32, 32, 32, 32, 32, 33, 33, 33, 33, 33, 34, 34,
    34, 34, 34, 35, 35, 35, 35, 35, 36, 36, 36, 36, 36, 37, 37, 37, 37,
    37, 38, 38, 38, 38, 38, 39, 39, 39, 39, 39, 40, 40, 40, 40, 40, 41,
    41, 41, 41, 41, 42, 42, 42, 42, 42, 43, 43, 43, 43, 43, 44, 44, 44,
    44, 44, 45, 45, 45, 45, 45, 46, 46, 46, 46, 46, 47, 47, 47, 47, 47,
    48, 48, 48, 48, 48, 49, 49, 49, 49, 49, 50, 50, 50, 50, 50, 51, 51,
    51, 51, 51, 52, 52, 52, 52, 52, 53, 53, 53, 53, 53, 54, 54, 54, 54,
    54, 55, 55, 55, 55, 55, 56, 56, 56, 56, 56, 57, 57, 57, 57, 57, 58,
    58, 58, 58, 58, 59, 59, 59, 59, 59, 60, 60])

# cdict = dict(
#     red = (
#         (0.0, 0.5, 0.5),
#         (1.0, 1.0, 1.0)
#     ),
#     green = (
#         (0.0, 0.5, 0.5),
#         (1.0, 1.0, 1.0)
#     ),
#     blue = (
#         (0.0, 0.5, 0.5),
#         (1.0, 1.0, 1.0)
#     )
# )
# my_cmap = colors.LinearSegmentedColormap('my_cmap', cdict)

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
            # if framerate is given a float, generator will take forever.
            # at #9 part
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
        print '\n======================init params========================'
        print 'max sfreq', self.max_spat_freq
        print 'max tfreq', self.max_temp_freq
        print 'contrast', self.contrast
        print 'rotation', self.rotation
        print 'duration', self.duration
        print 'bandwidth', self.bandwidth
        print 'Pixel X', self.pixel_x
        print 'Pixel Y', self.pixel_y
        print 'framerate', self.framerate
        print 'imsize', self.imsize
        print 'imageMag', self.imageMag
        print 'screen width cm ', self.screenWidthCm
        print 'screen dist cm', self.screenDistanceCm
        print 'nframes', int(np.ceil(self.duration*self.framerate))
        print '======================init params========================\n'
    def stim_to_movie(self):
        print '01/12'
        imsize = self.imsize
        movieMag = self.imageMag

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
        self.factor = self.contr_period * self.framerate
        self.offsets = (imsize * np.arange(nframes) / self.factor).round().astype(int)
        for frame, offset in zip(frames, self.offsets):
            frame[:] = (frame - 0.5) * np.roll(self.gauss2d, offset)

        print '12/12'
        self.moviedata = cm.gray(frames + 0.5, bytes=True)
        self.shape = self.moviedata.shape # z, y, x
        return self.moviedata
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
        import tifffile
        if self.moviedata is None:
            self.moviedata = self.stim_to_movie()
        tifffile.imsave('/Volumes/Users/ht/Desktop/gaussianNoise.tif', self.moviedata)
        # tifffile.imsave('gaussianNoise.tif', movie)
        return self

def tempsave(data):
    import tifffile
    tifffile.imsave('/Volumes/Users/ht/Desktop/gaussianNoise.tif', data)

qwe = SweepingNoiseGenerator().generate()
tempsave(qwe.moviedata)
# .stim_to_movie()
# SweepingNoiseGenerator().stim_to_file()
