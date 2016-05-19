from sqlalchemy import Column, Integer, Unicode, ForeignKey
from sqlalchemy.orm import relationship

from pacu.core.io.scanbox.model.workspace import Workspace
from pacu.core.io.scanbox.model.roi import ROI
from pacu.core.io.scanbox.model.trace import Trace
from pacu.core.io.scanbox.model.colormap import Colormap
from pacu.core.io.scanbox.model.action import Action

Colormap.workspace_id = Column(Integer, ForeignKey(Workspace.id))
Colormap.workspace = relationship(Workspace)
ROI.workspace_id = Column(Integer, ForeignKey(Workspace.id))
ROI.workspace = relationship(Workspace)
ROI.traces = relationship(Trace, order_by=Trace.id, lazy='joined')
Trace.roi_id = Column(Integer, ForeignKey(ROI.id))
Trace.roi = relationship(ROI)
Workspace.colormaps = relationship(Colormap, order_by=Colormap.id, lazy='joined')
Workspace.rois = relationship(ROI, order_by=ROI.id, lazy='joined')

__all__ = 'Workspace ROI Colormap Trace Action'.split()
