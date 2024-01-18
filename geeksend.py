import appdaemon.plugins.hass.hassapi as hass
from json import dumps
from random import randint

PUBLISH_TOPIC = "display/state"

def SendMqttMessage(self, MessageDict):
    try:
        Message = dumps(MessageDict)
        self.log("GeekSend: Converted json ("+str(MessageDict)+") -> mqtt ("+str(Message)+")")
        self.mqtt.mqtt_publish(PUBLISH_TOPIC, Message)
        self.log("GeekSend: Published under "+str(PUBLISH_TOPIC))
    except KeyError as ex:
        self.log("GeekSend: ERROR="+ex)
    pass

class GeekSend(hass.Hass):
    def initialize(self):
        self.mqtt = self.get_plugin_api("MQTT")
        self.listen_event(self.GeekSendReceivedEvent, "GEEK_SEND_EVENT")
        if self.mqtt.is_client_connected():
            self.log("GeekSend: MQTT is connected")
        self.log("GeekSend: Initialized")
        MessageDict = {
            'Element': 'Monitoring!',
            'Status': '0'
        }
        SendMqttMessage(self, MessageDict)

    def GeekSendReceivedEvent(self, event_name, data, kwargs):
        self.log("GeekSend: GEEK_SEND_EVENT wake up geek_send_received_event()")
        self.log("GeekSend: event_name value="+str(event_name))
        self.log("GeekSend: data value="+str(data))
        self.log("GeekSend: kwargs value="+str(kwargs))
        MessageDict = {
            'Element': 'empty',
            'Status': 'none'
        }
        for Parameter in data:
            if Parameter == 'Element':
                MessageDict['Element']=data['Element']
            if Parameter == 'Status':
                MessageDict['Status']=data['Status']
        SendMqttMessage(self, MessageDict)
