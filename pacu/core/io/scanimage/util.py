import numpy as np

def infer_nchannels(tiff):
    try:
        print 'Inferring how many channels there are...'
        maybe1 = tiff[0::2].mean()
        maybe2 = tiff[1::2].mean()
        print '`mean` of [0::2]', maybe1
        print '`mean` of [1::2]', maybe2
        nchan = 2 if  maybe1 / maybe2 < 0.75 else 1
        print 'I guess this stack has {} channel(s).'.format(nchan)
    except Exception as e:
        print 'Can not determine the number of channels.'
        print e
        return 0
    else:
        return nchan

def nan_for_json(dt):
    new = {}
    for key, val in dt.items():
        if isinstance(val, np.ndarray):
            new[key] = val
        elif np.isnan(val):
            new[key] = 'nan'
        else:
            new[key] = val
    return new
