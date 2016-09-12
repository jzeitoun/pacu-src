from pacu.profile import manager
from pacu.core.model.experiment import ExperimentV1
from pacu.core.svc.vstim.handler.base import HandlerResource
from pacu.core.svc.vstim.handler.base import HandlerBase
from pacu.core.svc.vstim.handler.keyword import Keyword

class ExpV1HandlerResource(HandlerResource):
    DB = manager.get('db')
    def service_done(self, service):
        result = super(ExpV1HandlerResource, self).service_done(service)
        return self.dump(result)
    def dump(self, result): # to DB
        try:
            payload = result.pop('payload')
            model = ExperimentV1(**result)
            model.keyword = self.component.keyword
            model.duration = max(t for ts in model.off_time for t in ts)
            for key, val in payload.items():
                print key, val
                for attr in 'clsname pkgname kwargs'.split():
                    ett_attr = key + '_' + attr
                    ett_val = val.get(attr)
                    setattr(model, ett_attr, ett_val)
            session = self.DB.instance()
            session.add(model)
            session.commit()
        except Exception as e:
            print 'An exception from DB!', e
            result['error'] = str(e)
        else:
            result.update(id=model.id, created_at=model.created_at)
        return result

class ExpV1Handler(HandlerBase):
    sui_icon = 'database'
    package = __package__
    description = 'Scanbox users must provide correct information to take sbx recordings to analysis session.'
    __call__ = ExpV1HandlerResource.bind('stimulus', 'result')
    keyword = Keyword('')
