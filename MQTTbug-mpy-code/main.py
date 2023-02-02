import sys,gc
print( "main: " + ssid)
print( "ip: " + str(wlan.ifconfig()[0]))
# temporary exit
#sys.exit()

try:
    lasttime = utime.time()
    livetick = 0
    while onPin():
        if lasttime + 5 <= utime.time():
            lasttime = utime.time()
            livetick += 1
            oled.fill_rect(0,20,128,10,0) 
            oled.text(f'{livetick:00005d}', 0, 20, 1)
            devline = 30
            for dev in DEVICES:
                oled.fill_rect(0,devline,128,10,0)        
                oled.text(dev.readvalues(), 0, devline, 1)
                devline += 10
                dev.publishvalues(mqtt,station)
            oled.show()
        mqtt.check_msg()
        if livetick % 60 == 0:
            gc.collect()

    if onPin():
        sys.exit()
    else:
        print("EXIT script by pin 22")
        oled.fill(0)
        oled.text('exit on Pin 22',0,0,1)
        oled.show()

except Exception as e:
    print("RESTART script on Exception {}".format(str(e)))
    oled.fill(0)
    oled.text('reset on Except',0,0,1)
    oled.text(str(e),0,10,1)
    oled.show()
    utime.sleep(5)
    if onPin:
        reset()
    