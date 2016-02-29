import time
import struct
from collections import namedtuple

import numpy as np
import tifffile

from pacu.util.path import Path
from pacu.api.model.http.custom import query
from pacu.util.prop.memoized import memoized_property
from pacu.core.io.trajectory.trial import TrajectoryTrial

gene = '8s3I'
suffixes = '.mmap.npy', '.meta.bin', '.stat.npy', '.time.npy', '.imported'

class TrajectorySession(object):
    @classmethod
    def import_raw_by_id(cls, id):
        session_path = query.get_session_path(int(id))
        print 'Locate session directory: ' + session_path.str
        stems = [path.with_name(path.stem) for path in session_path.ls('*.tif')]
        for stem in stems:
            cls.import_raw(stem)
        print 'Import complete!'
    @classmethod
    def import_raw(cls, path):
        print 'Import trial: ', path
        mmappath, metapath, statpath, timepath, imptpath = [
            Path(path.str + suf) for suf in suffixes]
        if imptpath.is_file():
            print 'Already imported...skip!'
            return
        tiffpath = path.str + '.tif'
        file_size = Path(tiffpath).lstat().st_size
        print '\tLoad tiff stack...({:,} bytes)'.format(file_size)
        tiff = tifffile.imread(tiffpath)
        print '\tLoad timestamp...({} frames)'.format(tiff.shape[0])
        tss = np.fromfile(path.str + '.csv', sep='\n', dtype='float32')
        print '\tGenerate basic information...'
        record = struct.pack(gene, tiff.dtype.name, *tiff.shape)
        print '\tmax...'
        max = tiff.max(axis=(1,2))
        print '\tmin...'
        min = tiff.min(axis=(1,2))
        print '\tmean...'
        mean = tiff.mean(axis=(1,2))
        rec = np.rec.fromarrays([max, min, mean], names='MAX, MIN, MEAN')
        print '\tOpening memory mapped IO...'
        mmap = np.memmap(mmappath.str,
            mode='w+', dtype=tiff.dtype, shape=tiff.shape)
        print '\tWriting to disk...'
        mmap[:] = tiff[:]
        metapath.write(record, mode='wb')
        np.save(statpath.str, rec)
        np.save(timepath.str, tss)
        imptpath.write(u'', 'w')
        print '\tDone!'
    def __init__(self, path):
        self.path = Path(path).resolve()
    @memoized_property
    def trials(self):
        return [
            TrajectoryTrial(path.with_name(path.stem))
            for path in sorted(self.path.ls('*.imported'))]
    def get_trial(self, id):
        path = sorted(self.path.ls('*.imported'))[id]
        return TrajectoryTrial(path.with_name(path.stem))

def get_trial_index(id):
    path = query.get_session_path(int(id))
    return [(index, trial.path.name)
        for index, trial in enumerate(TrajectorySession(path).trials)]

def TrajectoryTrialFetcher(files=-1):
    session_id, trial_id = map(int, files.split(','))
    path = query.get_session_path(session_id)
    return TrajectorySession(path).get_trial(trial_id)

# test = '/Volumes/Gandhi Lab - HT/Soyun/2016-02-04T14-27-00'
# qwe = TrajectorySession.import_raw_by_id(1)
# qwe = TrajectorySession(test)
