import network
import dht
import machine 
import time
#import urequests
import gc 
import urandom
#import micropython
from umqtt.simple import MQTTClient
import esp
esp.osdebug(False)


class SrruIoT(object):
    def __init__(self,_id,client,bssid,bssid_pass):
        
        gc.enable()
        self.pms = machine.UART(2)
        self.pms.init(9600,bits=8,parity=None,stop=1)
        self.dhs = dht.DHT22(machine.Pin(4))
        self.station_id = _id
        self.CFG_BSSID=bssid
        self.CFG_BSSID_PASS=bssid_pass
        self.START=time.ticks_ms()
        self.MQTT = MQTTClient(client,"mqtt.srru.ac.th",1883,"miot","SrruMIoT@2019")


    def do_connect(self):

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        if wlan.isconnected():
                #print(wlan.ifconfig())
                return True

        wlan.connect(self.CFG_BSSID, self.CFG_BSSID_PASS)
        c = 0
        while not wlan.isconnected():
                time.sleep(1)
                print('[',c,'] connecting ... to ',self.CFG_BSSID)
                c = c + 1
                if c > 300:
                        return False
        
        print(wlan.ifconfig())
        return True

    def publish_data(self, pm25, pm10, temp, humid):
        try:
            print("pub-->",pm25, pm10, temp, humid)
            return True
        except:
            return False
        return False
    
    def calc_pms(self, x, y):
        pm = x
        pm <<= 8
        pm = pm | y
        return pm

    def extract_pms(self, raw):
        try:
            pm10=None
            pm25=None
            for i, x in enumerate(raw):
                if i+9 < len(raw)-1 and x == 66 and raw[i+1] == 77:
                    pm25 = self.calc_pms(raw[i+6],raw[i+7])
                    pm10 = self.calc_pms(raw[i+8],raw[i+9])
                    return pm25, pm10
        except:
            pass
        return None, None

    def dht_sensing(self):
        temp=None
        humid=None
        try:
            self.dhs.measure()
            temp = self.dhs.temperature()
            humid = self.dhs.humidity()
        except:
            pass
        return temp, humid

    def sening(self):
        raw = self.pms.read(42)
        pm25, pm10 = self.extract_pms(raw)    
        temp, humid = self.dht_sensing()
        return pm25, pm10, temp, humid

    def infinity(self):
        while True:
##            try:
                if self.do_connect():
                    pm25, pm10, temp, humid = self.sening()
                    self.publish_data(pm25, pm10, temp, humid)
##                    c = 0      
##                    while not send_data(pm25, pm10, temp, humid) and c < 30:
##                        c =  c + 1 
##                        time.sleep(10)
##
##                    if c >= 30:
##                        time.sleep(30)
##                        machine.reset()
##
##
##                diff = (time.ticks_ms()-START)/(1000*60)
##                print(diff)
##                if diff >= 180:
##                    time.sleep(5)
##                    machine.reset()
                
                time.sleep(5)
                gc.collect()

##            except:
##                print("Except")
##                time.sleep(30)
##                machine.reset()

        

if __name__ == '__main__':
    #_id,bssid,bssid_pass
    w=network.WLAN(network.STA_IF)
    w.active(True)
    w.connect("CSOffice2")

    iot = SrruIoT("23",str(urandom.getrandbits(30)),"CSOffice2","")
    iot.infinity()
    

