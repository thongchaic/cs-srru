import os
import time
import machine
import network
import ubinascii
import urequests
import socket 
import dht


CFG_BSSID='SRRU-IoT'
CFG_BSSID_PASS='SrruIoT@2019'

FRONT_LED = machine.Pin(2, machine.Pin.OUT)
DHT_SENSOR = dht.DHT22(machine.Pin(5))
#SOIL_SENSOR = machine.ADC(0)
RELAY = machine.Pin(4,machine.Pin.OUT)
HOST = socket.getaddrinfo('0.0.0.0',80)[0][-1]

def __init__():
	ap = network.WLAN(network.AP_IF)
        ap.active(True)
        #ap.ifconfig(('4.4.4.4','255.255.255.0','4.4.4.1','8.8.8.8'))
        ap.config(essid="SRRU_WaterPump")
        ap.ifconfig()
	FRONT_LED.value(1)

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

            tmp = str(line)
            if "GET /?led=on" in tmp:
                RELAY.on()
            elif "GET /?led=off" in tmp:
                RELAY.off()
        
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
    temp = 0
    humid =0
    try:
        DHT_SENSOR.measure()
        temp = DHT_SENSOR.temperature()
        humid  = DHT_SENSOR.humidity()
        print(temp, humid)
    except:
        print("dht error")

    html = """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none;
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}</style></head><body> <h1>SRRU BigData</h1>
  <p>Status: <strong>""" + gpio_state + """</strong></p><p><a href="/?led=on"><button class="button">ON</button></a></p>
  <p><a href="/?led=off"><button class="button button2">OFF</button></a></p>
  <p>Temp: <strong>""" + str(temp) + """</strong>, Humid: <strong>"""+ str(humid) + """</strong></p>
  </body></html>"""
    return html

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
def blink_led(t=1,d=0.1):
        while t >= 0:
                FRONT_LED.value(t%2)
                t = t - 1 
                time.sleep(d)
        FRONT_LED.value(1)
        
def measurment():
 
        temp = None
        humid = None
        soil = None
        
        try:
                blink_led(10,0.05)
                DHT_SENSOR.measure()
                temp = DHT_SENSOR.temperature()
                humid  = DHT_SENSOR.humidity()

        except:
                print("DHT sensor failed!!")

        try:
                blink_led(5, 0.1)
                soil = SOIL_SENSOR.read()
        except:
                print("Soil sensor failed!!")
                
        print("data => ", temp,", ",humid,", ",soil)
        
        return temp, humid, soil

def send_data(temp,humid):

        try:
                print("sending humid=",humid,", temp=",temp)
                send_url = "https://surin.srru.ac.th/api/iot/data?token=431.2218518518519&device_id=0"
                if temp is not None:
                        send_url = send_url+"&dht_temperature="+str(temp)
                if humid is not None:
                        send_url = send_url+"&dht_humidity="+str(humid)
                urequests.get(send_url)
                return True
        except:
                print("Failed to send temp,humid of (",temp,",",humid,")")
                      
        return False

def deep_sleep():
        print('Deep sleep...for .. 20s')
        rtc = machine.RTC()
        rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
        rtc.alarm(rtc.ALARM0, 20000)
        machine.deepsleep()
        
if __name__ == '__main__':

	__init__()
        start_http_server()
