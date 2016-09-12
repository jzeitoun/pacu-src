__package__ = '' # unicode package name error

import cv2
import numpy as np

def main(workspace, condition, roi, datatag):
    on_duration = condition.on_duration
    off_duration = condition.off_duration
    framerate = condition.io.mat.framerate # capture_frequency
    nframes = condition.io.mat.nframes
    on_frames = int(framerate * on_duration)
    off_frames = int(framerate * off_duration)
    trial = datatag.trial

    on_first_frame = int(datatag.trial.on_time*framerate)
    on_last_frame = int(on_first_frame + on_frames)

    # we can use last off period when we work with very first trial
    baseline_first_frame = max(on_first_frame - off_frames, 0)
    baseline_last_frame = max(on_first_frame - 1, on_frames)

    off_first_frame = min(on_last_frame, nframes)
    off_last_frame = min(off_first_frame + off_frames, nframes)

    # print (baseline_first_frame, baseline_last_frame,
    #         on_first_frame, on_last_frame,
    #         off_first_frame, off_last_frame)

    trace = roi.overall_mean.value
    on_trace = trace[on_first_frame:on_last_frame]
    baseline_trace = trace[baseline_first_frame:baseline_last_frame]
    later_part = int(workspace.baseline_duration * framerate)
    later_baseline_trace = baseline_trace[-later_part:]

    f_0 = later_baseline_trace.mean()
    on_trace_f_0 = (on_trace - f_0) / f_0
    baseline_trace_f_0 = (baseline_trace - f_0) / f_0

    return dict(on=on_trace_f_0.tolist(), baseline=baseline_trace_f_0.tolist())


if __name__ == '__sbx_main__':
    datatag.value = main(workspace, condition, roi, datatag)

