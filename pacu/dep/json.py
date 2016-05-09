from __future__ import print_function
from __future__ import absolute_import

import numpy as np

def deco_dumps(lib_dumps):
    def fix_todict(o):
        if hasattr(o, 'toDict'):
            return fix_todict(o.toDict())
        elif isinstance(o, dict):
            return {key: fix_todict(val) for key, val in o.items()}
        elif hasattr(o, '__iter__'):
            return [fix_todict(e) for e in o]
#         elif isinstance(o, np.inf.__class__):
#             return 'inf'
        else:
            return o
    def object_dumps(o):
        try:
            return lib_dumps(o)
        except OverflowError as e:
            return lib_dumps(fix_todict(o))
    return object_dumps

# def deco_loads(lib_loads):
#     def fix_encoding(o):
#         return o.encode('utf-8')
#     def object_loads(o):
#         try:
#             return lib_loads(o)
#         except ValueError as e:
#             return lib_loads(fix_encoding(o))
#     return object_loads

# ujson > 1.3 has weird error with unicode
# so use 1.2 and make json interface manually
import ujson as best
best.dumps = deco_dumps(best.dumps)
# best.loads = deco_loads(best.loads)
