import os 
import time
import machine
import network
import ubinascii
import urequests
import socket


CFG_BSSID='SRRU-IoT'
CFG_BSSID_PASS='SrruIoT@2019'
CFG_APNAME='IoTCar'
#CFG_BSSID='PNHome2'
#CFG_BSSID_PASS='st11ae58*'

FRONT_LED = machine.Pin(2, machine.Pin.OUT)
P1 = machine.Pin(13, machine.Pin.OUT)
P2 = machine.Pin(15, machine.Pin.OUT)
P3 = machine.Pin(16, machine.Pin.OUT)


def __init__():
	print("INIT")
	print('Frequency ', machine.freq())
	FRONT_LED.value(1)
	stop()


def start_ap(is_on):
	ap = network.WLAN(network.AP_IF)
	mac = ubinascii.hexlify(ap.config('mac'),'').decode()
	ap.config(essid=CFG_APNAME+'-'+str(mac),password='micropythoN',channel=11)
	ap.ifconfig(('4.4.4.4', '255.255.255.0', '4.4.4.4', '1.1.1.1'))
	ap.active(is_on)
	
def do_connect():

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        if wlan.isconnected():
                print(wlan.ifconfig())
                return 
        
        if not wlan.isconnected():
                wlan.connect(CFG_BSSID,CFG_BSSID_PASS)
                c = 0
                while not wlan.isconnected():
                        time.sleep(1)
                        print('[',c,'] connecting ... to WLAN')
                        c = c + 1
                        FRONT_LED.value(c%2)
                        pass

def left():
        print("go left")
        P1.on()
        P2.on()
        P3.on()
def right():
        print("go right")
        P1.off()
        P2.off()
        P3.on()
def straight():
        print("go straight")
        P1.off()
        P2.on()
        P3.off()
def stop():
        print("stop")
        P1.off()
        P2.on()
        P3.on()
        
def start_web():
        print("Start WWW")
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 80))
        s.listen(5)
        while True:
                conn, addr = s.accept()
                print("connected from ...", str(addr))
                request = conn.recv(1024)
                request = str(request)
                #print('result = ', request.find('/?go=left'))
                if request.find('favicon.ico') > 0:
                        pass
                if request.find('/?go=left') > 0:
                        left()
                elif request.find('/?go=right') > 0:
                        right()
                elif request.find('/?go=straight') > 0:
                        straight()
                else:
                        stop()
                        
                html = """<HTML><BODY>
                        <table style="width:100%">
                                <tr><td style="color:green;"><a href="/?go=left">left</a></td><td style="color:yellow;"><a href="/?go=right">Right</a></td></tr>
                                <tr><td style="color:green;"><a href="/?go=straight">Straight</a></td><td style="color:yellow;"><a href="/?go=stop">Stop</a></td></tr>
                        </table></BODY></HTML>"""
                conn.send('HTTP/1.1 200 OK\n')
                conn.send('Content-Type: text/html\n')
                conn.send('Connection: close\n\n')
                conn.sendall(html)
                conn.close()
                
                
if __name__ == '__main__':
        
	__init__()
	#start_ap(False)
	do_connect()
	FRONT_LED.value(1)
        start_web()
	
        
