import json
import mosquitto

class MQ(object):
    def __init__(self, hostname, broker, port, root, sink, logger):
        self.hostname = hostname
        self.broker = broker
        self.port = port
        self.root = root.strip('/')
        self.sink = sink
        self.logger = logger

        self.topic_msgs = root + "/all/messages"
        self.topic_status = root + hostname + "/status"

        id = "xbmc-mqtt-%s" % (hostname,)
        self.client = mosquitto.Mosquitto(client_id=id, clean_session=False)


    def on_connect(self, mosq, obj, rc):
        self.sink.on_connect()
        self.client.publish(self.topic_status, payload="online", qos=0, retain=True)
        self.client.subscribe(self.topic_msgs, 1)


    def on_message(self, mosq, obj, msg):
        self.logger.info('Message receieved')
        self.logger.debug('Message: %s %s %s', msg.topic, msg.qos, msg.payload)

        try :
            msg = json.loads(msg.payload)
            self.sink.on_message(msg)
        except Exception as e:
            self.logger.error('Unknown message exception: %', e)
            self.logger.error('Faulty Message: %s %s %s', msg.topic, msg.qos, msg.payload)


    def on_publish(self, mosq, obj, mid):
        pass


    def on_subscribe(self, mosq, obj, mid, granted_qos):
        self.logger.info("Subscribed: %s %s", mid, granted_qos)


    def on_log(self, mosq, obj, level, string):
        self.logger.info("Server log: [%s] %s", level, string)


    def run(self):
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe

        self.client.will_set(self.topic_status, payload="offline", qos=0, retain=True)
        self.client.reconnect_delay_set(delay=3, delay_max=30, exponential_backoff=True)

        try:
            self.client.connect(self.broker, self.port, 60)
        except Exception as e:
            self.logger.fatal("connection failed: %s", e)
            return

        self.client.loop_start()


    def stop(self):
        self.client.loop_stop()
