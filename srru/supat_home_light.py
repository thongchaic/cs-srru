import os
import time
import machine
import network
import ubinascii

FRONT_LED = machine.Pin(2, machine.Pin.OUT)
LIGHT = machine.Pin(14,machine.Pin.IN)
RELAY = machine.Pin(12, machine.Pin.OUT)

def __init__():
    FRONT_LED.value(1)
    ap = network.WLAN(network.AP_IF)
    mac = ubinascii.hexlify(ap.config('mac'),'').decode()
    ap.config(essid='SUPAT_Home',password='micropythoN',channel=11)
    ap.ifconfig(('4.4.4.4', '255.255.255.0', '4.4.4.4', '1.1.1.1'))
    ap.active(True)
    ap.ifconfig()

def start_mon():
    RELAY.off()
    D = 0 
    while True:
        try:
            L = LIGHT.value()
            print(L)
            if L == 1:
                RELAY.on()
            else:
                RELAY.off()
        except:
            print("ERR") 

        time.sleep(10)
                
if __name__ == '__main__':
    __init__()
    start_mon()

