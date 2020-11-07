import network
import dht
import machine 
import time
import urequests
import gc 
#import micropython
import esp
import onewire
import ds18x20
import socket

addr = socket.getaddrinfo('0.0.0.0',80)[0][-1]
server = socket.socket()
esp.osdebug(None)

class PNHome(object):

    def __init__(self,_id,bssid,bssid_pass):

        gc.enable()
        self.id = _id
        self.bssid = bssid 
        self.bssid_pass = bssid_pass
        self.start=time.ticks_ms()
        self.N1 = machine.Pin(14,machine.Pin.OUT)
        self.N2 = machine.Pin(12,machine.Pin.OUT)
        self.N1.off()
        self.N2.off()
        self.ds = ds18x20.DS18X20(onewire.OneWire( machine.Pin(2) ))
        self.roms = self.ds.scan()


    def do_connect(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        if wlan.isconnected():
            return True

        wlan.connect(self.bssid, self.bssid_pass)
        c = 0
        while not wlan.isconnected():
            time.sleep(1)
            c = c + 1
            if c > 300:
                return False
            
        wlan.ifconfig( ('192.168.1.74', '255.255.255.0', '192.168.1.1', '1.1.1.1') )
        print(wlan.ifconfig())
        return True

    def deep_sleep(self):
        print('Deep sleep...')
        rtc = machine.RTC()
        rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
        rtc.alarm(rtc.ALARM0, 1000*60*5)
        machine.deepsleep()
    
    def html(self):
        html = """
<!DOCTYPE html>
<html>
<head>
<title>PNHome</title>
</head>
<body>
<script>
     function relay(val){
          var req = new XMLHttpRequest();
          req.open("GET", "/?relay="+val, true);
          req.send(null);
     }
</script> 
<style>
tr,td,h1 {
   text-align: center;
}
h1{
    color:red;
    }
button{
      width: 100px;
      height: 70px;
      background-color:#FF7F50;
      border-radius: 40px;
      border: 2px solid #ffdd00;
      }
</style>
</head>
<body>
    <h1>PNHome</h1>
    
    <table width="100%" border=0>
        <tr>
            <td> <button onclick="relay(1)">Pump</button> </td>
        </tr>

        <tr>
            <td><button onclick="relay(2)">UV</button> </td>
        </tr>
    </table> 
<br><br>
<p>
    61191440109 <br>
    Pranee Maithong
    </p>

    61191440114 <br>
    Katunyuta Srikruedam
    </p>
</body>
</html>
        """
        return html 

    def sening(self):
        self.ds.convert_temp()
        time.sleep_ms(750)
        tmp = None
        for rom in self.roms:
            tmp = self.ds.read_temp(rom)
        return tmp
    
    def infinity(self):
        server.bind(addr)
        server.listen(1)
        
        while True:
            try:
                c, a = server.accept()
                print("request from => ", a)
                f = c. makefile('rwb', 0)
                relay = -1
                while True:
                    line = f.readline()
                    print(line)
                    if not line or line == b'\r\n':
                        break
                
                

            except:
                print("-.-")
                break
                #gc.collect()
                #time.sleep(60)
                #machine.reset()

if __name__ == '__main__':

    while True:
        try:
            iot = PNHome("","PNHome2","st11ae58*")
            iot.infinity()
        except:
            pass
            #machine.reset()

            
