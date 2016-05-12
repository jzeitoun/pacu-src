from sqlalchemy import Column, Integer, Unicode, ForeignKey
from sqlalchemy.orm import relationship

from pacu.core.io.scanbox.model.workspace import Workspace
from pacu.core.io.scanbox.model.roi import ROI
from pacu.core.io.scanbox.model.trace import Trace
from pacu.core.io.scanbox.model.action import Action

ROI.workspace_id = Column(Integer, ForeignKey(Workspace.id))
Workspace.rois = relationship(ROI, order_by=ROI.id, lazy='joined')
ROI.workspace = relationship(Workspace)
Trace.roi_id = Column(Integer, ForeignKey(ROI.id))
ROI.traces = relationship(Trace, order_by=Trace.id, lazy='joined')
Trace.roi = relationship(ROI)

__all__ = 'Workspace ROI Trace Action'.split()
