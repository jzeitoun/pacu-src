from __future__ import print_function
from __future__ import absolute_import

try:
    import ujson as best
    best.dumps(u'  ')
except:
    try:
        import yajl as best
        best.dumps(u'  ')
    except:
        try:
            import simplejson as best
            best.dumps(u'  ')
        except:
            import json as best
            best.dumps(u'  ')

print('json library resolved', best)
