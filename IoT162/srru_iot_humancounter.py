import os
import time
import machine
import network
import ubinascii
from hcsr04 import HCSR04

FRONT_LED = machine.Pin(2, machine.Pin.OUT)
SENSOR = HCSR04(trigger_pin=14,echo_pin=12)

def __init__():
    FRONT_LED.value(1)
    ap = network.WLAN(network.AP_IF)
    #mac = ubinascii.hexlify(ap.config('mac'),'').decode()
    #ap.config(essid='SUPAT_Home',password='micropythoN',channel=11)
    #ap.ifconfig(('4.4.4.4', '255.255.255.0', '4.4.4.4', '1.1.1.1'))
    ap.active(False)
    #ap.ifconfig()

def start_mon():
    passed=False
    human = 0 
    while True:
	d=SENSOR.distance_cm() 
        if not passed:
            print(d," => not passed...")
            if d < 95:
                passed = True
        else:
            print(d," => human found...")
            if d >= 95:
                passed = False 
                human = human + 1 
        
        time.sleep(0.5)
        print("human=",human)

if __name__ == '__main__':
    __init__()
    start_mon()

