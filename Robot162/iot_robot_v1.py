import os 
import time
import machine
import network
import ubinascii

from hcsr04 import HCSR04

CFG_BSSID='SRRU-WiFi'
CFG_BSSID_PASS='SrruIoT@2019'

FRONT_LED = machine.Pin(2, machine.Pin.OUT)
REAR_WHEEL = machine.Pin(16, machine.Pin.OUT)
FRONT  = HCSR04(trigger_pin=14, echo_pin=12, echo_timeout_us=1000000)


def __init__():
	print("INIT")
	print('Frequency ', machine.freq())
	FRONT_LED.value(1)
	ap = network.WLAN(network.AP_IF)
	mac = ubinascii.hexlify(ap.config('mac'),'').decode()
	ap.active(False)
	
def do_connect():

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        if wlan.isconnected():
                print(wlan.ifconfig())
                return 
        
        if not wlan.isconnected():
               # wlan.connect(CFG_BSSID,CFG_BSSID_PASS)
                wlan.connect(CFG_BSSID)
                c = 0
                while not wlan.isconnected():
                        time.sleep(1)
                        print('[',c,'] connecting ... to WLAN')
                        c = c + 1
                        FRONT_LED.value(c%2)
                        pass

        
def start_my_car():

        while True:
                front_cm = FRONT.distance_cm()
                print("Front=>", front_cm)
                time.sleep(1)



if __name__ == '__main__':
        
	__init__()
	do_connect()
        start_my_car()
	
        
