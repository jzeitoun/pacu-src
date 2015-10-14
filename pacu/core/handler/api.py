import importlib

# from ipdb import set_trace
from ...ext.tornado.web import RequestHandler

class APIHandler(RequestHandler):
    url = r'/api/(?P<api>[\w-]+)(?P<args>[\w/\-\.]*)'
    def prepare(self):
        try:
            api = self.path_kwargs['api']
            args = self.path_kwargs['args']
            try:
                self.http = importlib.import_module('pacu.api.%s.http' % api)
            except ImportError as e:
                print 'ImportError:', e
                self.send_error(404)
            else:
                self.args = filter(None, args.split('/'))
                self.kwargs = {key: val
                    for key, vals in self.request.arguments.items()
                    for val in vals}
        except KeyError:
            self.send_error(400)
        except Exception as e:
            print e
            self.send_error(500)
    # TODO: method extraction
    def head(self, api, args):
        try:
            result = self.http.head(self.request, *self.args, **self.kwargs)
        except TypeError as e:
            print e, type(e)
            self.set_status(400) # possible argument error
            self.write(str(e))
        except Exception as e:
            print e, type(e)
            self.set_status(403)
            self.write(str(e))
        else:
            for key, val in result:
                self.add_header(key, val)
            # self.finish(result)
    def get(self, api, args):
        if api == 'ping':
            return self.http.get(self, *self.args, **self.kwargs)
        try:
            result = self.http.get(self.request, *self.args, **self.kwargs)
        except TypeError as e:
            print e, type(e)
            self.set_status(400) # possible argument error
            self.write(str(e))
        except Exception as e:
            print e, type(e)
            self.set_status(403)
            self.write(str(e))
        else:
            self.finish(result)
    def post(self, api, args):
        try:
            result = self.http.post(self.request, *self.args, **self.kwargs)
        except TypeError as e:
            print e, type(e)
            self.set_status(400) # possible argument error
            self.write(str(e))
        except Exception as e:
            print e, type(e)
            self.set_status(403)
            self.write(str(e))
        else:
            self.finish(result)
