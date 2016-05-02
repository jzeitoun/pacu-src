from __future__ import print_function
from __future__ import absolute_import

def deco_dumps(lib_dumps):
    def fix_encoding(o):
        if isinstance(o, unicode):
            return o.encode('utf-8')
        elif isinstance(o, dict):
            return {key: fix_encoding(val) for key, val in o.items()}
        elif hasattr(o, '__iter__'):
            return [fix_encoding(e) for e in o]
        else:
            return o
    def object_dumps(o):
        try:
            return lib_dumps(o)
        except OverflowError as e:
            return lib_dumps(fix_encoding(o))
    return object_dumps

def deco_loads(lib_loads):
    def fix_encoding(o):
        return o.encode('utf-8')
    def object_loads(o):
        try:
            return lib_loads(o)
        except ValueError as e:
            return lib_loads(fix_encoding(o))
    return object_loads

import ujson as best
best.dumps = deco_dumps(best.dumps)
best.loads = deco_loads(best.loads)
