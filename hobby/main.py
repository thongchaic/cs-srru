import network
import machine
import time
import socket
import gc

addr = socket.getaddrinfo('0.0.0.0',80)[0][-1]
server = socket.socket()

RELAYS = [ machine.Pin(5,machine.Pin.OUT),
      machine.Pin(4,machine.Pin.OUT),
      machine.Pin(0,machine.Pin.OUT),
      machine.Pin(2,machine.Pin.OUT)]

def __init__():
    for r in RELAYS:
        r.off()
    ap = network.WLAN(network.AP_IF)
    ap.active(False)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("IoT","good2cu*99")
    t = 0
    while not wlan.isconnected():
        print("try to connect .." , t)
        time.sleep(2)
        t = t + 1

    wlan.ifconfig(("10.100.1.2","255.255.255.0","10.100.1.1","8.8.8.8"))
    print( wlan.ifconfig() )

def remote_controls():
    web = '''
    <!DOCTYPE html>
<html>
<head>
<title>Smart Home</title>
</head>
<body>
<script>
     function forward(){
          var req = new XMLHttpRequest();
          req.open("GET", "/?cmd=1", true);
          req.send(null);
     }
     function left(){
          var req = new XMLHttpRequest();
          req.open("GET", "/?cmd=2", true);
          req.send(null);
      }
      function backward(){
          var req = new XMLHttpRequest();
          req.open("GET", "/?cmd=3", true);
          req.send(null);
      }
      function stop(){
          var req = new XMLHttpRequest();
          req.open("GET", "/?cmd=0", true);
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
      width: 100%;
      height: 200px;
      background-color:#4bf542;
      border-radius: 40px;
      border: 2px solid #ffdd00;
      }
</style>
</head>
<body>
     <h1>CS-SRRU</h1>
     <table width="100%" border=0>
       <tr>
            <td colspan="2"> <button onclick="forward()"><h1>Switch1</h1></button> </td>
           </tr>
           <tr>
             <td> <button  onclick="backward()"><h1>Switch2</h1></button> </td>
             <td> <button  onclick="stop()"><h1>Switch3</h1></button> </td>
           </tr>
              <tr>
              <td colspan="3"><button onclick="left()"><h1>Pump</h1></button> </td>
            </tr>
         </table> 
<br><br>
</body>
</html>
    '''
    
    server.bind(addr)
    server.listen(1)
    
    print("Robot Interface Started!!")
    while True:
        try:
            c, a = server.accept()
            f = c. makefile('rwb', 0)
            index = -1
            while True:
                line = f.readline()
                if not line or line == b'\r\n':
                    break
                tmp = str(line)
                
                if "GET /?cmd=0" in tmp:
                    index = 0
                elif "GET /?cmd=1" in tmp:
                    index = 1
                elif "GET /?cmd=2" in tmp:
                    index = 2
                elif "GET /?cmd=3" in tmp:
                    index = 3
                elif "favicon.ico" in tmp:
                    index = -2
                    
            if index == -1:
                c.send("HTTP/1.0 200 OK\r\nContent-type: text/html; charset=utf-8\r\n\r\n")
                c.sendall(web)
                c.close()
            elif index == -2:
                c.send("HTTP/1.0 204 OK\r\n\r\n")
                c.close()
            else:
                toggle(index,a)
                c.send("HTTP/1.0 204 OK\r\n\r\n")
                c.close()
        except:
            for r in RELAYS:
                r.off()
            gc.collect()
            
def toggle(i,a):
    print(i,"=>",RELAYS[i].value(),":",a)
    if RELAYS[i].value() == 1:
        RELAYS[i].off()
    else:
        RELAYS[i].on()
        
if __name__ == '__main__':
    __init__()
    remote_controls()

