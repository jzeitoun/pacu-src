from .. import identity
from . import formatter
from .level import logging

def get_default():
    global formatter
    level = identity.log.level
    name = identity.path.src.name
    if name in logging.Logger.manager.loggerDict:
        return logging.getLogger(name)
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    logger.setLevel(level)
    handler.setLevel(level)
    handler.setFormatter(getattr(formatter, identity.log.formatter))
    logger.addHandler(handler)
    logger.debug('initializing <%s> logger at level %s !' % (name, level))
    return logger
