import cv2
import numpy as np

class ROITracer(object):
    def __init__(self, roi, frames):
        self.roi = roi
        self.frames = frames
        self.shape = frames.shape[1:]
    def mask(self):
        mask = np.zeros(self.shape, dtype='uint8')
        cv2.drawContours(mask, [self.roi.contours], 0, 255, -1)
        return mask
    def neuropil_mask(self, others):
        mask = np.zeros(self.shape, dtype='uint8')
        cv2.drawContours(mask, [self.roi.neuropil_contours], 0, 255, -1)
        cv2.drawContours(mask, [self.roi.contours], 0, 0, -1)
        for other in others:
            cv2.drawContours(mask, [other.contours], 0, 0, -1)
        return mask
    def trace(self):
        mask = self.mask()
        return np.stack(cv2.mean(frame, mask)[0] for frame in self.frames)
    def neuropil_trace(self, others):
        mask = self.neuropil_mask(others)
        return np.stack(cv2.mean(frame, mask)[0] for frame in self.frames)
