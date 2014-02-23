# Wrappers around xbmc builtins to not depend on them

from __future__ import print_function
import logging

try:
    import xbmc
except ImportError:
    xbmc = None

class XbmcLogger(object):
    def __init__(self, name):
        if not xbmc:
            raise ReferenceError("The xbmc module is not available")
        self.name = name

    def format_message(self, message):
        return u'%s -- %s' % (self.name, message,)

    def log(self, level, message, *args):
        m = unicode(message) % args
        xbmc.log(self.format_message(m).encode('ascii', 'replace'), level)

    def info(self, message, *args):
        self.log(xbmc.LOGNOTICE, message, *args)

    def debug(self, message, *args):
        self.log(xbmc.LOGDEBUG, message, *args)

    def error(self, message, *args):
        self.log(xbmc.LOGERROR, message, *args)

    def severe(self, message, *args):
        self.log(xbmc.LOGSEVERE, message, *args)

    def fatal(self, message, *args):
        self.log(xbmc.LOGFATAL, message, *args)


class Logger(object):
    def __init__(self, name):
        self.logger = logging.getLogger(name)

    def info(self, message, *args):
        self.logger.info(message, *args)

    def debug(self, message, *args):
        self.logger.debug(message, *args)

    def error(self, message, *args):
        self.logger.error(message, *args)

    def severe(self, message, *args):
        self.logger.error(message, *args)

    def fatal(self, message, *args):
        self.logger.critical(message, *args)


class LoggerSink(object):
    def __init__(self, logger):
        self.logger = logger

    def on_connect(self):
        self.logger.info('Mqtt Connected')

    def on_message(self, msg):
        self.logger.info('Received message: %s', msg)


class XbmcSink(object):
    def __init__(self):
        if not xbmc:
            raise ReferenceError("The xbmc module is not available")

    def on_connect(self):
        self.notify('Mqtt Connected', 'Waiting for messages', 10)

    def on_message(self, msg):
        self.notify(msg['title'], msg['text'], msg['duration'], msg.get('image', None))

    def escape(self, s):
        return unicode(s).replace('"', r'\"').join('""')

    def call(self, method, *args):
        method_call = u'%s(%s)' % (method, (','.join(map(self.escape, args))))
        xbmc.executebuiltin(method_call.encode('ascii', 'replace'))

    def notify(self, title, body, time, img=None):
        args = [title, body, int(time * 1000)]
        if img:
            args += [img]
        self.call('Notification', *args)
