from ..level import logging

class ColorFormatter(logging.Formatter):
    level_color_code = dict(
        NOTSET   = 37,
        DEBUG    = 36,
        INFO     = 32,
        WARNING  = 33,
        ERROR    = 35,
        CRITICAL = 31,
    )
    def format(self, record):
        foreground = self.level_color_code.get(record.levelname, 37) # fallback to white
        record.coloredname         = '\033[0;%sm%s\033[0m'   % (37, record.name)
        record.coloreddelimiter    = '\033[0;%sm%s\033[0m'   % (35, '@')
        record.coloredlevelinitial = '\033[1;%sm|%s|\033[0m' % (foreground, record.levelname[0])
        record.coloredbgopen       = '\033[0;30;%sm' % (foreground + 10)
        record.coloredbgclose      = '\033[0m'
        record.location            = ('%s.%s:' % (record.filename[:-3], record.funcName)) if record.levelno > 5 else ''
        return super(ColorFormatter, self).format(record)
    def __init__(self, fmt=None, datefmt=None):
        summary  = '%H:%M:%S'
        detail   = '%Y-%m-%d ' + summary
        time_fmt = summary
        super(ColorFormatter, self).__init__(fmt, time_fmt)
color_formatter = ColorFormatter(
    '%(coloredname)s%(coloreddelimiter)s'
    '%(asctime)s%(coloredlevelinitial)s'
    '%(location)s'
    '%(coloredbgopen)s %(message)s %(coloredbgclose)s'
)
