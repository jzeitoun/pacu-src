from __future__ import print_function
from __future__ import absolute_import

def deco(lib_dumps):
    def fix_encoding(o):
        if isinstance(o, unicode):
            return o.encode('utf-8')
        elif isinstance(o, dict):
            return lib_dumps({key: fix_encoding(val) for key, val in o.items()})
        elif hasattr(o, '__iter__'):
            return lib_dumps([fix_encoding(e) for e in o])
        else:
            return o
    def object_dumps(o):
        try:
            return lib_dumps(o)
        except OverflowError as e:
            return lib_dumps(fix_encoding(o))
    return object_dumps

import ujson as best
best.dumps = deco(best.dumps)
