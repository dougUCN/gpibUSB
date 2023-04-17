import sys
import serial
import time


class ds345:
    """SRS Signal generator"""

    TIMEOUT = 0.01  # Seconds to wait after sending command

    def __init__(self, devpath, address):
        """devpath = USB com port. address = GPIB device number"""
        self.devpath = devpath
        self.port = serial.Serial(self.devpath, 9600, timeout=0.5)
        self.addr = str(address)

        self.qAddr()
        self.sendCmd("*RST\n")  # Reset to default
        self.sendCmd("FUNC 0\n")  # Sine wave

    def sendCmd(self, cmd):
        """Sends command to device. cmd must be terminated with \\n"""
        self.port.write(bytes(cmd, "utf-8"))
        time.sleep(self.TIMEOUT)

    def qAddr(self):
        """Query address from controller"""
        self.sendCmd("++addr " + self.addr + "\n")

    def burstMode(self, burstCount=1):
        """Burst count =1 by default"""
        self.qAddr()
        self.sendCmd("MENA 1; MTYP 5\n")  # Enable modululation, set to burst
        self.sendCmd("BCNT " + str(burstCount) + "\n")

    def squareWave(self):
        self.qAddr()
        self.sendCmd("FUNC 1\n")

    def setFreq(self, freq):
        """[Hz]"""
        self.qAddr()
        self.sendCmd("FREQ " + str(freq) + "\n")

    def setAmp(self, amp):
        """[Volts]"""
        self.qAddr()
        self.sendCmd("AMPL " + str(amp) + "VP\n")

    def setTrg(self, trg, trgRt=1000):
        """0 = single, 1 = internal, 2 = + Ext, 3 = -Ext, 4 = line"""
        self.qAddr()
        self.sendCmd("TSRC " + str(trg) + "\n")
        if trg == 0:
            self.sendCmd("*TRG\n")  # Trigger immediately  if set to single mode
        elif trg == 1:
            self.sendCmd(
                "TRAT " + str(trgRt) + "\n"
            )  # Set trigger rate to trgRt [Hz] if int
