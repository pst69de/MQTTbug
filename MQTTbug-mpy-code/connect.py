from secrets import ssids, mqtts
import utime
from umqtt.simple import MQTTClient

def wlan_connect(wlan, ssid, host, oled, line):
    mypreshared = ssids[ssid]
    print("try connect " + ssid)
    #wlan.config(hostname=thehost)
    wlan.connect(ssid, mypreshared)
    
    maxwait = 10
    while maxwait > 0:
        if wlan.isconnected():
            break
        maxwait -= 1
        print('waiting for connect')
        utime.sleep(1)
    
    if not wlan.isconnected():
        raise RuntimeError('network connect failed')
    else:
        status = wlan.ifconfig()
        print('connect', status[0])
        oled.fill(0)
        line = 0
        oled.text('con:' + ssid,0,line,1)
        line += 10
        oled.text(str(status[0]),0,line,1)
        line += 10
        oled.show()
    return wlan

def mqtt_callback(topic,msg):
    print("Message received")
    print(msg)

def mqtt_connect(mqtt, mqtthost, mqtttopic, station):
    #MQTT Client connect
    mqtt = MQTTClient(client_id=station, server=mqtthost, port=1883, user=mqtts[mqtthost][0], password=mqtts[mqtthost][1], keepalive=3600, ssl=False, ssl_params={})
    mqtt.connect()
    mqtt.set_callback(mqtt_callback)
    mqtt.subscribe(mqtttopic)
    return mqtt
