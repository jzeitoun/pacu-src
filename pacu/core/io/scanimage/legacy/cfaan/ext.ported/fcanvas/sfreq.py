import numpy as np
import matplotlib.gridspec as gridspec

from ext.console import debug
from ext.fcanvas import MPLCanvas
from parse_tuning import Response

class TuningCurveCanvas(MPLCanvas):
    def initialize(self):
        self.setWindowTitle('Spatial Frequency Tuning Curve')

        gs0, gs1 = gridspec.GridSpec(1, 2, width_ratios=[4, 1])
        self.ax1 = self.figure.add_subplot(gs0)
        self.ax2 = self.figure.add_subplot(gs1, sharey=self.ax1)
        self.ax1.hold(False)

        self.ax1.set_title('Spatial Frequency', fontsize=12)

        self.ax2.set_title('ETC', fontsize=12)
        self.ax1.tick_params(labelsize=10)

        self.ax1t = self.ax1.twinx()
        self.ax1t.grid(axis='y')
        self.ax1t.tick_params(labelsize=6)

        self.ax2t = self.ax2.twinx()
        self.ax2t.grid(axis='y')
        self.ax2t.tick_params(labelsize=6)

    def replot(self, sfx, sfy, blank, fff):

        self.ax1.plot(sfx, sfy, '-ok')
        self.ax1.set_xticks(sfx)
        self.ax2.clear()

        if blank is not None:
            self.ax2.scatter([0], [blank], color='k')
        if fff is not None:
            self.ax2.scatter([1], [fff], color='k')

        self.ax2.label_outer()
        self.ax2.set_xticks([-1, 0, 1, 2])
        self.ax2.set_xticklabels(['', 'B', 'F', ''])

        self.ax1t.set_ylim(self.ax1.get_ylim())
        self.ax1t.set_yticks(sfy)

        self.ax2t.set_ylim(self.ax1.get_ylim())
        self.ax2t.set_yticks(filter(None, [blank, fff]))

        self.draw()

    def updatePlot(self, trace, cond, meta):
        rmax_by_sfreq = Response.rmax_by_sfreq(trace, cond, meta)
        r = Response(trace, cond, meta)
        sfx, sfy = zip(*rmax_by_sfreq)
        blank = r.blank.meantrace.mean() if r.blank else None
        fff = r.flicker.meantrace.mean() if r.flicker else None
        self.replot(sfx, sfy, blank, fff)
