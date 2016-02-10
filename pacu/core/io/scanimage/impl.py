import tifffile

class ScanimageIO(object):
    def __init__(self, filename):
        pass
        # pathz = ScanboxIO.resolve_path(filename)
        # self.info = ScanboxInfoView(pathz.get('.mat'))
        # self.data = ScanboxDataView(pathz.get('.sbx'))
    # @dimension(self)
    # @max_index(self)
    # request_frame(self, index)
    # grand_trace(self)
    # trace(self, x1, x2, y1, y2)

test ='/Volumes/Gandhi Lab - HT/sci/2014.12.20/x.140801.1/field004.tif'
qwe = ScanimageIO(test)
