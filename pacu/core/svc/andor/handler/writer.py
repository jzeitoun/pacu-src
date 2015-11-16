import re

from pacu.core.svc.andor.handler.base import BaseHandler

re_filename = re.compile(r'^\w+$')

class WriterHandler(BaseHandler):
    def check(self, filename):
        if not filename:
            return 'Filename should not be blank.'
        if not re_filename.match(filename):
            return 'Filename contains invalid character.'
