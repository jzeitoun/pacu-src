import importlib

from pacu.dep.json import best as json

def get(req, modname, fncname, *args, **kwargs):
    module = importlib.import_module('pacu.api.json.http.{}'.format(modname))
    func = getattr(module, 'get_{}'.format(fncname))
    rv = func(req, *args, **kwargs)
    return json.dumps(rv or {})

def post(req, modname, fncname, *args, **kwargs):
    module = importlib.import_module('pacu.api.json.http.{}'.format(modname))
    func = getattr(module, 'post_{}'.format(fncname))
    rv = func(req, *args, **kwargs)
    return json.dumps(rv or {})

def delete(req, modname, fncname, *args, **kwargs):
    module = importlib.import_module('pacu.api.json.http.{}'.format(modname))
    func = getattr(module, 'delete_{}'.format(fncname))
    rv = func(req, *args, **kwargs)
    return json.dumps(rv or {})
