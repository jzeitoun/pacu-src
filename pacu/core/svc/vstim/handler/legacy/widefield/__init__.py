import ujson
from datetime import datetime

from pacu.ext.tornado.httputil.request import Request
from pacu.util.path import Path
from pacu.core.svc.vstim.handler.expv1 import ExpV1HandlerResource
from pacu.core.svc.vstim.handler.base import HandlerBase
from pacu.core.svc.impl.exc import ServiceException
from pacu.core.svc.vstim.handler.sync_host import SyncHost
from pacu.core.svc.vstim.handler.sync_port import SyncPort
from pacu.core.svc.vstim.handler.exp_by import ExpBy, people

def get(req, protocol):
    url = 'msg/svc.andor.on_external/'
    print url + protocol
    try:
        json = ujson.loads(req.get(url + protocol, timeout=5).body or '{}')
        print json
    except Exception as e:
        print e
        raise Exception('Communication error.')
    data = json.get('data')
    error = json.get('error')
    if error:
        raise Exception(str(error))
    return data

def make_datapath(member, now):
    filedir = '{d.month}.{d.day}.{y}'.format(d=now, y=str(now.year)[2:])
    filename = ('{d.year}{d.month:02}{d.day:02}T'
            '{d.hour:02}{d.minute:02}{d.second:02}').format(d=now)
    return '/'.join((member, filedir, filename))

ip1_condpath = Path('D:', 'DropBox', 'Data', 'Conditions', 'Intrinsic')

class LegacyWidefieldHandlerResource(ExpV1HandlerResource):
    def __enter__(self):
        host = self.component.sync_host
        port = self.component.sync_port
        self.member_name = people[self.component.exp_by]['name']
        self.req = Request.with_host_and_port(host, port)
        self.synchronize()
        return super(LegacyWidefieldHandlerResource, self).__enter__()
    def dump(self, result):
        print 'DUMP!'
        self.sync_close()
        print self.now
        print self.member_name
        return result
    def synchronize(self):
        self.sync_state()
        self.sync_metadata()
        self.sync_open()
    def sync_state(self):
        return get(self.req, 'state_check')
    def sync_metadata(self):
        self.now = datetime.now()
        path = make_datapath(self.member_name, self.now)
        return get(self.req, 'sync_metadata/{}'.format(path))
    def sync_open(self):
        return get(self.req, 'open')
    def sync_close(self):
        return get(self.req, 'close')

class LegacyWidefieldHandler(HandlerBase):
    sui_icon = 'database'
    package = __package__
    description = ("This handler is setup to comply the "
        "legacy widefield experiment environment that requires "
        "`tcim` and `PsychStimController`. This handler should be "
        "able to access a local machine's directory. "
        "(D/DropBox/Data/Conditions/...) It also does same thing "
        "for ExpV1 handler.")
    __call__ = LegacyWidefieldHandlerResource.bind('stimulus', 'result')
    sync_host = SyncHost('128.200.21.73')
    sync_port = SyncPort('8761')
    exp_by = ExpBy('kirstie')


# io.savemat('ad', dict(Duration=10, WaitInterval=1, snp_rotate=0))
#
# '04-Dec-2015'
#
# datetime.now().strftime(ff)
# '20151204T134822'
