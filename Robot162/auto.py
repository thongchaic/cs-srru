import os 
import time
import machine
import network
import ubinascii
import urequests

from hcsr04 import HCSR04


#CFG_BSSID='SRRU-IoT'
#CFG_BSSID_PASS='SrruIoT@2019'

CFG_BSSID='PNHome2'
CFG_BSSID_PASS='st11ae58*'

FRONT_LED = machine.Pin(2, machine.Pin.OUT)
REAR_LED = machine.Pin(16, machine.Pin.OUT)

FR = machine.Pin(5, machine.Pin.OUT)
FL = machine.Pin(4, machine.Pin.OUT)
#FRONT  = HCSR04(trigger_pin=12, echo_pin=14, echo_timeout_us=1000000)
#REAR  = HCSR04(trigger_pin=15, echo_pin=13, echo_timeout_us=1000000)


def __init__():
	print("INIT")
	print('Frequency ', machine.freq())
	FRONT_LED.value(1)
        REAR_LED.value(1)
        FR.value(1)
        FL.value(1)

def start_ap():
	ap = network.WLAN(network.AP_IF)
	mac = ubinascii.hexlify(ap.config('mac'),'').decode()
	ap.config(essid=CFG_APNAME+'-'+str(mac),password='micropythoN',channel=11)
	ap.ifconfig(('4.4.4.4', '255.255.255.0', '4.4.4.4', '1.1.1.1'))
	ap.active(True)
	
def do_connect():

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        if wlan.isconnected():
                print(wlan.ifconfig())
                return 
        
        if not wlan.isconnected():
                wlan.connect(CFG_BSSID,CFG_BSSID_PASS)
                c = 0
                while not wlan.isconnected():
                        time.sleep(1)
                        print('[',c,'] connecting ... to WLAN')
                        c = c + 1
                        FRONT_LED.value(c%2)
                        REAR_LED.value(c%2)
                        pass

def tracer_callback(t):
        print("Tracing ",t)
        
def start_my_car():

        print("StartMyCar")
        FR.value(0)
        FL.value(0)

        #while True:
                
                #time.sleep(0.10)
                #front_cm = FRONT.distance_cm()
                #if front_cm < 15:
                        #FRONT_LED.value(0)
                #else:
                        #FRONT_LED.value(1)

                #rear_cm = REAR.distance_cm()
                #if rear_cm < 15:
                        #REAR_LED.value(0)
                #else:
                        #REAR_LED.value(1)


if __name__ == '__main__':
        
	__init__()
	do_connect()

	FRONT_LED.value(1)
        REAR_LED.value(1)

        start_my_car()
	
        
