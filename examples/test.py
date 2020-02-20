#!/usr/bin/env python
#
# Simple test of a device interfacting via Prologix GPIB USB
# that is just plugged into the computer without any prior setup
#
# DW 9/12/17
#

def main():
    import os.path
    import serial
    import sys

    if len( sys.argv ) != 4:
        print "Usage: ", os.path.basename( sys.argv[0] ), "<COM port> <GPIB address> <Command>"
        sys.exit(1)

    comport = sys.argv[1];
    addr = sys.argv[2];
    customCmd = sys.argv[3]

    ser = serial.Serial()

    try:
        success = True

        # ser = serial.Serial( '\\\\.\\'+sys.argv[1], 9600, timeout=0.5 )

        ser = serial.Serial( sys.argv[1], 9600, timeout=0.5 )

        cmd = '++mode 1'        #Controller mode
        print 'Sending:', cmd
        ser.write(cmd + '\n')
        s = ser.read(256);
        if len(s) > 0:
            print s

        cmd = '++addr ' + addr  #Query address
        print 'Sending:', cmd
        ser.write(cmd + '\n')
        s = ser.read(256);
        if len(s) > 0:
            print s

        cmd = '++auto 1'        #Read after write
        print 'Sending:', cmd
        ser.write(cmd + '\n')
        s = ser.read(256);
        if len(s) > 0:
            print s

        cmd = customCmd
	print 'Sending:', cmd
        ser.write(cmd + '\n')
        s = ser.read(256);
        if len(s) > 0:
            print s
	
    except serial.SerialException, e:
        print e

    except KeyboardInterrupt, e:
        ser.close()


    return

if ( __name__ == '__main__' ):
    main()
