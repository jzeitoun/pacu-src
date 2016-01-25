import os

class ScanboxDataView(object):
    def __init__(self, path):
        self.path = path
        self.size = path.stat().st_size
        self.file = path.open('rb')
