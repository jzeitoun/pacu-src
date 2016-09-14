__package__ = '' # unicode package name error

from pacu.core.io.scanbox.method.overall.tracer import ROITracer

def main(workspace, condition, roi, datatag):
    frames = condition.io.ch0.mmap
    tracer = ROITracer(roi, frames)
    main_trace = tracer.trace()
    if roi.neuropil_enabled:
        np_trace = tracer.neuropil_trace(workspace.other_rois(roi))
        main_trace -= np_trace * roi.neuropil_factor
    return main_trace

if __name__ == '__sbx_main__':
    datatag.value = main(workspace, condition, roi, datatag)