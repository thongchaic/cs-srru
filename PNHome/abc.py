import network
import machine 
import time
import gc 
import esp


class ABC(object):

    def __init__(self):
        gc.enable()
        self.N1 = machine.Pin(4,machine.Pin.OUT)
        self.N1.on()
        self.adc = machine.ADC(0)

    def infinity(self):
        
        while True:
            try:
                soil = self.adc.read()
                print(soil)
                if soil > 740:
                    self.N1.off()
                else:
                    self.N1.on()
                time.sleep(1)
            except:
                print("-.-")
                time.sleep(1)
                break

if __name__ == '__main__':

    while True:
        try:
            iot = ABC()
            iot.infinity()
        except:
            pass
            #machine.reset()

            
