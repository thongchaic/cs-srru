import network
import dht
import machine 
import time
import urequests
import gc 
#import micropython

pms = machine.UART(2)
dhs = dht.DHT22(machine.Pin(4))

CFG_BSSID='SRRU-WiFi'
CFG_BSSID_PASS=''
START=time.ticks_ms()

def __init__():
    pms.init(9600,bits=8,parity=None,stop=1)
    gc.enable()

def do_connect():

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        if wlan.isconnected():
                #print(wlan.ifconfig())
                return True

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

def send_data(pm25, pm10, temp, humid):
    try:

        send_url = "https://surin.srru.ac.th/api/iot/data?token=431.2218518518519&device_id=6"
        if temp is not None:
                send_url = send_url+"&dht_temperature="+str(temp)
        if humid is not None:
                send_url = send_url+"&dht_humidity="+str(humid)
        if pm25 is not None:
                send_url = send_url+"&pm25="+str(pm25)
        if pm10 is not None:
                send_url = send_url+"&pm10="+str(pm10)

        urequests.get(send_url)
        return True
    except:
        return False
    return False
def calc_pms(x,y):
    pm = x
    pm <<= 8
    pm = pm | y
    return pm

def extract_pms(raw):
    try:
        pm10=None
        pm25=None
        for i, x in enumerate(raw):
            if i+9 < len(raw)-1 and x == 66 and raw[i+1] == 77:
                pm25 = calc_pms(raw[i+6],raw[i+7])
                pm10 = calc_pms(raw[i+8],raw[i+9])
                return pm25, pm10
    except:
        pass
    return None, None

def dht_sensing():
    temp=None
    humid=None
    try:
        dhs.measure()
        temp = dhs.temperature()
        humid = dhs.humidity()
    except:
        pass
    return temp, humid

def sening():
    raw = pms.read(42)
    pm25, pm10 = extract_pms(raw)    
    temp, humid = dht_sensing()
    return pm25, pm10, temp, humid


if __name__ == '__main__':
    __init__()
    while True:
        try:
            if do_connect():
                pm25, pm10, temp, humid = sening()
                print(pm25, pm10, temp, humid)
                c = 0      
                while not send_data(pm25, pm10, temp, humid) and c < 30:
                    c =  c + 1 
                    time.sleep(10)

                if c >= 30:
                    time.sleep(30)
                    machine.reset()


            diff = (time.ticks_ms()-START)/(1000*60)
            print(diff)
            if diff >= 240:
                time.sleep(5)
                machine.reset()
            
            time.sleep(15)
            gc.collect()

        except:
            time.sleep(30)
            machine.reset()
