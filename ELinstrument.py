# Classe générique ELinstru #

import pyvisa

class Elinstrument:
    
    def __init__(self, address = '', timeout = 500, baudrate = 230400):
        self.address = address
        self.baudrate = baudrate
        self.timeout = timeout
        self.session = ''
    
    def open(self):
        self.session = pyvisa.ResourceManager().open_resource(self.address)
        self.session.timeout = self.timeout
        self.session.write_termination = '\n'
        self.session.read_termination = '\n'
    
    def write(self,string):
        self.session.write(string)

    def read(self):
        return self.session.read().strip()
    
    def query(self,string):
        return self.session.query(string).strip()
    
    def find(self,string):
        devices = pyvisa.ResourceManager().list_resources()
    
    def close(self):
        self.session.close()
        
    def clear(self):
        self.session.clear()
    
    def reverse(self, tuples):
        return tuples[::-1]

    def find_device(self, mystring):
        res = 'Not Found'
        devices = self.reverse(pyvisa.ResourceManager().list_resources())
        print('Devices list : ', devices)
        for device in devices :
            instr = pyvisa.ResourceManager().open_resource(device, open_timeout=500)
            instr.write_termination = '\n'
            instr.read_termination = '\n'
            idn = ''
            try :
                idn = (instr.query('*IDN?'))
            except :
                print('Error on ', device)
            finally :
                if idn.find(mystring) != -1:
                    res = device
                    print("Device '", mystring, "' found on", res)
                    break
                instr.close()
        return res

# EXEMPLES #

"""
nanoBLE = Elinstrument(Elinstrument().find_device('2021_ELINS_NanoBLE'), 200, 230400)
nanoBLE.open()
print('IDN ==> ',nanoBLE.query('*IDN?'))
print('STATUS ==> ',nanoBLE.query('TH?'))
nanoBLE.close()
"""

"""
biaxiale = Elinstrument('TCPIP0::192.168.142.71::80::SOCKET', 2000)
biaxiale.open()
print('IDN ==> ',biaxiale.query('*IDN?'))
print('STATUS ==> ',biaxiale.query('STATUS?'))
biaxiale.close()
"""