from ... import profile

from pacu.core.io.scanbox.impl2 import ScanboxIO
from pacu.core.io.scanbox.model import db as schema
import flask_restless
from flask_restless import APIManager
from flask import Flask, request

app = Flask(__name__)
q = ScanboxIO('day_ht/day5_003_020.io')
manager = APIManager(app='', session='')
manager = APIManager(app=app, session=q.db_session)
manager.create_api(schema.Workspace, methods=['GET', 'POST'])
manager.create_api(schema.Condition, methods=['GET', 'POST'])
manager.create_api(schema.ROI, methods=['GET', 'POST'])
manager.create_api(schema.Datatag, methods=['GET', 'POST'])
def add_cors_headers(response):
    print 'HEAHADEHAEDHAEHDA', response
    print manager.session
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS, GET, PUT, POST, DELETE, HEAD'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'PACU_JSONAPI_MODULE_NAME, PACU_JSONAPI_SESSION_ARGUMENTS, PACU_JSONAPI_BASE_NAME'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

def before():
    print 'BEFORE REQUST'

app.before_request(before)
app.after_request(add_cors_headers)
# app.run()

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)
# IOLoop.instance().start()

def main(**kwargs):
    profile.manager.currents.update(kwargs)
    profile.manager.print_status()
    log, web = profile.manager.instances('log', 'web')
    if NotImplemented in [web]:
        log.error('Unable to initialize profiles. Stop...')
    else:
        try:
            log.debug(web.format_status())
            return web.run()
        except Exception as e:
            log.error('Failed to run app. ({!s})'.format(e))
if __name__ == '__api_main__':
    main()
