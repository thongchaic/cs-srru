import os
import time
import machine
import network
import ubinascii
import urequests
from MQ2 import MQ2
import dht


CFG_BSSID='SRRU-IoT'
CFG_BSSID_PASS='SrruIoT@2019'

FRONT_LED = machine.Pin(2, machine.Pin.OUT)
DHT_SENSOR = dht.DHT22(machine.Pin(5))
LDR_SENSOR = machine.Pin(14, machine.Pin.IN)
MQ2_SENSOR = MQ2(pinData=0,baseVoltage=3.3)

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

def measurment():


        temp = None
        humid = None
	smoke = None
	lpg = None
	methane = None
	hydrogen = None
	ldr = None 
	try:
                print("Start DHT sensor")
		FRONT_LED.value(0)
		DHT_SENSOR.measure()
		temp = DHT_SENSOR.temperature()
		humid  = DHT_SENSOR.humidity()
		FRONT_LED.value(1)
	except:
		print("DHT ERROR....")
		FRONT_LED.value(1)
		
	try:
                print("Reading LDR...")
                ldr = LDR_SENSOR.value()
        except:
                print("LDR Error")

	try:
                print("Start MQ2 sensor")
		FRONT_LED.value(0)
		MQ2_SENSOR.calibrate()
		print("reading smoke ...")
		smoke = MQ2_SENSOR.readSmoke()
		print("reading lpg....")
		lpg = MQ2_SENSOR.readLPG()
		print("reading methane...")
		methane = MQ2_SENSOR.readMethane()
		print("reading hydrogen...")
		hydrogen = MQ2_SENSOR.readHydrogen()
		FRONT_LED.value(1)
	except:
		print("MQ2 ERROR")
		FRONT_LED.value(1)

        print("data measured, ", temp,", ",humid,smoke,lpg,methane,hydrogen, ldr)
        return temp, humid, smoke, lpg, methane, hydrogen, ldr

def send_data(temp, humid, smoke, lpg, methane, hydrogen, ldr):
        print("sending humid=",humid,", temp=",temp)
        send_url = "https://surin.srru.ac.th/api/iot/data?token=431.2218518518519&device_id=13"
        if temp is not None:
                send_url = send_url+"&dht_temperature="+str(temp)
        if humid is not None:
                send_url = send_url+"&dht_humidity="+str(humid)
        if smoke is not None:
                send_url = send_url+"&smoke="+str(smoke)
        if lpg is not None:
                send_url = send_url+"&lpg="+str(lpg)
        if methane is not None:
                send_url = send_url+"&methane="+str(methane)
        if hydrogen is not None:
                send_url = send_url+"&hydrogen="+str(hydrogen)
        if ldr is not None:
                send_url = send_url+"&ldr="+str(ldr)
                
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
		temp, humid, smoke, lpg, methane, hydrogen, ldr = measurment()
                c = 0
                while not send_data(temp, humid, smoke, lpg, methane, hydrogen, ldr):
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
	deep_sleep()
