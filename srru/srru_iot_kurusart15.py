import time
import machine
import network
import ubinascii
import urequests
import dht
from hcsr04 import HCSR04

#https://surin.srru.ac.th/api/iot/data?token=431.2218518518519&device_id=9&dht_temperature=27
#CFG_BSSID='SRRU-IoT'
#CFG_BSSID_PASS='SrruIoT@2019'


CFG_BSSID='CSOffice2'
CFG_BSSID_PASS=''


DHT_SENSOR = dht.DHT22(machine.Pin(5))
DISTANCE = HCSR04(trigger_pin=14,echo_pin=12)

def __init__():
    ap = network.WLAN(network.AP_IF)
    ap.active(False)

def do_connect():

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        if wlan.isconnected():
                print(wlan.ifconfig())
                return True

        
        if not wlan.isconnected():
                wlan.connect(CFG_BSSID, CFG_BSSID_PASS)
                c = 0
                d = 0
                while not wlan.isconnected():
                        time.sleep(1)
                        print('[',c,'] connecting ... to ',CFG_BSSID)
                        c = c + 1 
                        if c > 60:
                            wlan.connect(CFG_BSSID, CFG_BSSID_PASS)
                            d = d + 1
                            if d > 5:
                                return False
                        
        print(wlan.ifconfig())
        return True


def measurment():

        temp = None
        humid = None
        distance = None
        try:
	    DHT_SENSOR.measure()
	    temp = DHT_SENSOR.temperature()
	    humid  = DHT_SENSOR.humidity()
	except:
	    print("DHT ERROR....")
		
	try:
            distance = DISTANCE.distance_cm()
        except:
            print("distance error")
            
            
	return temp, humid, distance










    

	
def send_data(temp, humid, distance):
    print("sending => ",temp,",", humid,",",distance)
    send_url = "https://surin.srru.ac.th/api/iot/data?token=431.2218518518519&device_id=15"
    if temp is not None:
        send_url = send_url+"&dht_temperature="+str(temp)
    if humid is not None:
        send_url = send_url+"&dht_humidity="+str(humid)
    if distance is not None:
        send_url = send_url+"&hcsr04_distance="+str(distance)

    try:
        print(send_url)
        urequests.get(send_url)
    except:
        return False
    
    return True


def deep_sleep():
    print('Deep sleep...for .. 60s')
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, 60000)
    machine.deepsleep()

if __name__ == '__main__':
    __init__()
    while True:
        try:
            connected = do_connect()
            if connected:
                temp, humid, distance = measurment()
                c = 0
                while not send_data(temp, humid, distance):
                    print('Send data failed .. ',c)
                    time.sleep(5)
                    c = c + 1
                    if c > 5:
                        break
                
                time.sleep(5)
            else:
                #machine.reset()
                print("Exit")
                
        except:
            #machine.reset()
            print('error')
            break
