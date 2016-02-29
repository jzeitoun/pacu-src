"""
For make PACU backend compliant with JSONAPI. Ember will use it.
"""

import ujson

from pacu import profile
from pacu.core.model import Base
from pacu.ext.sqlalchemy.orm import session
from pacu.core.model.analysis import AnalysisV1
from pacu.api.model.http.custom import query as cquery

DB = profile.manager.get('db')

modelmap = dict(
    analyses=AnalysisV1
)

def get(req, model, id=None, **kwargs):
    if model == 'tr-sessions':
        return ujson.dumps(dict(data=cquery.trajectory_sessions(id)))
    session = DB.instance()
    Model = modelmap.get(model)
    query = session.query(Model).order_by(Model.id.desc())
    if id:
        data = query.get(id).serialize(type=model)
    else:
        data = [m.serialize(type=model) for m in query.all()]
    return ujson.dumps(dict(data=data))

def post(req, model, **kwargs):
    data = ujson.loads(req.body)['data']
    attr = data['attributes']
    type = data['type']
    model = modelmap.get(type)(**attr)
    session = DB.instance()
    session.add(model)
    try:
        session.commit()
    except Exception as e:
        print e.__class__, e
        raise e
    else:
        data = model.serialize(type)
        return ujson.dumps(dict(data=data))
