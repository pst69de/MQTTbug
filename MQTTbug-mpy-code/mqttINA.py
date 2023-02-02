#!/usr/bin/python3

class INA:
    def __init__(self,i2c):
        self.I2C = i2c
        # from ina219 import INA219
        from adafruit_ina219 import INA219, ADCResolution, BusVoltageRange
        #self.device = INA219(shunt_ohms=0.1, max_expected_amps = 1.0, address=0x40)
        #self.device.configure(voltage_range=self.device.RANGE_32V, gain=self.device.GAIN_AUTO, bus_adc=self.device.ADC_128SAMP, shunt_adc=self.device.ADC_128SAMP)
        self.device = INA219(self.I2C)
        self.device.bus_adc_resolution = ADCResolution.ADCRES_12BIT_128S
        self.device.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_128S
        # optional : change voltage range to 16V
        self.device.bus_voltage_range = BusVoltageRange.RANGE_32V
        self.device.set_calibration_32V_2A()

        self.v=self.device.bus_voltage
        self.i=self.device.current
        self.p=self.device.power/1000
        
    def readvalues(self):
        self.v=self.device.bus_voltage
        self.i=self.device.current
        self.p=self.device.power/1000
        return '{0:0.2f}V{1:0.0f}mA{2:0.2f}W'.format(self.v,self.i,self.p)
        
    def publishvalues(self, mqtt, base):
        self.v=self.device.bus_voltage
        # paho style
        #mqtt.publish(topic=base+"/device/INA/tension",payload='{0:0.2f}'.format(self.v))
        mqtt.publish(topic=base+"/device/INA/tension",msg='{0:0.2f}'.format(self.v))
        self.i=self.device.current
        # paho style
        #mqtt.publish(topic=base+"/device/INA/current",payload='{0:0.0f}'.format(self.i))
        mqtt.publish(topic=base+"/device/INA/current",msg='{0:0.0f}'.format(self.i))
        self.p=self.device.power/1000
        # paho style
        #mqtt.publish(topic=base+"/device/INA/power",payload='{0:0.2f}'.format(self.p))
        mqtt.publish(topic=base+"/device/INA/power",msg='{0:0.2f}'.format(self.p))
        
