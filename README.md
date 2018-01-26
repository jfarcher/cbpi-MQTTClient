# cbpi-MQTTClient
This plugins allows you to send data to an MQTT message broker using a [CraftBeerPi background task](https://github.com/Manuel83/craftbeerpi3/wiki/Custom-Background-Task).

## Installation
```
cd craftbeerpi3/modules/plugins/

git clone https://github.com/peakMeissner/cbpi-MQTTClient

cd cbpi-MQTTClient
```
In case you miss the eclipse phao library. Install the dependencies using:
```
pip install paho-mqtt
```

## Configuration
Based on the requirement you can define a background task in the ```__init__.py``` file. To get started check out the following example:
```
mqttc = MQTTClient().connect()                                            # initialize the MQTT client

@cbpi.backgroundtask(key='mqtt_client', interval=2.5)                     # create bg job with an interval of 2.5 seconds 
def mqtt_client_background_task(api):
    sensors = cbpi.cache.get('sensors')                                   # read available sensors

    for key, value in sensors.iteritems():                                # loop over the sensors
        topic = 'CraftBeerPi/sensor/' + str(value.instance.id)            # define the MQTT topic
        data = {                                                          # define the playload
            'id': value.instance.id,
            'value': value.instance.last_value,
            'unit': value.instance.get_unit()
        }
        payload = json.dumps(data, ensure_ascii=False)                    # convert payload to JSON
        mqttc.publish(topic, payload)                                     # publish the payload

```

## Testing
In order to test the client in a local enviroment you'll need an MQTT message broker such as [Mosquitto](https://mosquitto.org/). You can easily install the message broker on you local CraftBeerPi by using the following command. 
```
sudo apt-get install mosquitto mosquitto-clients
```
If you want to subscribe to the published content I recomend the [MQTT.fx](http://www.mqttfx.org/) client.

## Example - SAP IoT Services
Integrating CraftBeerPi through [cbpi-MQTTClient](https://github.com/peakMeissner/cbpi-MQTTClient) with [SAP IoT Services](https://www.sap.com/germany/trends/internet-of-things.html).
![](https://github.com/peakMeissner/cbpi-MQTTClient/blob/master/docs/img/SAP_IoT_Service_MQTT.png)
