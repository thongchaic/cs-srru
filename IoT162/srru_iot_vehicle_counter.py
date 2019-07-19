import os 
import time
import machine
import network
import ubinascii
import urequests
import socket
from hcsr04 import HCSR04

FRONT_LED = machine.Pin(2, machine.Pin.OUT)
FRONT = HCSR04(trigger_pin=12, echo_pin=14, echo_timeout_us=1000000)

def __init__():
	print("INIT")
	print('Frequency ', machine.freq())
	FRONT_LED.value(1)
	ap = network.WLAN(network.AP_IF)
	mac = ubinascii.hexlify(ap.config('mac'),'').decode()
	ap.config(essid=CFG_APNAME+'-'+str(mac),password='micropythoN',channel=11)
	ap.ifconfig(('4.4.4.4', '255.255.255.0', '4.4.4.4', '1.1.1.1'))
	ap.active(False)
