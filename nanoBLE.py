
# Classe specifique NanoBLE #

from ELinstrument import Elinstrument
import re

class nanoBLE(Elinstrument):
    
    def __init__(self, address ='', timeout = 500, baudrate = 230400):
        Elinstrument.__init__(self, address, timeout, baudrate)

    def get_IDN(self):
        return self.query("*IDN?")
        
    def get_MEAS(self):
        datas = self.query("TH?")
        return re.findall(r'[-+]?([0-9]*\.[0-9]+|[0-9]+)', datas)

# EXEMPLE #

"""
device_port = Elinstrument().find_device('2021_ELINS_NanoBLE')
mydevice = nanoBLE(device_port, 200, 230400)
mydevice.open()
print("IDN ==> ",mydevice.get_IDN())
print("MEAS ==> ",mydevice.get_MEAS())
print("QUERY ==> ",mydevice.query("*IDN?"))
print("BAD RQS ==> ",mydevice.query("POUET?"))
mydevice.close()
"""