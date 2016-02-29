import importlib

import ujson

def get(req, modname, fncname, *args):
    module = importlib.import_module('pacu.api.json.http.{}'.format(modname))
    func = getattr(module, fncname)
    rv = func(req, *args)
    return ujson.dumps(rv or {})
