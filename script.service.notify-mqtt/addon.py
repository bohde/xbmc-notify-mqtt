#!/usr/bin/python
#
import xbmcaddon
import socket
import sys
import time
import os

addon = xbmcaddon.Addon()
__cwd__ = xbmc.translatePath(addon.getAddonInfo('path')).decode("utf-8")
sys.path.append(os.path.join(__cwd__, 'resources', 'lib' ))
import mq
import ui

def main():
    logger = ui.XbmcLogger('Mqtt')

    hostname = socket.gethostname()
    broker = addon.getSetting("host")
    port = int(addon.getSetting("port"))
    root = addon.getSetting("path")

    logger.info('Connecting to %s@%s:%s/%s', hostname, broker, port, root)

    sink = ui.XbmcSink()

    client = mq.MQ(hostname, broker, port, root, sink, logger)
    client.run()

    while not xbmc.abortRequested:
            time.sleep(.1)

    logger.info('Abort requested')
    client.stop()


if __name__ == '__main__':
    main()
