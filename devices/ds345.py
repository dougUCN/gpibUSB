import sys
import serial
import time

class ds345:    #SRS Signal generator

    def __init__(self, devpath, address):
        self.devpath = devpath
        self.port = serial.Serial(self.devpath, 9600, timeout=0.5)
        self.addr = str(address)

        self.qAddr()
        self.port.write(b'*RST\n')    # Reset to default
        self.port.write(b'FUNC 0\n')    # Sine wave

    def qAddr(self):        # Query address
        self.port.write( bytes('++addr ' + self.addr + '\n', 'utf-8' ))

    def burstMode(self, burstCount=1): # Burst count =1 by default
        self.qAddr()
        self.port.write(b'MENA 1; MTYP 5\n')    #Enable modululation, set to burst
        self.port.write( bytes('BCNT ' + str(burstCount) + '\n', 'utf-8' ))

    def squareWave(self):
        self.qAddr()
        self.port.write(b'FUNC 1\n')

    def setFreq(self, freq):    #[Hz]
        self.qAddr()
        self.port.write( bytes('FREQ ' + str(freq) + '\n' , 'utf-8' ))

    def setAmp(self, amp):    #[Volts]
        self.qAddr()
        self.port.write( bytes( 'AMPL ' + str(amp) + 'VP\n', 'utf-8' ))

    def setTrg(self, trg, trgRt=1000):    # 0 = single, 1 = internal, 2 = + Ext, 3 = -Ext, 4 = line
        self.qAddr()
        self.port.write( bytes( 'TSRC ' + str(trg) + '\n' , 'utf-8'))
        if trg == 0:
            self.port.write(b'*TRG\n')    # Trigger immediately  if set to single mode
        elif trg == 1:
            self.port.write( bytes('TRAT ' + str(trgRt) + '\n', 'utf-8'  )) # Set trigger rate to trgRt [Hz] if int

