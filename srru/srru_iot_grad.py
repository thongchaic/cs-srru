import time
import machine
import network
import ubinascii
import urequests
import dht

#https://surin.srru.ac.th/api/iot/data?token=431.2218518518519&device_id=9&dht_temperature=27
CFG_BSSID='SRRU-IoT'
CFG_BSSID_PASS='SrruIoT@2019'

DHT_SENSOR = dht.DHT22(machine.Pin(5))


def __init__():
    ap = network.WLAN(network.AP_IF)
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

        try:
		DHT_SENSOR.measure()
		temp = DHT_SENSOR.temperature()
		humid  = DHT_SENSOR.humidity()
	except:
		print("DHT ERROR....")

	return temp, humid

	
def send_data(temp, humid):
    print("sending => ",temp, humid)
    send_url = "https://surin.srru.ac.th/api/iot/data?token=431.2218518518519&device_id=19"
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
                    time.sleep(15)
                    c = c + 1
                    if c > 5:
                        break
                
                time.sleep(30)
                
        except:
            print("fatal error")
            time.sleep(60)


            
