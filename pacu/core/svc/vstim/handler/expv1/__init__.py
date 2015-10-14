from pacu.profile import manager
from pacu.core.model.experiment import ExperimentV1
from pacu.core.svc.vstim.handler.base import HandlerResource
from pacu.core.svc.vstim.handler.base import HandlerBase

class ExpV1HandlerResource(HandlerResource):
    DB = manager.get('db')
    def service_done(self, service):
        result = super(ExpV1HandlerResource, self).service_done(service)
        return self.dump(result)
    def dump(self, result): # to DB
        try:
            model = ExperimentV1(**result)
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
#     experiment_subject = StringSpec('', desc='Type to search mice...',
#         input_component='x-input-search',
#         input_option=dict(
#             query = 'mice',
#             fields = 'id sex name DOB'.split(),
#             path = 'name'
#         )
#     )
    __call__ = ExpV1HandlerResource.bind('stimulus', 'result')
