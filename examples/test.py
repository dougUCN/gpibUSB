#!/usr/bin/env python
#
# Simple test of a device interfacting via Prologix GPIB USB
# that is just plugged into the computer without any prior setup
#
# DW 9/12/17
#

import os.path
import serial
import sys
import time

def main():
    # baudRate = 9600
    baudRate = 115200

    if len( sys.argv ) != 4:
        print ("Usage: ", os.path.basename( sys.argv[0] ), "<COM port> <GPIB address> <Command>")
        sys.exit(1)

    comport = sys.argv[1];
    addr = sys.argv[2];

    ser = serial.Serial()

    try:
        ser = serial.Serial( sys.argv[1], baudRate, timeout=0.5 )

        sendCmd('++addr ' + addr, ser)  #Setting address

        sendCmd('++auto 1', ser)        #Read after write
        
        sendCmd(sys.argv[3], ser) 

    except serial.SerialException as e:
        print(e)

    except KeyboardInterrupt as e:
        ser.close()


    return

def sendCmd(cmd, ser):
    print('Sending:',cmd)
    ser.write( bytes( cmd + '\n', 'utf-8') )
    time.sleep(0.1)
    s = ser.read(256)
    if len(s) > 0:
        print(s)

if ( __name__ == '__main__' ):
    main()
