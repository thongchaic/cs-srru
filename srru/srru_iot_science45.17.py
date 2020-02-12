import time
import machine
import network
import ubinascii
import urequests
import dht
import gc 

#CFG_BSSID='SRRU-IoT'
#CFG_BSSID_PASS='SrruIoT@2019'

DEVICE_ID='17'
CFG_BSSID='CSOffice2'
CFG_BSSID_PASS=''


DHT_SENSOR = dht.DHT22(machine.Pin(5))


def __init__():
    gc.enable()
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
                while not wlan.isconnected():
                        time.sleep(1)
                        print('[',c,'] connecting ... to ',CFG_BSSID)
                        c = c + 1
                        if c > 300:
                            return False
                        
        print(wlan.ifconfig())
        return True


def measurment():

        temp = None
        humid = None

        try:
		DHT_SENSOR.measure()
		temp = DHT_SENSOR.temperature()
		humid  = DHT_SENSOR.humidity()
	except:
		print("DHT ERROR....")

	return temp, humid

	
def send_data(temp, humid):
    print(DEVICE_ID,"_sending => ",temp, humid)
    send_url = "https://surin.srru.ac.th/api/iot/data?token=431.2218518518519&device_id="+str(DEVICE_ID)
    if temp is not None:
        send_url = send_url+"&dht_temperature="+str(temp)
    if humid is not None:
        send_url = send_url+"&dht_humidity="+str(humid)

    try:
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

def reset_machine():
    gc.collect()
    time.sleep(3)
    machine.reset()
    
if __name__ == '__main__':
    __init__()
    while True:
        try:
            connected = do_connect()
            if connected:
                temp, humid = measurment()
                c = 0
                while not send_data(temp, humid):
                    print('Send data failed .. ',c)
                    time.sleep(10)
                    c = c + 1
                    if c > 6:
                        reset_machine()
                
                time.sleep(30)
            else:
                reset_machine()
                
        except:
            reset_machine()
