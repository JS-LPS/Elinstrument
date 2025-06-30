# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 14:24:29 2024

@author: frest
"""
"""
from USS_DBS import USS_DBS

USS_DBS.find('',9600)
"""

import pyvisa
import time

rm = pyvisa.ResourceManager()

"""
print('ressources list : ',rm.list_resources(),'\r\n')
print('opened ressources list : ',rm.list_opened_resources(),'\r\n')
print('ressource infos : ',rm.resource_info('ASRL5::INSTR'),'\r\n')
"""

device = rm.open_resource('ASRL5::INSTR')
device.baud_rate = 9600
for i in range(3):
    try :
        print(device.read())
    except :
        print('Error on read')
    finally : 
        time.sleep(0.2)
device.close()