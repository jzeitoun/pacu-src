__package__ = '' # cv2 unicode package name error

import cv2
import numpy as np

def main(workspace, condition, roi, datatag):
    frames = workspace.io.channel.mmap
    mask = np.zeros(frames.shape[1:], dtype='uint8')
    cv2.drawContours(mask, [roi.contours], 0, 255, -1)
    return np.stack(cv2.mean(frame, mask)[0] for frame in frames)

if __name__ == '__sbx_main__':
    datatag.value = main(workspace, condition, roi, datatag)
