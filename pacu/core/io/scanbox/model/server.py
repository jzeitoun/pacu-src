import importlib

from flask import Flask
from flask import request
from flask_restless import APIManager
from flask_restless.views.base import ModelView

from pacu.core.io.scanbox.model import db as schema

class nmspc:
    session = schema.get_sessionmaker(':memory:', echo=False, autocommit=False)

# monkey patching for dynamic session binding
modelview_init_original = ModelView.__init__
def modelview_init_override(self, session, model, *args, **kw):
    modelview_init_original(self, nmspc.session, model, *args, **kw)
ModelView.__init__ = modelview_init_override

def select_db_session():
    sa = request.headers.get('pacu-jsonapi-session-arguments')
    mn = request.headers.get('pacu-jsonapi-module-name')
    if all((sa, mn)):
        Session = importlib.import_module(mn).Session(*sa.split(','), echo=False)
        nmspc.session = Session()

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS, GET, PUT, POST, DELETE, HEAD, PATCH'
    response.headers['Access-Control-Allow-Headers'] = 'PACU_JSONAPI_MODULE_NAME, PACU_JSONAPI_SESSION_ARGUMENTS, PACU_JSONAPI_BASE_NAME, Content-Type'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

def create_endpoint():
    app = Flask(__name__)
    app.before_request(select_db_session)
    app.after_request(add_cors_headers)
    methods = 'GET POST PUT DELETE PATCH'.split()
    manager = APIManager(app=app, session=nmspc.session)
    manager.create_api(schema.Workspace, methods=methods)
    manager.create_api(schema.Condition, methods=methods)
    manager.create_api(schema.ROI, methods=methods)
    manager.create_api(schema.Datatag, methods=methods)
    manager.create_api(schema.Trial, methods=methods)
    manager.create_api(schema.Colormap, methods=methods)
    manager.create_api(schema.EphysCorrelation, methods=methods)
    return app
