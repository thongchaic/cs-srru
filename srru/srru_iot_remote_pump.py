import os
import time
import machine
import network
import ubinascii
import urequests
import socket 
import dht
import _thread


DHT_SENSOR = dht.DHT22(machine.Pin(23))
WATER_SENSOR = machine.ADC(machine.Pin(34))
RELAY = machine.Pin(22,machine.Pin.OUT)
HOST = socket.getaddrinfo('0.0.0.0',80)[0][-1]
MANUAL=False

def __init__():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    #ap.ifconfig(('4.4.4.4','255.255.255.0','4.4.4.1','8.8.8.8'))
    ap.config(essid="SRRU_AutoPump")
    ap.ifconfig()

    #w=network.WLAN(network.STA_IF)
    #w.active(True)
    #w.connect("PNHome2","st11ae58*")

def start_sensors():
    print("Start Sensors...")
    while True:
        water = WATER_SENSOR.read()
        #print("Water=",water)
        if water < 2000:
            RELAY.on()
        else:
            RELAY.off()

        time.sleep(1)

def start_http_server():
    print("Http server started!")
    sock = socket.socket()
    sock.bind(HOST)
    sock.listen(1)
    
    while True:
        cl, addr = sock.accept()
        #print("connection from ",cl, ", Addr = ",addr)
        client_file = cl.makefile('rwb',0)
        status = "ON" 
        while True:
            line = cl.readline()
            if not line or line == b'\r\n':
                break
            #print(line)
            #tmp = str(line)
            #if "GET /?led=on" in tmp:
            #    print("ON")
            #    RELAY.on()
            #elif "GET /?led=off" in tmp:
            #    print("OFF")
            #    RELAY.off()
            #elif "GET /?mode=auto" in tmp:
            #    print("Auto")
            #    RELAY.off()
            #    MANUAL=False
            # elif "GET /?mode=manual" in tmp:
            #    print("Manual")
            #    RELAY.off()
            #    MANUAL=True
        
        res=web_page()
        cl.send("HTTP/1.1 200 OK\n")
        cl.send("Content-Type: text/html\n")
        cl.send("Connection: close\n\n")
        cl.sendall(res)
        cl.close()

def web_page():
    if RELAY.value() == 1:
        gpio_state="ON"
    else:
        gpio_state="OFF"
    temp=0
    humid=0
    try:
        DHT_SENSOR.measure()
        temp = DHT_SENSOR.temperature()
        humid  = DHT_SENSOR.humidity()
    except:
        temp = 0 
        humid = 0
    water = WATER_SENSOR.read()
    #print(water, temp, humid)

    html = """<html><head>
     <meta http-equiv="refresh" content="15">
    <title>SRRU BigData</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none;
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}</style></head><body> <h1>SRRU BigData</h1>
  <p>Pump: <strong>""" + gpio_state + """</strong></p>
  <p>Water: <strong>""" + str(water) + """</strong></p>
  <p>Temp: <strong>""" + str(temp) + """</strong>, Humid: <strong>"""+ str(humid) + """</strong></p>
  <table border="0">
    <tr>
        <td></td>
        <td></td>
    <tr>
        <td></td>
        <td></td>
    </tr>
  </table>
  </body></html>"""

    return html
 
if __name__ == '__main__':

	__init__()
        _thread.start_new_thread(start_http_server,())
        _thread.start_new_thread(start_sensors,())

