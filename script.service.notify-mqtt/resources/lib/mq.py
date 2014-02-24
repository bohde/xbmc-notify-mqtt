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

        self.topic_msgs = "/all/messages"
        self.topic_status = hostname + "/status"

        id = "xbmc-mqtt-%s" % (hostname,)
        self.client = mosquitto.Mosquitto(client_id=id, clean_session=False)


    def auth(self, username, password=None):
        self.client.username_pw_set(username, password)


    def on_connect(self, mosq, obj, rc):
        self.sink.on_connect()
        self.publish(self.topic_status, payload="online", qos=0, retain=True)
        self.client.subscribe(self.topic_msgs, 1)


    def on_message(self, mosq, obj, msg):
        self.logger.info('Message receieved')
        msg.payload = unicode(msg.payload.decode('utf-8'))
        msg.topic = unicode(msg.topic.decode('utf-8'))
        self.logger.debug(u'Message: %s %s %s', msg.topic, msg.qos, msg.payload)

        try :
            payload = json.loads(msg.payload)
            self.sink.on_message(payload)
        except Exception as e:
            self.logger.error(u'Faulty Message: %s %s %s', msg.topic, msg.qos, msg.payload)


    def on_subscribe(self, mosq, obj, mid, granted_qos):
        self.logger.info("Subscribed: %s %s", mid, granted_qos)


    def publish(self, topic, *args, **kwargs):
        self.client.publish(self.root + topic, *args, **kwargs)


    def run(self):
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe

        self.client.will_set(self.root + self.topic_status, payload="offline", qos=0, retain=True)
        self.client.reconnect_delay_set(delay=3, delay_max=30, exponential_backoff=True)

        try:
            self.client.connect(self.broker, self.port, 60)
        except Exception as e:
            self.logger.fatal("connection failed: %s", e)
            return

        self.client.loop_start()


    def stop(self):
        self.client.loop_stop()
