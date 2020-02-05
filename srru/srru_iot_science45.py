import time
import machine
import network
import ubinascii
import urequests
import dht

#https://surin.srru.ac.th/api/iot/data?token=431.2218518518519&device_id=9&dht_temperature=27
CFG_BSSID='SRRU-WiFi'
CFG_BSSID_PASS=''

DHT_SENSOR = dht.DHT22(machine.Pin(5))
