from machine import Pin, I2C, reset
from hal import mySDA, mySCL
import utime

from sh1106 import SH1106_I2C
import framebuf

#from adafruit_sht31d import SHT31D

from secrets import station, ssids, mqtts
import network
from connect import wlan_connect, mqtt_connect

onPin = Pin(22, mode=Pin.IN, pull=Pin.PULL_UP)
print('onPin is 22')

try:
    # 0x3C is used by SSH1306 and SH1106 OLEDs
    print('try I2C')
    CHECKI2CDEVICES = { 0x3C: "mqttOLED", 0x40: "mqttINA", 0x44: "mqttSHT", 0x23:"mqttBH", 0x48:"mqttADS"}
    DEVICES = []
    i2c = I2C(0, sda = Pin(mySDA), scl = Pin(mySCL), freq = 400000)
    print('try OLED')
    oled = SH1106_I2C(128, 64, i2c, rotate = 180)

    oled.fill(0)
    line = 0

    climate = None

    print('scan I2C')
    for dev in i2c.scan():
        if dev in CHECKI2CDEVICES.keys():
            print('{0} in DEVICES {1}'.format(hex(dev),CHECKI2CDEVICES[dev]))
            if CHECKI2CDEVICES[dev] == "mqttOLED":
                #from mqttOLED import OLED
                #DEVICES.append(OLED(i2c))
                print('found OLED')
                oled.text("OLED",0,line,1)
                line += 10
                oled.show()
                pass
            if CHECKI2CDEVICES[dev] == "mqttINA":
                from mqttINA import INA
                DEVICES.append(INA(i2c))
                print('found INA')
                oled.text("INA",0,line,1)
                line += 10
                oled.show()
            if CHECKI2CDEVICES[dev] == "mqttBH":
                from mqttBH import BH
                DEVICES.append(BH(i2c))
                print('found BH')
                oled.text("BH",0,line,1)
                line += 10
                oled.show()
            if CHECKI2CDEVICES[dev] == "mqttSHT":
                from mqttSHT import SHT
                DEVICES.append(SHT(i2c))
                climate = DEVICES[-1]
                print('found SHT')
                oled.text("SHT",0,line,1)
                line += 10
                oled.show()
            if CHECKI2CDEVICES[dev] == "mqttADS":
                from mqttADS import ADS
                DEVICES.append(ADS(i2c))
                print('found ADS')
                oled.text("ADS",0,line,1)
                line += 10
                oled.show()
        else:
            print('{0} unknown device'.format(hex(dev)))


    #climate = SHT31D(i2c)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    ssid = ""
    rssi = -90
    stats = wlan.scan()
    #(ssid, bssid, channel, RSSI, security, hidden)
    for stat in stats:
        network = stat[0].decode()
        if stat[3] >= rssi and network in ssids:
            ssid = network
            rssi = stat[3]
            print(network)
            oled.text(network,0,line,1)
            oled.text(str(stat[3]),96,line,1)
            line += 10
            oled.show()

    mqtthost = "192.168.69.111"
    mqtt = None
    mqtttopic = str.encode(station + "/text")


    wlan = wlan_connect(wlan, ssid, station, oled, line)
    mqtt = mqtt_connect(mqtt, mqtthost, mqtttopic, station)

    #mqtt.wait_msg()
except Exception as e:
    print("RESTART script on Exception {}".format(str(e)))
    utime.sleep(15)
    if onPin:
        reset()

