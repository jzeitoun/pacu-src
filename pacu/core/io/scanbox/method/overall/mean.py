__package__ = '' # unicode package name error

from pacu.core.io.scanbox.method.overall.tracer import ROITracer

def main(workspace, condition, roi, datatag):
    frames = condition.io.ch0.mmap
    tracer = ROITracer(roi, frames)
    if roi.neuropil_enabled: # np goes first to get cache benefit because
                             # np has larger area than normal
        print 'NP enabled, NP first'
        np_trace = tracer.neuropil_trace(workspace.other_rois(roi))
        main_trace = tracer.trace()
        main_trace -= np_trace * roi.neuropil_factor
    else:
        main_trace = tracer.trace()
    return main_trace.tolist()

if __name__ == '__sbx_main__':
    datatag.value = main(workspace, condition, roi, datatag)
