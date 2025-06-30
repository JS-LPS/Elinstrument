# Classe générique ELinstru #

import pyvisa
import pyvisa.constants

class ElInstrument:
    
    def __init__(self, address = '', timeout = 500, baudrate = 230400):
        self.rm = pyvisa.ResourceManager()
        
        self.instr = self.rm.open_resource(address)
        self.session = self.instr.session
        self.rm.visalib.set_attribute(self.session,pyvisa.constants.ResourceAttribute.timeout_value,timeout)

        self.instr.write_termination = '\n'
        self.instr.read_termination = '\n'
        self.instr.send_end = True
        
        
        """
        if self.instr.resource_name.startswith('ASRL') :
            print('ASRL detected : setting up IO buffers')
            try :
                self.rm.visalib.set_attribute(self.session,pyvisa.constants.ResourceAttribute.asrl_baud_rate,baudrate)
                self.rm.visalib.set_buffer(self.session,pyvisa.constants.BufferType.io_in,4096)
                self.rm.visalib.set_buffer(self.session,pyvisa.constants.BufferType.io_out,4096)
                self.rm.visalib.flush(self.session,pyvisa.constants.BufferOperation.flush_transmit_buffer)
                self.rm.visalib.flush(self.session,pyvisa.constants.BufferOperation.flush_write_buffer)
            except :
                print('Error while buffers setup')
        """
    
    def __del__(self):
        try :
            self.instr.close()
            self.rm.close()
        except : print('Error On Destructor')

    def write(self,string):
        self.instr.write(string)

    def read(self):
        try : ack = self.instr.read().strip()
        except : ack = "Error On Read"
        finally : return ack
    
    def query(self,string):
            self.instr.write(string)
            try : ack = self.instr.read().strip()
            except : ack = "Error On Query : " + string
            finally : return ack

    def close(self):
        self.instr.close()
        self.rm.close()
        
    def clear(self):
        self.instr.clear()
    
    def find(string, baudrate):
        res = 'Not Found'
        rm = pyvisa.ResourceManager()
        devices = rm.list_resources()
        # print('Devices list : ', devices)
        for device in devices[::-1] : 
            try :
                instr = rm.open_resource(device,open_timeout=200)
                rm.visalib.set_attribute(instr.session,pyvisa.constants.ResourceAttribute.asrl_baud_rate,baudrate)
                rm.visalib.set_attribute(instr.session,pyvisa.constants.ResourceAttribute.timeout_value,200)
                rm.visalib.set_buffer(instr.session,pyvisa.constants.BufferType.io_in,4096)
                rm.visalib.set_buffer(instr.session,pyvisa.constants.BufferType.io_out,4096)
                rm.visalib.flush(instr.session,pyvisa.constants.BufferOperation.flush_transmit_buffer)
                rm.visalib.flush(instr.session,pyvisa.constants.BufferOperation.flush_write_buffer)

                instr.write_termination = '\n'
                instr.read_termination = '\n'
                instr.send_end = True
                idn = ''

                try :
                    idn = (instr.query('*IDN?'))
                    print('Successful query on',device,' ==> ',idn.strip())
                except :
                    print('Error on query',device,'...')
                finally :
                    if idn.find(string) != -1:
                        print("Device '",string, "' found on",device,'\n')
                        res = device
                        instr.close()
                        break
                    else :
                        print('\n')
            except :
                    print('Error on opening', device,'...')
        return res

# EXEMPLES #

DEVICE_ADDR = 'ASRL14::INSTR'

"""
print('\n--- TEST RAW ---\n')
rm = pyvisa.ResourceManager()
Pouet =  rm.open_resource(DEVICE_ADDR, baud_rate = 230400, timeout = 200)
#Pouet =  rm.open_resource('TCPIP0::192.168.142.74::80::SOCKET', timeout = 1000)
Pouet.write_termination = '\n'
Pouet.read_termination = '\n'
Pouet.send_end = True

if Pouet.resource_name.startswith('ASRL') :
            print('ASRL detected : setting up IO buffers')
            rm.visalib.set_buffer(Pouet.session,16,1024)
            rm.visalib.set_buffer(Pouet.session,32,1024)
            rm.visalib.flush(Pouet.session,32)
            rm.visalib.flush(Pouet.session,2)

print('IDN request ==> ',Pouet.query('*IDN?'))
Pouet.close()
rm.close()
print('\n--- FIN TEST Raw ---\n')
"""

#__________________________________________________________________________________


"""
print('\n--- TEST Wrapper ---\n')
Pouet = ElInstrument(DEVICE_ADDR, 200, 230400)
#Pouet = ElInstrument('TCPIP0::192.168.142.74::80::SOCKET', 2000)
print('IDN request ==> ',Pouet.query('*IDN?'))
del Pouet
print('\n--- FIN TEST Wrapper ---\n')
"""

#__________________________________________________________________________________

"""
print('\n--- TEST Find ---\n')
#ElInstrument.find('2021_ELINS_NanoBLE',230400)
#ElInstrument.find('NanoBLE',230400)
ElInstrument.find('Mbed',230400)
Pouet = ElInstrument(ElInstrument.find('Mbed',230400), 200, 230400)
print('IDN request ==> ',Pouet.query('*IDN?'))
del Pouet
print('\n--- FIN TEST Find ---\n')"""
