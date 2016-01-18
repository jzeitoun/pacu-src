import os

class ScanboxDataView(object):
    def __init__(self, sbxfile):
        self.name = sbxfile
        self.size = os.path.getsize(sbxfile)
        self.file = open(sbxfile, 'rb')
