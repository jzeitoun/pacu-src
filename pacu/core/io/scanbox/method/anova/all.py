__package__ = '' # unicode package name error

import numpy as np
from scipy import stats

def main(workspace, condition, roi, datatag):
#     blank = self.blank.meantrace if self.blank else []
#     flicker = self.flicker.meantrace if self.flicker else []
    all_oris = [
        [np.array(rep.value['on']).mean() for rep in reps]
        for sf, oris in roi.dt_ori_by_sf.items()
        for ori, reps in oris.items()
    ]
    print 'number of alll oris', len(all_oris)
    print 'do nothing...not implemented'
    return [[]]

    # if self.flicker and self.blank:
    #     f_reps = [ont.array.mean() for ont in self.flicker.ontimes]
    #     b_reps = [ont.array.mean() for ont in self.blank.ontimes]
    #     matrix = np.array([b_reps, f_reps] + all_oris).T
    #     f, p = stats.f_oneway(f_reps, b_reps, *all_oris)
    #     return util.nan_for_json(dict(f=f, p=p, matrix=matrix))
    # else:
    #     matrix = [[]]
    #     return util.nan_for_json(dict(matrix=matrix))

if __name__ == '__sbx_main__':
    datatag.value = main(workspace, condition, roi, datatag)

