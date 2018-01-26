import paho.mqtt.client as mqtt
import uuid
from modules import cbpi

"""
This class creates an MTTQ client for the CraftBeerPi application. The class
uses the eclipse paho library (https://www.eclipse.org/paho/clients/python/).
In order to instantiate the class simply pass a configuration dictionary to the
constructor. The config dictionary can contain the following options:

    {
        'id': 'yourClientID',		# Client ID	-> defaults to generated UUID
        'host': 'your-mqtt-host.com'    # URI           -> defaults to 127.0.0.1
        'port': 8883                    # Port          -> defaults to 1883
        'keepalive': 60                 # Lifetime      -> defaults to 60s
        'credentials': {                # HTTP-Config   -> defaults to None
            'user': 'foo'               #   User
            'password': 'bar'           #   Password
        }
        'tls_settings': {               # TLS-Config    -> defaults to None
            'ca_certs': '/etc/ssl/...'  #   Cert-Dir
            'tls_version': XXX          #   TLS-Version  -> defaults TLSv1
        }
    }

"""
class MQTTClient():
    config = {
        'host': '127.0.0.1',
        'port': 1883,
        'keepalive': 60,
        'credentials': None,
        'tls_settings': None
    }

    def __init__(self, config=None):
        if config is not None:
            self.config = config

        if self.config.get('id') is None:
           self.config['id'] = uuid.uuid4().hex 
           
        self.__mqttc = mqtt.Client(client_id=self.config.get('id'))
        self.__mqttc.on_connect = self.__on_connect

    def __on_connect(self, client, userdata, flags, rc):
        cbpi.app.logger.info('MQTTClient connected. RC = ' + str(rc))

    def connect(self):
	credentials = self.config.get('credentials')
	tls = self.config.get('tls_settings')

        if credentials is not None:
            self.__mqttc.username_pw_set(**credentials)

        if tls is not None:
            self.__mqttc.tls_set(**tls)

        self.__mqttc.connect(
            self.config.get('host'),
            self.config.get('port'),
            self.config.get('keepalive')
        )
        return self

    def publish(self, topic, payload):
        self.__mqttc.loop_start()
        self.__mqttc.publish(topic, payload)
        self.__mqttc.loop_stop()
        return True
