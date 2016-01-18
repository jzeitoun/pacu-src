from pacu.core.svc.vstim.window.base.interval import Interval
from pacu.core.svc.impl.resource import Resource
from pacu.core.svc.impl.component import Component

class WindowResource(Resource):
    def __enter__(self):
        comp = self.component
        from psychopy.visual import Window # eats some time
        window = Window((comp.pixel_x, comp.pixel_y),
            useFBO = True,
            # units='deg',
            monitor = self.monitor.instance,
            allowStencil = True,
            fullscr = comp.fullscr)
        self.instance = window
        self.flip = window.flip
        return self
    def __exit__(self, type, value, tb):
        self.instance.close()
    def get_isi(self):
        return Interval(self.instance)

class WindowBase(Component):
    __call__ = WindowResource.bind('monitor')
