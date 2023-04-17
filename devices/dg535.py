import sys
import serial
import time


class dg535:
    """DG 535 Pulse Gate"""

    TIMEOUT = 0.1  # Seconds to wait after sending command

    def __init__(self, devpath, address, DOUBLE_BITS=False):
        """
        devpath = USB com port. address = GPIB device number
        Set DOUBLE_BITS=True to solve DG535 bit-dropping issue (see README)
        """
        self.devpath = devpath
        self.port = serial.Serial(self.devpath, 9600, timeout=0.5)
        self.addr = str(address)
        self.doubleBits = DOUBLE_BITS

        self.qAddr()
        self.sendCmd("CL\r")

    def qAddr(self):
        """Query address from controller"""
        self.port.write(bytes("++addr " + self.addr + "\n", "utf-8"))

    def sendCmd(self, cmd):
        """Sends command to devices. cmd must be terminated with \\n"""
        if self.doubleBits:
            self.port.write(bytes(self.double(cmd), "utf-8"))
        else:
            self.port.write(bytes(cmd, "utf-8"))
        time.sleep(self.TIMEOUT)

    def double(self, s):
        """For instance, abc -> aabbcc"""
        return "".join([x * 2 for x in s])

    ### IMPORTANT ###
    ## Ports on the from panel correspond to the following numbers ##
    ## T0:1, A:2, B:3, AB/-AB:4, C:5, D:6, CD/-CD:7           ##

    def setPulse1(self, p1Time):
        """Set width of pulse 1 [sec]"""
        self.qAddr()
        self.sendCmd("DT 2,1,0\n")
        self.sendCmd("DT 3,2," + str(p1Time) + "\n")

    def setPulse2(self, precTime, p2Time):
        """Sets width of pulse 2, which starts some precTime after pulse 1"""
        self.qAddr()
        self.sendCmd("DT 5,3," + str(precTime) + "\n")
        self.sendCmd("DT 6,5," + str(p2Time) + "\n")

    def setAmp(self, output, amp):
        """Max step size +/- 4[V], minimum +/- 0.1[V]"""
        self.qAddr()
        self.sendCmd("OM " + str(output) + ",3\n")  # Voltage variable mode
        self.sendCmd("OA " + str(output) + "," + str(amp) + "\n")
        self.sendCmd("OO " + str(output) + ",0\n")  # Voltage offset

    def setTrg(self, trg, trgRt=10000, extTrg=1):
        """
        trg: 0 = Int, 1 = Ext, 2 = SingleShot, 3 = Burst
        trgRt only applies to Int and burst mode
        extTrg is the external trigger level in [volts]
        """
        self.qAddr()
        self.sendCmd("TM " + str(trg) + "\n")
        if trg == 0:  # set trigger rate for Int mode
            self.sendCmd("TR 0," + str(trgRt) + "\n")
        elif trg == 1:  # External trigger level in [volts]
            self.sendCmd("TL " + str(extTrg) + "\n")
        elif trg == 2:  # Immediately trigger for single shot mode
            self.sendCmd("SS\n")
        elif trg == 3:  # set trigger rate for burst mode
            self.sendCmd("TR 1," + str(trgRt) + "\n")
