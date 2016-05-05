from sqlalchemy import Column, Integer, Unicode, ForeignKey
from sqlalchemy.orm import relationship

from pacu.core.io.scanbox.model.workspace import Workspace
from pacu.core.io.scanbox.model.roi import ROI
from pacu.core.io.scanbox.model.trace import Trace

Workspace.rois = relationship('ROI', order_by='ROI.id', lazy='joined')
ROI.workspace_id = Column(Integer, ForeignKey('workspace.id'))
ROI.workspace = relationship('Workspace')
ROI.traces = relationship('Trace', order_by='Trace.id', lazy='joined')
Trace.roi_id = Column(Integer, ForeignKey('roi.id'))
Trace.roi = relationship('ROI')

__all__ = 'Workspace ROI Trace'.split()
