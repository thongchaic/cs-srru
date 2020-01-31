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

servo = machine.PWM(machine.Pin(2), freq=1000)


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
        
def start_servo():
        i = 0
        while i < 1023:
                print("duty = ",str(i))
                servo.duty(i)
                blink_led(5,0.1)
                time.sleep(3)
                servo.duty(0)
                i = i + 1
        
if __name__ == '__main__':

	__init__()
	connected = do_connect()

	if connected:
                start_servo()
                        
