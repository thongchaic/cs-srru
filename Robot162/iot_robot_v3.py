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

FRONT_LED = machine.Pin(2, machine.Pin.OUT)
P1 = machine.Pin(16, machine.Pin.OUT)
P2 = machine.Pin(4, machine.Pin.OUT)
FRONT = HCSR04(trigger_pin=12, echo_pin=14, echo_timeout_us=1000000)

def __init__():
	print("INIT")
	print('Frequency ', machine.freq())
	FRONT_LED.value(1)
	ap = network.WLAN(network.AP_IF)
	ap.active(False)

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
	FRONT_LED.value(0)
    P1.on()
    P2.on()

def forward():
	print("forward....")
	P1.on()
	P2.off()

def backward():
	print("backward....")
	#P1.off()
	#P2.off()

def start_my_car():

	while True:
 		front_cm = FRONT.distance_cm()
		print("Front=>", front_cm)
		if front_cm < 80:
			stop()
		else:
			forward()

		time.sleep(0.5)


if __name__ == '__main__':

	__init__()
	#start_ap(False)
	#do_connect()
	start_my_car()
