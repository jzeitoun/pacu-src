import importlib

import ujson

from ...ext.tornado import websocket

# currently web socket handler does not work in non-main thread
# thus shell mode does not support web socket in place.
class WSHandler(websocket.WebSocketHandler):
    """
    A Generic web socket handler.
      * `check_origin` returns always `True`.
    """
    url = r'/ws/(?P<modname>[\w\.]+)/(?P<clsname>\w+)'
    inst = None
    def open(self, modname, clsname):
        self.set_nodelay(True)
        # print 'OPEN', modname, clsname, self.get_argument('files')
        try:
            cls = getattr(importlib.import_module(modname), clsname)
        except ImportError as e:
            raise e
        except AttributeError as e:
            raise e
        kwargs = {key: val
            for key, vals in self.request.arguments.items()
            for val in vals}
        # print kwargs
        try:
            # print 'try bind websocket delegator'
            self.inst = cls(**kwargs)
        except Exception as e:
            print 'delegator init error', e
    def on_close(self):
        print 'CLOSE'
    def access(self, route):
        attrs = route.split('.')
        value = reduce(getattr, attrs, self.inst)
        return value
    def invoke(self, route, args=None, kwargs=None):
        func = self.access(route)
        return func(*args or [], **kwargs or {})
    def on_message(self, message):
        try:
            seq, ftype, route, payload = ujson.loads(message)
            as_binary = payload.pop('as_binary')
            # print 'ONMSG', seq, ftype, route, payload, '!!!!!!!!!!!!', as_binary
            func = getattr(self, ftype)
            rv = func(route, **payload)
        except AttributeError as e:
            print 'attrerror', e
            rv = 'ERROR!'+str(e) # should go for pure ws fetch?
        except ValueError as e:
            print 'invalid json', e
            rv = 'ERROR!'+str(e) # should go for pure ws fetch?
        except Exception as e:
            print 'invalid json', e
            rv = 'ERROR!'+str(e) # should go for pure ws fetch?
        if as_binary:
            self.write_message(rv, binary=True)
        else:
            try:
                dumped = ujson.dumps([seq, rv])
            except:
                dumped = ujson.dumps([seq, str(rv)])
            self.write_message(dumped)
