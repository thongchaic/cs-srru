import os 
import time
import machine
import network
import ubinascii
import urequests
import socket
from hcsr04 import HCSR04

CFG_BSSID='SRRU-IoT'
CFG_BSSID_PASS='SrruIoT@2019'
CFG_APNAME='IoTCar'
#CFG_BSSID='PNHome2'
#CFG_BSSID_PASS='st11ae58*'

FRONT_LED = machine.Pin(2, machine.Pin.OUT)
P1 = machine.Pin(16, machine.Pin.OUT)
P2 = machine.Pin(4, machine.Pin.OUT)

FRONT = HCSR04(trigger_pin=12, echo_pin=14, echo_timeout_us=1000000)

def __init__():
	print("INIT")
	print('Frequency ', machine.freq())
	FRONT_LED.value(1)
	stop()


def start_ap(is_on):
	ap = network.WLAN(network.AP_IF)
	mac = ubinascii.hexlify(ap.config('mac'),'').decode()
	ap.config(essid=CFG_APNAME+'-'+str(mac),password='micropythoN',channel=11)
	ap.ifconfig(('4.4.4.4', '255.255.255.0', '4.4.4.4', '1.1.1.1'))
	ap.active(is_on)
	
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
                        pass

def stop():
        print("stop")
        P1.on()
        P2.on()
         
def start_my_car():

        while True:
                front_cm = FRONT.distance_cm()
                print("Front=>", front_cm)
                if front_cm < 80:
                        P1.value(0)
                        P2.value(1)
			time.sleep(3)

                else:
                        P1.value(0)
                        P2.value(0)


                time.sleep(0.1)
                
                
if __name__ == '__main__':
        
	__init__()
	#start_ap(False)
	do_connect()
	FRONT_LED.value(1)
        start_my_car()
	
        
