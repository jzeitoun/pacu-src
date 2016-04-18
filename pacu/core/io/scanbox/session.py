from pacu.util.path import Path

class ScanboxSession(object):
    def __init__(self, path):
        self.path = Path(path).ensure_suffix('.session')
