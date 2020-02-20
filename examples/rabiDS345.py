#!/usr/bin/env python
#
# Generates one Pi pulse (Rabi) using two DS345 signal generators
# Does NOT scan across RF freq or pulse time
#
#
# DW 9/15/17

import os.path
import sys
import serial
import math
from .. import devices

COM_PORT = '/dev/ttyUSB0'
GPIB_ADDR_1 = 13    # DS345 giving the RF pulse
GPIB_ADDR_2 = 19    # DS345 acting as pulse generator
RF_GEN_AMP = 1	    # [Volts]
PULSE_GEN_AMP = 1   # [Volts]

def main():
    if len( sys.argv ) != 3:
        print ("Usage: ", os.path.basename( sys.argv[0] ), "<Pulse time> <RF_Freq>")
        sys.exit(1)
    pulseTime = float(sys.argv[1])
    pulseFreq = float(sys.argv[2])

    # Set dev 1 as RF pulse generator
    dev1 = devices.ds345(COM_PORT, GPIB_ADDR_1)
    dev1.setFreq(pulseFreq)
    dev1.setAmp(RF_GEN_AMP)
    dev1.burstMode(int(math.ceil(pulseTime*pulseFreq))) # Need burst count to last pulse time
    dev1.setTrg(2)			# 0 = single, 1 = Int, 2 = +Ext, 3 = -Ext, 4 = line

    # Set dev2 as pulse generator
    dev2 = devices.ds345(COM_PORT, GPIB_ADDR_2)
    dev2.squareWave()
    dev2.burstMode()               	# Burst count = 1
    dev2.setFreq( 1.0/2.0/pulseTime )   # 1/2 period = width of pulse
    dev2.setAmp(PULSE_GEN_AMP)
    dev2.setTrg(2)

if (__name__ == '__main__'):
    main()
