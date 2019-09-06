import os
import time
import machine
import network
import ubinascii
import urequests
import socket

#driver for distance_cm()
from hcsr04 import HCSR04

CFG_BSSID='SRRU-IoT'
CFG_BSSID_PASS='SrruIoT@2019'

FRONT_LED = machine.Pin(2, machine.Pin.OUT)
P1 = machine.Pin(16, machine.Pin.OUT)
P2 = machine.Pin(5, machine.Pin.OUT)
P3 = machine.Pin(4, machine.Pin.OUT)
P4 = machine.Pin(0, machine.Pin.OUT)

FRONT = HCSR04(trigger_pin=12, echo_pin=14, echo_timeout_us=1000000)

def __init__():
    print("INIT")
    print('Frequency ', machine.freq())
    FRONT_LED.value(1)
    ap = network.WLAN(network.AP_IF)
    ap.active(False)

def stop():
    print("stop")
    FRONT_LED.value(0)
    P1.on()
    P2.on()
    P3.on()
    P4.on()

def forward():
    print("forward....")
    P1.on()
    P2.off()
    P3.off()
    P4.on()

def backward(t=0):
    print("backward....")
    P1.off()
    P2.on()
    P3.on()
    P4.off()
    time.sleep(t)
    stop()

def turn_left(t=0):
    print("Left....")
    P1.on()
    P2.off()
    P3.on()
    P4.on()
    time.sleep(t)
    stop()

def turn_right(t=0):
    print("Right....")
    P1.on()
    P2.on()
    P3.off()
    P4.on()
    time.sleep(t)
    stop()

def start_my_car():
    while True:
 	front_cm = FRONT.distance_cm()
	print("Front=>", front_cm)
	if front_cm < 20:
	    stop()
	    time.sleep(2)
	    turn_left(4)
	
	else:
	    forward()

	time.sleep(0.5)

if __name__ == '__main__':

    __init__()
    start_my_car()

