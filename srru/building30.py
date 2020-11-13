import network
import dht
import machine 
import time
import urequests
import gc 
#import micropython
import esp
#esp.osdebug(None)



class SrruIoT(object):

    def __init__(self,_id,bssid,bssid_pass):

        gc.enable()

        #self.buffer = bytearray(42)        
        self.pms = machine.UART(2)
        self.pms.init(9600,bits=8,parity=None,stop=1)
        self.dhs = dht.DHT22(machine.Pin(4))

        self.id = _id
        self.bssid = bssid 
        self.bssid_pass = bssid_pass
        self.start=time.ticks_ms()

    def do_connect(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        if wlan.isconnected():
            #print(wlan.ifconfig())
            return True

        wlan.connect(self.bssid, self.bssid_pass)
        c = 0
        while not wlan.isconnected():
            time.sleep(1)
            print('[',c,'] connecting ... to ',self.bssid)
            c = c + 1
            if c > 300:
                return False
            
        print(wlan.ifconfig())
        return True

    def send_data(self, pm25, pm10, temp, humid):
        try:

            send_url = "https://surin.srru.ac.th/api/iot/data?token=431.2218518518519&device_id="+self.id
            if temp is not None:
                send_url = send_url+"&dht_temperature="+str(temp)
            if humid is not None:
                send_url = send_url+"&dht_humidity="+str(humid)
            if pm25 is not None:
                send_url = send_url+"&pm25="+str(pm25)
            if pm10 is not None:
                send_url = send_url+"&pm10="+str(pm10)
            print(send_url)
            urequests.get(url=send_url,timeout=5)
            print("Return True......")
            return True
        except:
            print("-")
            #gc.collect()
            return False
        return False

    def calc_pms(self, x,y):
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
            #try:
                if self.do_connect():
                    pm25, pm10, temp, humid = self.sening()
                    print(pm25, pm10, temp, humid)
                    c = 0      
                    while not self.send_data(pm25, pm10, temp, humid) and c < 15:
                        c =  c + 1
                        print("try...",c,"..",gc.mem_free())
                        time.sleep(10)

                    if c >= 15:
                        time.sleep(30)
                        machine.reset()

                diff = (time.ticks_ms()-self.start)/(1000*60)
                print(diff)
                if diff >= 240:
                    machine.reset()
                
                time.sleep(2)
                gc.collect()

            #except:
            #    print("-.-")
            #    time.sleep(30)
            #    machine.reset()


if __name__ == '__main__':

    iot = SrruIoT("23","PNHome2","st11ae58*")
    iot.infinity()

