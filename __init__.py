import json
from modules import cbpi
from MQTTClient import MQTTClient

mqttc = MQTTClient().connect()                                            # initialize the MQTT client

                                                                          # uncomment and modify :)
@cbpi.backgroundtask(key='mqtt_client', interval=2.5)                     # create bg job with an interval of 2.5 seconds 
def mqtt_client_background_task(api):
    sensors = cbpi.cache.get('sensors')                                   # read available sensors

    for key, value in sensors.iteritems():                                # loop over the sensors
        topic = 'CraftBeerPi/sensor/' + str(value.instance.id)            # define the MQTT topic
        data = {                                                          # define the playload
            'id': value.instance.id,
            'name':value.instance.name,
            'actual': value.instance.last_value,
            'unit': value.instance.get_unit()
        }
        payload = json.dumps(data, ensure_ascii=False)                    # convert payload to JSON
        mqttc.publish(topic, payload)                                     # connect to the MQTT server and publish the payload
