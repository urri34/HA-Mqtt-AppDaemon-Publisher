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
        MessageDict = {
            'Element': 'WifiSolar',
            'Status': randint(0, 2)
        }
        SendMqttMessage(self, MessageDict)
