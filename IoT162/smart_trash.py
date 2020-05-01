from hcsr04 import HCSR04
import time
import machine
import network
import ubinascii
import dht
import gc


distance=HCSR04(trigger_pin=14,echo_pin=12)
servo = machine.PWM(machine.Pin(2),freq=100)
def __init__():
    gc.enable()
    ap = network.WLAN(network.AP_IF)
    ap.active(False)
    servo.duty(1)
    #servo.duty(0)

def main():
    opened = False
    while True:
        d = distance.distance_cm()
        print(d, opened)
        if d <= 60 and not opened:
            servo.duty(155)
            opened = True
        if d > 60 and opened:
            servo.duty(1)
            opened = False
            #servo.duty(0)
        time.sleep(1)
        
if __name__ == '__main__':
    __init__()
    main()
    
