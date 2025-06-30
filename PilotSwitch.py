from ElInstrument import ElInstrument

class PilotSwitch(ElInstrument):
    def __init__(self, address = '', timeout = 500): ElInstrument.__init__(self, address, timeout)

    def getIDN(self):       return self.query("*IDN?")
    def getMAC(self):       return self.query("MAC?")
    def getCLIENT(self):    return self.query("CLIENT?")
    def getETH(self):       return self.query("ETH?")
    def getIP(self):        return self.query("IP?")
    def getIPALL(self):     return self.query("IP=ALL?")
    def getSWITCHS(self):   return self.query("SWITCHS?")

    def openSwitchs(self):  self.write('1O;2O')
    def closeSwitchs(self): self.write('1C;2C')
    def openSwitch1(self):  self.write('1O')
    def closeSwitch1(self): self.write('1C')
    def openSwitch2(self):  self.write('2O')
    def closeSwitch2(self): self.write('2C')

    def ethReboot(self):    self.write('ETH=REBOOT')
    def ethDhcp(self):      self.write('ETH=DHCP')
    def ethStatic(self, ip = '192.168.33.4', port = 80, mask = '255.255.255.0', gateway = '192.168.33.0'): self.write('ETH=IP '+ip+':'+str(port)+' '+mask+' '+gateway)
    

# EXEMPLE #


"""device_port = ElInstrument().find_device('2021_ELINS_NanoBLE')
mydevice = nanoBLE(device_port, 200, 230400)
mydevice.open()
print("IDN ==> ",mydevice.get_IDN())
print("MEAS ==> ",mydevice.get_MEAS())
print("QUERY ==> ",mydevice.query("*IDN?"))
print("BAD RQS ==> ",mydevice.query("POUET?"))
mydevice.close()"""
