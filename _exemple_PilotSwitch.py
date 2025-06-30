CLASS_PILOT_SWITCH = True

if CLASS_PILOT_SWITCH:
    from PilotSwitch    import PilotSwitch

    sw = PilotSwitch('TCPIP0::192.168.33.4::80::SOCKET')
    print(sw.getIDN())
    print(sw.getIPALL())
    sw.openSwitchs()
    print('OPEN\t1&2\t', sw.getSWITCHS())
    sw.closeSwitch1()
    print('CLOSE\t1\t', sw.getSWITCHS())
    sw.openSwitch1()
    print('OPEN\t1\t', sw.getSWITCHS())
    sw.closeSwitchs()
    print('CLOSE\t1&2\t', sw.getSWITCHS())
    del sw
else:
    from ElInstrument   import ElInstrument

    sw = ElInstrument('TCPIP0::192.168.33.4::80::SOCKET')
    print(sw.query('*IDN?'))
    print(sw.query('IP=ALL?'))
    sw.write('1O;2O')
    print('OPEN\t1&2\t', sw.query('SWITCHS?'))
    sw.write('2C')
    print('CLOSE\t2\t', sw.query('SWITCHS?'))
    sw.write('2O')
    print('OPEN\t2\t', sw.query('SWITCHS?'))
    sw.write('1C;2C')
    print('CLOSE\t1&2\t', sw.query('SWITCHS?'))
    del sw