# Classe générique ELinstru #

import time, re, pyvisa

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

# Classe specifique NanoBLE #

class nanoBLE(Elinstrument):
    
    def __init__(self, address ='', timeout = 500, baudrate = 230400):
        Elinstrument.__init__(self, address, timeout, baudrate)

    def get_IDN(self):
        return self.query("*IDN?")
        
    def get_MEAS(self):
        datas = self.query("TH?")
        return re.findall(r'[-+]?([0-9]*\.[0-9]+|[0-9]+)', datas)

# AUTOTEST #

print("TEST COMMUNICATION NANOBLE")
device_port = Elinstrument().find_device('2021_ELINS_NanoBLE')
mydevice = nanoBLE(device_port, 200, 230400)
mydevice.open()
print("IDN ==> ",mydevice.get_IDN())
print("MEAS ==> ",mydevice.get_MEAS())
print("QUERY ==> ",mydevice.query("*IDN?"))
print("BAD RQS ==> ",mydevice.query("POUET?"))
mydevice.close()
print("FIN DU TEST NANOBLE")

"""
print("TEST COMMUNICATION BIAXIALE")
biaxiale = Elinstrument('TCPIP0::192.168.142.71::80::SOCKET', 2000)
biaxiale.open()
print("QUERY ==> ",biaxiale.query("*IDN?"))
print("BAD RQS ==> ",biaxiale.query("POUET?"))
biaxiale.close()
print("FIN DU TEST BIAXIALE")
"""