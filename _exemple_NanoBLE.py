from nanoBLE import nanoBLE
from time import sleep

device_port = 'ASRL10::INSTR'
#device_port = nanoBLE.find('2021_ELINS_NanoBLE', 230400)

mydevice = nanoBLE(device_port, 200, 230400)
print("IDN ==> ",mydevice.get_IDN())
print("MEAS ==> ",mydevice.get_MEAS())
print("QUERY ==> ",mydevice.query("*IDN?"))
print("BAD RQS ==> ",mydevice.query("POUET?"))

for i in range(10) :
    print('[',i,'] MEAS ==> ',mydevice.get_MEAS())
    sleep(0.100)
    
sleep(1)
mydevice.close()
