from general.umqttsimple import MQTTClient
from machine import Pin
import ubinascii

import machine
import time


pin4, pin13, pin16 = Pin(4, Pin.OUT), Pin(13, Pin.OUT), Pin(16, Pin.OUT)

pin34, pin35, pin36, pin37, pin38, pin39 = Pin(34, Pin.IN), Pin(35, Pin.IN), Pin(36, Pin.IN), Pin(37, Pin.IN), Pin(38, Pin.IN), Pin(39, Pin.IN)

mqtt_server = '192.168.1.6'
client_id = ubinascii.hexlify(machine.unique_id()).decode('utf-8')
   #nombre = ubinascii.hexlify(machine.unique_id()).decode('utf-8')
topic_sub = nombre + '/confirmacion'
topic_sub = topic_sub.encode()

topic_sub2 = nombre + '/IO2/mando'
topic_sub2 = topic_sub2.encode()

topic_sub4 = nombre + '/IO4/mando'
topic_sub4 = topic_sub4.encode()

topic_sub13 = nombre + '/IO13/mando'
topic_sub13 = topic_sub13.encode()

topic_sub16= nombre + '/IO16/mando'
topic_sub16 = topic_sub16.encode()
######################################################
topic_pub = nombre + '/confirmacion'
topic_pub = topic_pub.encode()

topic_pub2 = nombre+"/IO2/estado"
topic_pub2 = topic_pub2.encode()

topic_pub4 = nombre+"/IO4/estado"
topic_pub4 = topic_pub4.encode()

topic_pub13 = nombre+"/IO13/estado"
topic_pub13 = topic_pub13.encode()

topic_pub16 = nombre+"/IO16/estado"
topic_pub16 = topic_pub16.encode()

a = [topic_pub, topic_pub2, topic_pub4, topic_pub13, topic_pub16]

b = [topic_sub2, topic_sub4, topic_sub13, topic_sub16]

last_message = 0
message_interval = .5

counter = 0
def sub_cb(topic, msg):

    if topic == topic_sub and b"1" in msg:
        pin2.off()
        time.sleep(.2)
        led.on()

    if topic == topic_sub2 and msg == b"1":
      pin2.on()
    elif topic == topic_sub2 and msg == b"0":
      pin2.off()

    if topic == topic_sub4 and msg == b"1":
      pin4.on()
    elif topic == topic_sub4 and msg == b"0":
      pin4.off()

    if topic == topic_sub13 and msg == b"1":
      pin13.on()
    elif topic == topic_sub13 and msg == b"0":
      pin13.off()

    if topic == topic_sub16 and msg == b"1":
      pin16.on()
    elif topic == topic_sub16 and msg == b"0":
      pin16.off()

def connect_and_subscribe():
    global nombre, mqtt_server, topic_sub
    client = MQTTClient(nombre, mqtt_server,user="", password="", port=1883)
    client.set_callback(sub_cb)
    client.connect()
    for i in range (len(b)):
        client.subscribe(b[i])
        print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, b[i]))
    return client

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

while True:

    try:
        client.check_msg()
        if (time.time() - last_message) > message_interval:

            msg = b'Hola%d' % counter
            estado_2 = b'%d' % pin2.value()
            estado_4 = b'%d' % pin4.value()
            estado_13 = b'%d' % pin13.value()
            estado_16 = b'%d' % pin16.value()

            m = [msg, estado_2, estado_4, estado_13, estado_16]

            for i in range (len(a)):

                client.publish(a[i], m[i])
            last_message = time.time()
            counter += 1

    except OSError as e:
        restart_and_reconnect()
