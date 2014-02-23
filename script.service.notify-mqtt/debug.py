#!/usr/bin/python
# A script to test message sending outside of xbmc.
# Usage ./debug.py <broker host> <broker port> <topic root>
import socket
import sys
import time
import os
import logging

PROJECT_ROOT = os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'resources', 'lib' ))
import mq
import ui

def main(broker, port, root):
    logging.basicConfig(level=logging.DEBUG)
    logger = ui.Logger('Mqtt')

    hostname = socket.gethostname()
    port = int(port)

    logger.info('Connecting to %s@%s:%s/%s', hostname, broker, port, root)

    sink = ui.LoggerSink(logger)

    client = mq.MQ(hostname, broker, port, root, sink, logger)
    client.run()

    try:
        while True:
            time.sleep(.1)
    except KeyboardInterrupt:
        pass

    logger.info('Abort requested')
    client.stop()


if __name__ == '__main__':
    main(*sys.argv[1:])
