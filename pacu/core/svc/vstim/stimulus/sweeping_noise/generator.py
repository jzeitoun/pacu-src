import tifffile
import numpy as np

class SweepingNoiseGenerator():
    def __init__(self, spat_freq=0.05, temp_freq=4):
        # maybe internal
        self.spat_freq = spat_freq
        self.temp_freq = temp_freq
        self.nyq_pix = .5
        self.contrast_period = 10
    def stim_to_movie(self,
            pixel_x=1024, pixel_y=768,
            duration=5, framerate=30,
            degX=80, imsize=64, contrast=0.25):
        # degX could be # misc.pix2deg(self.pixel_x, monitor)
        nframes=int(np.ceil(duration*framerate))
        # frameT=np.divide(range(nframes), framerate)??

        imageMag=np.floor(float(pixel_y)/imsize)
        degperpix=(degX/float(pixel_x))*imageMag

        # frequency intervals for FFT
        freqInt_pix=self.nyq_pix/(.5*imsize)
        nyq=framerate/2
        tempFreq_int=nyq/(.5*nframes)

        # Cutoffs in terms of frequency intervals
        tempCutoff = int(np.round(self.temp_freq/tempFreq_int))
        maxFreq_pix = self.spat_freq*degperpix
        spatCutoff = int(np.round(maxFreq_pix / freqInt_pix))

        # generate frequency spectrum (invFFT)
        alpha = -1
        offset = 3
        range_mult = 1

        # for noise that extends past cutoff parameter (i.e. if cutoff = 1sigma)
        spaceRange = np.array(
            range(
                imsize/2 - range_mult*spatCutoff-1,
                imsize/2 + range_mult*spatCutoff,
                1
            )
        ) + 1
        tempRange = np.array(
            range(
                nframes/2 - range_mult*tempCutoff-1,
                nframes/2 + range_mult*tempCutoff,
                1
            )
        ) + 1
        [x,y,z] = np.meshgrid(
            range(-range_mult*spatCutoff, range_mult*spatCutoff+1, 1),
            range(-range_mult*spatCutoff, range_mult*spatCutoff+1, 1),
            range(-range_mult*tempCutoff, range_mult*tempCutoff+1, 1)
        )

        # can put any other function to describe frequency spectrum in here,
        # e.g. gaussian spectrum
        # use = np.exp(-1*((0.5*x.^2/spatCutoff^2) + (0.5*y.^2/spatCutoff^2) + (0.5*z.^2/tempCutoff^2)));
        # use = np.single(((x.^2 + y.^2)<=(spatCutoff^2))& ((z.^2)<(tempCutoff^2)) );
        use = np.multiply(
            (
                ((x**2 + y**2) <= (spatCutoff**2)).astype(int)
                    &
                ((z**2) < (tempCutoff**2)).astype(int)
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
        fullspace = np.array(range(-range_mult*spatCutoff-1,range_mult*spatCutoff,1))
        halfspace = np.array(range(0,range_mult*spatCutoff,1))
        halftemp = np.array(range(0,range_mult*tempCutoff,1))

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
        immax = (imraw.std())/contrast
        immin = -1*immax
        imscaled = (imraw-immin-imraw.mean())/(immax-immin)

        # Create Gaussian filter
        sweepingbandwidth_control=5
        sigma = sweepingbandwidth_control/degperpix
        gauss_mask = np.array([
            1/(sigma * np.sqrt(2*np.pi)) * np.exp(-float(x)**2/(2*sigma**2))
            for x in range(-int(imsize/2),int(imsize/2))
        ])
        mask1 = np.tile(gauss_mask/gauss_mask.max(),[imsize,1])

        for f in range(1, nframes+1, 1):
            mask = np.roll(
                np.transpose(mask1),
                int(np.round(f*imsize/(self.contrast_period*framerate))),
                0
            )
            imscaled[:,:,f-1] = np.transpose(
                np.multiply((imscaled[:,:,f-1]-.5), np.transpose(mask))
            )
        moviedata = ((imscaled[0:imsize,0:imsize,:]+.5)*255)+1
        moviedata = np.uint8(np.floor(moviedata))
        moviedata = np.transpose(moviedata,(2,1,0))
        return moviedata
    def stim_to_file(self, **kwargs):
        movie = self.stim_to_movie(**kwargs)
        tifffile.imsave('gaussianNoise.tif', movie)

# SweepingNoiseGenerator().stim_to_file()
