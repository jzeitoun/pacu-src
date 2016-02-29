import time
import calendar
from datetime import datetime
from datetime import timedelta

import numpy as np

from pacu.util.prop.memoized import memoized_property
from pacu.util.path import Path
from pacu.core.io.trajectory.log.position import Position
from pacu.core.io.trajectory.log import velocity

offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
offset = offset / 60 / 60
log_base_path = Path('/Volumes/Gandhi Lab - HT/Soyun/VR Logs')
log_paths = list(log_base_path.glob('*/*.csv'))

class TrajectoryLog(object):
    def __init__(self, path):
        self.path = path.with_suffix('.npy')
        self.datetime = datetime.strptime(path.stem, 'VR%Y%m%d%H%M%S')
        try:
            self.frame = np.rec.array(np.load(self.path.str))
        except Exception as e:
            self.frame = self.import_raw(path.with_suffix('.csv'))
    @classmethod
    def import_raw(cls, path): # csv
        filetime = datetime.strptime(path.stem, 'VR%Y%m%d%H%M%S')
        pos = np.rec.array(Position.from_lines(path.open()), names=Position._fields)
        velo = velocity.make(pos.ts, pos.x, pos.y)
        epochs = [
            (filetime + timedelta(hours=offset, seconds=delta) - datetime(1970, 1, 1)
        ).total_seconds() for delta in pos.ts]
        frame = np.rec.array(zip(*(
            epochs, pos.x, pos.y, pos.z, velo)
        ), names=['E', 'X', 'Y', 'Z', 'V'])
        np.save(path.with_suffix('.npy').str, frame)
        return frame
    @classmethod
    def query(cls, time):
        for path in reversed(sorted(log_paths)):
            logtime = datetime.strptime(path.stem, 'VR%Y%m%d%H%M%S')
            if logtime < time:
                return cls(path)

# test = Path('/Volumes/Users/ht/dev/ephemeral/vr/VR20160205104017.csv')
# q = TrajectoryLog.import_raw(test)
# q = TrajectoryLog(test)
# for lp in log_paths:
#     TrajectoryLog.import_raw(lp)

# example = datetime(2016, 02, 04, 14, 27, 00)
