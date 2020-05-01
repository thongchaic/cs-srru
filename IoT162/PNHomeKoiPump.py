import os
import time
import machine
import network
import ubinascii
#import urequests
#from MQ2 import MQ2
#import dht
from umqtt.simple import MQTTClient

CFG_BSSID='PNHome2'
CFG_BSSID_PASS='st11ae58*'
MQTT = MQTTClient("6a27c8877f52","qrdee.co",1883,"miot","SrruMIoT@2019")
#DHT_SENSOR = dht.DHT22(machine.Pin(5))
FILTER = machine.Pin(14,machine.Pin.OUT)
FOUTAIN = machine.Pin(12,machine.Pin.OUT)

def __init__():
	ap = network.WLAN(network.AP_IF)
	ap.active(False)
	FILTER.off()
	FOUTAIN.off()
	
	
def do_connect():

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        if wlan.isconnected():
                print(wlan.ifconfig())
                return True

        if not wlan.isconnected():
                wlan.connect(CFG_BSSID, CFG_BSSID_PASS)
                c = 0
                while not wlan.isconnected():
                        time.sleep(1)
                        print('[',c,'] connecting ... to WLAN')
                        c = c + 1
                        if c > 300:
                                return False
                        pass

        return True
        
def deep_sleep():
        print('Deep sleep...for .. 60s')
        rtc = machine.RTC()
        rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
        rtc.alarm(rtc.ALARM0, 60000)
        machine.deepsleep()

def mqtt_sub(t,m):
        print(str(t))
        print(str(m))
        if t == b"/pnhome/koi/filter":
                if m == b"0":
                        FILTER.off()
                else:
                        FILTER.on()
        if t == b"/pnhome/koi/foutain":
                if m == b"0":
                        FOUTAIN.off()
                else:
                        FOUTAIN.on()
        if t == b"/pnhome/koi/status":
                pl = str(FILTER.value())+str(FOUTAIN.value())
                MQTT.publish(b"/pnhome/koi/value",pl)
                
if __name__ == '__main__':

	__init__()

        while True:
                connected = do_connect()
                if connected:
                        
                        MQTT.set_callback(mqtt_sub)
                        MQTT.connect()
                        MQTT.subscribe(b"/pnhome/koi/foutain")
                        MQTT.subscribe(b"/pnhome/koi/filter")
                        MQTT.subscribe(b"/pnhome/koi/status")
                        #MQTT.wait_msg()
                        if True:
                                t1 = time.time()
                                while True:
                                        try:
                                                #print("WAit")
                                                dif = time.time() - t1
                                                #print(t1, time.time(), dif)
                                                MQTT.check_msg()
                                                time.sleep(0.5)
                                                if dif > 90:
                                                        t1 = time.time()
                                                        pl = str(FILTER.value())+str(FOUTAIN.value())
                                                        MQTT.publish(b"/pnhome/koi/value",pl)
                                                        break
                                                        
                                                        
                                                #MQTT.wait_msg()
                                        finally:
                                                #MQTT.disconnect()
                                                pass
                                                #print("disconnected ... ")
##                                                #time.sleep(1)
                                                #machine.reset()
                                                
                        else:
                                #print("Check...")
                                MQTT.check_msg()
                                time.sleep(1)
                        
                else:
                        time.sleep(10)

