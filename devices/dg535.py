import sys
import serial
import time

class dg535:    #SRS pulse generator
    gpibControllerSux = False    #Some prologix controllers drop every other byte. See sendCmd()

    def __init__(self, devpath, address):
        self.devpath = devpath
        self.port = serial.Serial(self.devpath, 9600, timeout=0.5)
        self.addr = str(address)

        self.qAddr()
        self.sendCmd('CL\r')

    def qAddr(self):        # Query address
        self.port.write( bytes('++addr ' + self.addr + '\n', 'utf-8' ))

    def sendCmd(self, cmd): # Doubles every letter in cmd if Prologix gpib usb drops every other byte
        if self.gpibControllerSux:
            self.port.write( bytes(self.double(cmd), 'utf-8')) # Assumes cmd is a string that is null terminated
            time.sleep(0.1)
        else:
            self.port.write( bytes(cmd, 'utf-8') )
            time.sleep(0.1)

    def double(self, s):    #For instance, abc -> aabbcc
        return ''.join([x*2 for x in s])

    ### IMPORTANT ###
    ## Ports on the from panel correspond to the following numbers ##
    ## T0:1, A:2, B:3, AB/-AB:4, C:5, D:6, CD/-CD:7           ##

    def setPulse1(self, p1Time):
        self.qAddr()
        self.sendCmd('DT 2,1,0\n')
        self.sendCmd('DT 3,2,' + str(p1Time) + '\n')

    def setPulse2(self, precTime, p2Time):
        self.qAddr()
        self.sendCmd('DT 5,3,' + str(precTime) + '\n')
        self.sendCmd('DT 6,5,' + str(p2Time) + '\n')

    def setAmp(self, output, amp): #Max step size +/- 4[V], minimum +/- 0.1[V]
        self.qAddr()
        self.sendCmd('OM ' + str(output) + ',3\n')  #Voltage variable mode
        self.sendCmd('OA ' + str(output) + ',' + str(amp) + '\n')
        self.sendCmd('OO ' + str(output) + ',0\n')    #Voltage offset

    def setTrg(self, trg, trgRt=10000, extTrg =1): # 0 = Int, 1 = Ext, 2 = SS, 3 = Burst
        self.qAddr()
        self.sendCmd('TM ' + str(trg) +'\n')
        if trg == 0:        #set trigger rate for Int mode
            self.sendCmd('TR 0,' + str(trgRt) + '\n')
        elif trg == 1:        #External trigger level in [volts]
            self.sendCmd('TL ' + str(extTrg) + '\n')
        elif trg == 2:        #Immediately trigger for single shot mode
            self.sendCmd('SS\n')
        elif trg == 3:        #set trigger rate for burst mode
            self.sendCmd('TR 1,' + str(trgRt) + '\n')
