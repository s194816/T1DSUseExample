import paho.mqtt.client as paho
from paho import mqtt

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)
    
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))   

def on_message(client, userdata, msg):
    print(msg.topic + ": " + str(msg.payload))
      

def subscribe (topic) :
    
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    client.on_connect = on_connect

    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

    client.username_pw_set("DEM-T1DS", "Thesis1234")

    client.connect("4af60bec82144872a35cde8b4ad13058.s1.eu.hivemq.cloud", 8883)

    client.on_subscribe = on_subscribe
    client.on_message = on_message

    client.subscribe(topic,qos=0)
    client.loop_forever()

