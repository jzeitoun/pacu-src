__package__ = '' # unicode package name error

import cv2
import numpy as np

def main(workspace, condition, roi, datatag):
    on_duration = condition.on_duration
    off_duration = condition.off_duration

    n_panes = condition.info.get('focal_pane_args', {}).get('n', 1)
    pane_offset = workspace.cur_pane or 0

    framerate = condition.info['framerate'] # / n_panes # capture_frequency
    nframes = condition.info['nframes'] # / n_panes

    on_frames = int(framerate * on_duration)
    off_frames = int(framerate * off_duration)
    bs_frames = off_frames

    maybe_first_frame = int(datatag.trial_on_time*framerate)
    ff_remainder = maybe_first_frame % n_panes
    ff_comp = n_panes - ff_remainder

    if ff_remainder is not 0: # taking wrong offset
        print 'Trial #{} First frame compensation: {}, {:+}'.format(
            datatag.trial_order, maybe_first_frame, ff_comp)

    on_first_frame = maybe_first_frame + ff_comp
    on_last_frame = on_first_frame + on_frames

    # we can use last off period when we work with very first trial
    maybe_bs_first_frame = on_first_frame - off_frames
    bs_remainder = maybe_bs_first_frame % n_panes
    bs_comp = -bs_remainder

    if bs_remainder is not 0: # taking wrong offset, go backwards!
        print 'Trial #{} Baseline frame compensation: {}, {+}'.format(
            datatag.trial_order, maybe_bs_first_frame, bs_comp)

    baseline_first_frame = maybe_bs_first_frame + bs_comp
    baseline_last_frame = baseline_first_frame + off_frames

    if baseline_first_frame < 0:
        baseline_first_frame = 0
        baseline_last_frame = 0

    print ('\ntrial #{} @{}pane'
           '\nbase -> [{}:{}]'
           '\non   -> [{}:{}]').format(
            datatag.trial_order, pane_offset,
            baseline_first_frame, baseline_last_frame,
            on_first_frame, on_last_frame)

    trace = np.array(roi.dtoverallmean.value)
    on_trace = trace[on_first_frame:on_last_frame]
    baseline_trace = trace[baseline_first_frame:baseline_last_frame]

    maybe_later_part = int(workspace.baseline_duration * framerate)
    lp_remainder = maybe_later_part % n_panes
    lp_comp = n_panes - lp_remainder

    later_part = maybe_later_part + lp_comp
    later_baseline_trace = baseline_trace[-later_part:]

    f_0 = later_baseline_trace.mean()
    on_trace_f_0 = (on_trace - f_0) / f_0
    baseline_trace_f_0 = (baseline_trace - f_0) / f_0

    length_on = len(on_trace_f_0)
    if length_on != on_frames:
        print ('Trial #{} has ontime duration mismatch ({}/{}), '
                'fixed with NaNs').format(datatag.trial_order, length_on, on_frames)
        on_trace_f_0 = np.concatenate([on_trace_f_0,
            np.full(on_frames-length_on, np.nan)])

    length_bs = len(baseline_trace_f_0)
    if length_bs != bs_frames:
        print ('Trial #{} has offtime duration mismatch ({}/{}), '
                'fixed with NaNs').format(datatag.trial_order, length_bs, bs_frames)
        baseline_trace_f_0 = np.concatenate([baseline_trace_f_0,
            np.full(bs_frames-length_bs, np.nan)])

    return dict(on=on_trace_f_0.tolist(), baseline=baseline_trace_f_0.tolist())


if __name__ == '__sbx_main__':
    datatag.value = main(workspace, condition, roi, datatag)
