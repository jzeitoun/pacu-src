import sys

import importlib
import traceback

import struct
import numpy as np
import ujson

from ...ext.tornado import websocket

def handle_exc(e):
    info = sys.exc_info()
    source = traceback.format_exception(*info)
    print '\n======== exception on websocket delegation ========'
    traceback.print_exception(*info)
    print '======== exception on websocket delegation ========\n'
    raise e

# currently web socket handler does not work in non-main thread
# thus shell mode does not support web socket in place.
class WSHandler(websocket.WebSocketHandler):
    """
    A Generic web socket handler.
      * `check_origin` returns always `True`.
    """
    url = r'/ws/(?P<modname>[\w\.]+)/(?P<clsname>\w+)'
    inst = None
    __socket__ = None
    def open(self, modname, clsname):
        print 'websocket is opening...'
        self.set_nodelay(True)
        try:
            cls = getattr(importlib.import_module(modname), clsname)
        except ImportError as e:
            handle_exc(e)
        except AttributeError as e:
            handle_exc(e)
        kwargs = {key: val
            for key, vals in self.request.arguments.items()
            for val in vals}
        # print kwargs
        try:
            # print 'try bind websocket delegator'
            self.inst = cls(**kwargs)
            self.inst.__socket__ = self
        except Exception as e:
            handle_exc(e)
    def on_close(self):
        print 'websocket is closing...'
        if hasattr(self.inst, '__dnit__'):
            self.inst.__dnit__()
        if self.inst:
            self.inst.__socket__ = None
    def access(self, route):
        attrs = route.split('.')
        value = reduce(getattr, attrs, self.inst)
        return value
    def invoke(self, route, args=None, kwargs=None):
        func = self.access(route)
        return func(*args or [], **kwargs or {})
    def on_message(self, message):
        rv, err = None, None
        try:
            seq, ftype, route, payload = ujson.loads(message)
            as_binary = payload.pop('as_binary')
            func = getattr(self, ftype)
            rv = func(route, **payload)
        except Exception as e:
            info = sys.exc_info()
            source = traceback.format_exception(*info)
            print '\n======== exception on websocket ========'
            traceback.print_exception(*info)
            print '======== exception on websocket ========\n'
            err = dict(
                title = e.__class__.__name__,
                detail = str(e),
                source = source
            )
        if as_binary and rv is not None:
            # two uint32 for seq and error, 8bytes in total
            # in network byte order (big endian)
            meta = struct.pack('!II', seq, 0) # 0 for err (temporary)
            self.write_message(meta + rv, binary=True)
        else:
            self.dump_message(seq, rv, err)
    def dump_message(self, seq, rv, err):
        try:
            dumped = ujson.dumps([seq, rv, err])
        except Exception as e: # coerce
            print 'Websocket coerces output:', str(e)
            dumped = ujson.dumps([seq, str(rv), err])
            # print dumped
        self.write_message(dumped)
