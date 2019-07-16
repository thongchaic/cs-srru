import os
import time
import machine
import network
import ubinascii
import urequests
from MQ7 import MQ7
import dht


CFG_BSSID='PNHome2'
CFG_BSSID_PASS='st11ae58*'

FRONT_LED = machine.Pin(2, machine.Pin.OUT)
DHT_SENSOR = dht.DHT22(machine.Pin(5))
MQ7_SENSOR = MQ2(pinData=0,baseVoltage=3.3)

def __init__():
	FRONT_LED.value(1)

def start_ap():
	ap = network.WLAN(network.AP_IF)
	#mac = ubinascii.hexlify(ap.config('mac'),'').decode()
	#ap.config(essid=CFG_APNAME+'-'+str(mac),password='micropythoN',channel=11)
	#ap.ifconfig(('4.4.4.4', '255.255.255.0', '4.4.4.4', '1.1.1.1'))
	ap.active(False)

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
                
def measurment():


        temp = None
        humid = None
	carbon_m = None
	try:
                print("Start DHT sensor")
		blink_led(5,0.1)
		DHT_SENSOR.measure()
		temp = DHT_SENSOR.temperature()
		humid  = DHT_SENSOR.humidity()
	except:
		print("DHT ERROR....")
		FRONT_LED.value(1)
		

	try:
                print("Start MQ7")
		blink_led(25,0.05)
		MQ7_SENSOR.calibrate()
                print("reading smoke ...")
                blink_led(25,0.05)
                carbon_m = MQ7_SENSOR.readCarbonMonoxide()
	except:
		print("MQ2 ERROR")
		FRONT_LED.value(1)

        print("data measured, ", temp, humid, carbon_m)
        return temp, humid, carbon_m

def send_data(temp, humid, carbon_m):
        print("sending humid=",temp, humid, carbon_m)
        blink_led(10,0.1)
        send_url = "https://surin.srru.ac.th/api/iot/data?token=431.2218518518519&device_id=11"
        if temp is not None:
                send_url = send_url+"&dht_temperature="+str(temp)
        if humid is not None:
                send_url = send_url+"&dht_humidity="+str(humid)
        if carbon_m is not None:
                send_url = send_url+"&carbon_monoxide="+str(carbon_m)

        urequests.get(send_url)
        return True

def deep_sleep():
        print('Deep sleep...for .. 60s')
        rtc = machine.RTC()
        rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
        rtc.alarm(rtc.ALARM0, 90000)
        machine.deepsleep()

if __name__ == '__main__':

	__init__()
	start_ap()

	FRONT_LED.value(1)

	connected = do_connect()

	if connected:

                FRONT_LED.value(1)
		temp, humid, carbon_m = measurment()
                c = 0
                while not send_data(temp, humid, carbon_m):
                        print('Send data failed .. ',c)
                        time.sleep(3)
                        c = c + 1
                        if c > 5:
                                FRONT_LED.value(0)
                                break
                        pass
        FRONT_LED.value(1)
        print("Code update gap")
        time.sleep(10)
	#deep_sleep()
