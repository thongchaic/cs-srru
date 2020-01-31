import os
import time
import machine
import network
import ubinascii
import urequests
import socket
from hcsr04 import HCSR04

import socket 

SERVER = socket.getaddrinfo('0.0.0.0',80)[0][-1]

CFG_BSSID='SRRU-IoT'
CFG_BSSID_PASS='SrruIoT@2019'

FRONT_LED = machine.Pin(2, machine.Pin.OUT)
P1 = machine.Pin(16, machine.Pin.OUT)
P2 = machine.Pin(5, machine.Pin.OUT)
P3 = machine.Pin(4, machine.Pin.OUT)
P4 = machine.Pin(0, machine.Pin.OUT)

FRONT = HCSR04(trigger_pin=12, echo_pin=14, echo_timeout_us=1000000)

def __init__():
    print("INIT")
    print('Frequency ', machine.freq())
    FRONT_LED.value(1)
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="TC_Racing")
    stop()

def stop():
    print("stop")
    FRONT_LED.value(0)
    P1.off()
    P2.off()
    P3.off()
    P4.off()
    time.sleep(1)

def forward():
    print("forward....")
    P1.off()
    P2.on()
    P3.off()
    P4.on()
    
def backward():
    print("backward....")
    P1.on()
    P2.off()
    P3.on()
    P4.off()

def turn_left(t=0):
    print("trun left")
    P1.off()
    P2.on()
    P3.off()
    P4.off()
    time.sleep(t)

def turn_leftv2():
    print("turn left v2")
    P1.off()
    P2.on()
    P3.off()
    P4.off()
    while True:
        front_cm = FRONT.distance_cm()
        if front_cm > 20:
            stop()
            break
    
    time.sleep(1)

def turn_right(t=0):
    print("Turn right")
    P1.off()
    P2.off()
    P3.off()
    P4.on()
    time.sleep(1)

def turn_rightv2():
    print("Turn right")
    P1.off()
    P2.off()
    P3.off()
    P4.on()
    while True:
        front_cm = FRONT.distance_cm()
        if front_cm > 20:
            stop()
            break
    time.sleep(1)


def remote_control():
    print("remote")
    html = '''
    <!DOCTYPE html>
<html>
<head>
<title>TC Racing</title>
<style>
body {
  background-color: black;
  text-align: center;
  color: white;
  font-family: Arial, Helvetica, sans-serif;
}
.button{display: inline-block; background-color: #e7bd3b; border: none;
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
</style>
</head>
<body>

<h1>TC Racing</h1>

 <table border="1" width="100%">
    <tr>
        <td colspan="2">
        	<a  href="/?move=forward">
            	<button class="button">Forward</button>
            </a>
        </td>
    </tr>
    <tr>
        <td>
         <a  href="/?move=turn_left">
            	<button class="button">Left</button>
            </a>
        </td>
        <td>
         <a  href="/?move=turn_right">
            	<button class="button">Right</button>
            </a>
        </td>
    </tr>
     <tr>
        <td colspan="2">
        <a  href="/?move=backward">
            	<button class="button">Backward</button>
            </a>
        </td>
    </tr>
    <tr>
        <td colspan="2">
        <a  href="/?move=stop">
            	<button class="button">Stop</button>
            </a>
        </td>
    </tr>
  </table>
</body>
</html>
    '''
    return html 

def remote_car():
    print("start remote....")
    sock = socket.socket()
    sock.bind(SERVER) 
    sock.listen(1)
    while True:
        client, addr = sock.accept()
        clfile = client.makefile('rwb',0)
        while True:
            line = client.readline()
            if not line or line == b'\r\n':
                break 
            tmp = str(line)
            if "GET /?move=stop" in tmp:
                stop()
            elif "GET /?move=forward" in tmp:
                forward()
            elif "GET /?move=turn_left" in tmp:
                turn_left()
            elif "GET /?move=turn_right" in tmp:
                turn_right()
        
        remote = remote_control()
        client.send("HTTP/1.1 200 OK\n")
        client.send("Content-Type: text/html\n")
        client.send("Connection: close\n\n")
        client.sendall(remote)
        client.close()

def auto_car():
    while True:
 	front_cm = FRONT.distance_cm()
	print("Front=>", front_cm)
	if front_cm < 20:
	    stop()
            #think
            time.sleep(1)
            #check =>[left, right]
            #choose => left 
            turn_left(5)
            #turn_leftv2()
	else:
	    forward()
	time.sleep(0.5)

if __name__ == '__main__':

    __init__()
    #auto_car()
    remote_car()


