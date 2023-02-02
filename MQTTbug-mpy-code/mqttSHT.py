#!/usr/bin/python3

class SHT:
    def __init__(self,i2c):
        self.I2C = i2c
        from adafruit_sht31d import SHT31D
        self.device = SHT31D(self.I2C, 0x44)

        self.t=self.device.temperature
        self.rh=self.device.relative_humidity 
        
    def readvalues(self):
        self.t=self.device.temperature
        self.rh=self.device.relative_humidity 
        return '{0:0.1f}dgC {1:0.1f}RH%'.format(self.t, self.rh)
        
    def publishvalues(self, mqtt, base):
        self.t=self.device.temperature
        # paho style
        #mqtt.publish(topic=base+"/device/SHT/temperature",payload='{0:0.1f}'.format(self.t))
        mqtt.publish(topic=base+"/device/SHT/temperature",msg='{0:0.1f}'.format(self.t))
        self.rh=self.device.relative_humidity 
        # paho style
        #mqtt.publish(topic=base+"/device/SHT/humidity",payload='{0:0.1f}'.format(self.rh))
        mqtt.publish(topic=base+"/device/SHT/humidity",msg='{0:0.1f}'.format(self.rh))

