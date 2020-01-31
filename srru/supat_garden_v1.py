import os
import time
import machine
import network
import ubinascii
import urequests
#from MQ2 import MQ2
#import dht


#CFG_BSSID='PNHome2'
#CFG_BSSID_PASS='st11ae58*'
THRESHOLD=790

FRONT_LED = machine.Pin(2, machine.Pin.OUT)
#DHT_SENSOR = dht.DHT22(machine.Pin(5))
#MQ2_SENSOR = MQ2(pinData=0,baseVoltage=5.0)
RELAY = machine.Pin(4, machine.Pin.OUT)
SOIL = machine.ADC(0)

def __init__():
	FRONT_LED.value(1)
	ap = network.WLAN(network.AP_IF)
	mac = ubinascii.hexlify(ap.config('mac'),'').decode()
	ap.config(essid='SUPAT_'+str(mac),password='micropythoN',channel=11)
	ap.ifconfig(('4.4.4.4', '255.255.255.0', '4.4.4.4', '1.1.1.1'))
	ap.active(True)
        ap.ifconfig()

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
        

def send_data(soil_moise):
        connected = do_connect()
        if connected:
                blink_led(10,0.05)
                print("sending humid=",soil_moise)
                send_url = "https://surin.srru.ac.th/api/iot/data?token=x&device_id=y"
                if soil_moise is not None:
                        send_url = send_url+"&soil_moise="+str(soil_moise)
                        urequests.get(send_url)
        return True

def deep_sleep():
        print('Deep sleep...for .. 5min')
        rtc = machine.RTC()
        rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
        rtc.alarm(rtc.ALARM0, 300000)
        machine.deepsleep()

def start_mon():
        blink_led(10,0.05)
        RELAY.off()
        c = 0
        sm = 0
        
        #while c < 10:
        #        c = c + 1
        #        tmp = SOIL.read()
        #        print(c," : ", tmp)
        #        sm = sm + tmp
        #        time.sleep(1)
        #avg_sm = sm/10
        #print("avg_sm=",avg_sm)
        while True:
                avg_sm = SOIL.read()
                if avg_sm <= THRESHOLD:
                    print("moise ok=> ",avg_sm)
                    RELAY.off()
                else:
                    print("On => ", avg_sm)
                    RELAY.on()
                time.sleep(1)
        #        sm = SOIL.read()
        #        blink_led(25,0.05)
        #        time.sleep(10) 
        #        deep_sleep()
        #else:
        #    print("dry relay on!")
        #    RELAY.on()       
        #RELAY.on()
    

        #while True:
        #        soil_moise = SOIL.read()
        #        if soil_moise <= THRESHOLD:
        #                RELAY.off()
        #                send_data(soil_moise)
        #                blink_led(25,0.05)
        #                time.sleep(10)
        #                deep_sleep()
        #        time.sleep(1)
                

if __name__ == '__main__':

	__init__()
	FRONT_LED.value(1)
	start_mon()

