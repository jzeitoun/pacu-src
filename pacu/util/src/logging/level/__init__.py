from __future__ import absolute_import

import logging

logging.VERBOSE = 5
logging.addLevelName(logging.VERBOSE, 'VERBOSE')
logging.Logger.verbose = lambda inst, msg, *args, **kwargs:\
    inst.log(logging.VERBOSE, msg, *args, **kwargs)

for name in (
    'verbose' , # DEV CODING-TIME
    'debug'   , # DEV RUN-TIME
    'info'    , # SERVICE TRACKING
    'warning' , # DEPRECATION, CATCHABLE
    'error'   , # BOOTSTRAP FAIL, UNCATCHABLE
    'critical'  # SECURITY
    ): setattr(logging.Logger, name[0], getattr(logging.Logger, name))
