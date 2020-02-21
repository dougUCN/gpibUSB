#!/usr/bin/env python
#
# Generates up to two RF pulses with precession time in between
# Does NOT scan across RF freq or pulse time
#
#
# DW 9/15/17

import os.path
import sys
import serial
import math

sys.path.append("..")
import devices

COM_PORT = '/dev/ttyUSB0'
GPIB_ADDR_1 = 13    # DS345 giving the RF pulse
GPIB_ADDR_2 = 20    # DG535 acting as pulse generator

def main():
    if len( sys.argv ) != 8:
        print ("Usage:", os.path.basename(sys.argv[0]),
         "<Pulse 1 t> <Pulse 2 t> <prec t> <Pulse 1 amp> <Pulse 2 amp> <RF freq> <RF amp>")
        sys.exit(1)
    p1Time = float(sys.argv[1])
    p2Time = float(sys.argv[2])
    precTime = float(sys.argv[3])
    p1Amp = float(sys.argv[4])
    p2Amp = float(sys.argv[5])
    rfFreq = float(sys.argv[6])
    rfAmp = float(sys.argv[7])
    
    # Set dev 1 as RF pulse generator
    dev1 = devices.ds345(COM_PORT, GPIB_ADDR_1)
    dev1.setFreq(rfFreq)
    dev1.setAmp(rfAmp)
    # Burst count needs to last for duration of both pulses + precession
    dev1.burstMode( int(math.ceil( rfFreq* (p1Time + p2Time + precTime) )) )
    dev1.setTrg(2)	# External trigger

    # Set dev2 as gate pulse generator
    dev2 = devices.dg535(COM_PORT, GPIB_ADDR_2)
    dev2.setTrg(1)	# External trigger
    dev2.setPulse1(p1Time)
    dev2.setPulse2(precTime, p2Time)
    dev2.setAmp(4, p1Amp)
    dev2.setAmp(7, p2Amp)

if (__name__ == '__main__'):
    main()
