import os
import time
import machine
import network
import ubinascii
import urequests

import dht


CFG_BSSID='SRRU-IoT'
CFG_BSSID_PASS='SrruIoT@2019'

FRONT_LED = machine.Pin(2, machine.Pin.OUT)
DHT_SENSOR = dht.DHT22(machine.Pin(5))
SOIL_SENSOR = machine.ADC(0)
RELAY = machine.Pin(4,machine.Pin.OUT)


def __init__():
	FRONT_LED.value(1)
	ap = network.WLAN(network.AP_IF)
	ap.active(False)
	FRONT_LED.value(1)


def do_connect():

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        if wlan.isconnected():
                print(wlan.ifconfig())
                return

        if not wlan.isconnected():
                wlan.connect(CFG_BSSID, CFG_BSSID_PASS)
                c = 0
                while not wlan.isconnected():
                        time.sleep(1)
                        print('[',c,'] connecting ... to WLAN')
                        c = c + 1
                        FRONT_LED.value(c%2)
                        if c > 300:
                                return False
                        pass

        return True
def blink_led(t=1,d=0.1):
        while t >= 0:
                FRONT_LED.value(t%2)
                t = t - 1 
                time.sleep(d)
        FRONT_LED.value(1)
        
def measurment():
 
        temp = None
        humid = None
        soil = None
        
        try:
                blink_led(10,0.05)
                DHT_SENSOR.measure()
                temp = DHT_SENSOR.temperature()
                humid  = DHT_SENSOR.humidity()

        except:
                print("DHT sensor failed!!")

        try:
                blink_led(5, 0.1)
                soil = SOIL_SENSOR.read()
        except:
                print("Soil sensor failed!!")
                
        print("data => ", temp,", ",humid,", ",soil)
        
        return temp, humid, soil

def send_data(temp,humid):

        try:
                print("sending humid=",humid,", temp=",temp)
                send_url = "https://surin.srru.ac.th/api/iot/data?token=431.2218518518519&device_id=0"
                if temp is not None:
                        send_url = send_url+"&dht_temperature="+str(temp)
                if humid is not None:
                        send_url = send_url+"&dht_humidity="+str(humid)
                urequests.get(send_url)
                return True
        except:
                print("Failed to send temp,humid of (",temp,",",humid,")")
                      
        return False

def deep_sleep():
        print('Deep sleep...for .. 20s')
        rtc = machine.RTC()
        rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
        rtc.alarm(rtc.ALARM0, 20000)
        machine.deepsleep()
        
if __name__ == '__main__':

	__init__()
	connected = do_connect()

	if connected:
                while True:
                        temp, humid, soil = measurment()
                        if soil > 790:
                                RELAY.on()
                        else:
                                RELAY.off()
                                
                        time.sleep(2)
                        
