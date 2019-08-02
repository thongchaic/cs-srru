import os 
import time
import machine
import network
import ubinascii
import urequests
from hcsr04 import HCSR04

sensor  = HCSR04(trigger_pin=12, echo_pin=14, echo_timeout_us=1000000)
D5 = machine.Pin(5,machine.Pin.OUT)

def __init__():
    print("INIT")
    D5.off()
    ap = network.WLAN(network.AP_IF)
    ap.active(False)

def stop():
    print("stop...")
    D5.on()

def forward():
    print("forward ...")
    D5.off()

def start_my_car():
    while True:
        front_cm = sensor.distance_cm()
        print("distance = ",front_cm)
        if front_cm < 15:
            stop()
        else:
            forward()

        time.sleep(1)


if __name__ == '__main__':
    __init__()
    start_my_car()
	
        
