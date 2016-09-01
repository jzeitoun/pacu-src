from sqlalchemy import Column, Integer, Unicode, ForeignKey
from sqlalchemy.orm import relationship

from pacu.core.io.scanbox.model.workspace import Workspace
from pacu.core.io.scanbox.model.roi import ROI
from pacu.core.io.scanbox.model.datatag import Datatag
from pacu.core.io.scanbox.model.ephys_correlation import EphysCorrelation
from pacu.core.io.scanbox.model.colormap import Colormap
from pacu.core.io.scanbox.model.action import Action
from pacu.core.io.scanbox.model.condition import Condition
from pacu.core.io.scanbox.model.trial import Trial

class flist(list):
    @property
    def first(self):
        return self[0]
    @property
    def last(self):
        return self[-1]

EphysCorrelation.workspace_id = Column(Integer, ForeignKey(Workspace.id))
Colormap.workspace_id = Column(Integer, ForeignKey(Workspace.id))
ROI.workspace_id = Column(Integer, ForeignKey(Workspace.id))
Datatag.roi_id = Column(Integer, ForeignKey(ROI.id))
Datatag.trial_id = Column(Integer, ForeignKey(Trial.id))
Workspace.condition_id = Column(Integer, ForeignKey(Condition.id))
Trial.condition_id = Column(Integer, ForeignKey(Condition.id))

ROI.overall_mean = relationship(Datatag,
    primaryjoin=(ROI.id == Datatag.roi_id) & (Datatag.category == 'overall') & (Datatag.method == 'mean'),
    uselist=False,
    cascade='all, delete-orphan',
    lazy='joined')
ROI.datatags = relationship(Datatag, order_by=Datatag.id,
    collection_class=flist,
    cascade='all, delete-orphan',
    backref='roi',
    lazy='joined')
Trial.datatags = relationship(Datatag, order_by=Datatag.id,
    collection_class=flist,
    # cascade='all, delete-orphan',
    backref='trial',
    lazy='select') # select as a default
Workspace.colormaps = relationship(Colormap, order_by=Colormap.id,
    collection_class=flist,
    cascade='all, delete-orphan',
    backref='workspace',
    lazy='joined')
Workspace.rois = relationship(ROI, order_by=ROI.id,
    collection_class=flist,
    cascade='all, delete-orphan',
    backref='workspace',
    lazy='joined')
Workspace.ecorrs = relationship(EphysCorrelation, order_by=EphysCorrelation.id,
    collection_class=flist,
    cascade='all, delete-orphan',
    backref='workspace',
    lazy='joined')
Condition.workspaces = relationship(Workspace, order_by=Workspace.id,
    collection_class=flist,
    cascade='all, delete-orphan',
    backref='condition',
    lazy='joined')
Condition.trials = relationship(Trial, order_by=Trial.id,
    collection_class=flist,
    cascade='all, delete-orphan',
    backref='condition',
    lazy='joined')

__all__ = ('Workspace ROI Colormap Datatag '
           'EphysCorrelation Action Condition Trial').split()
