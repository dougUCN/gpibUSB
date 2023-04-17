import sys
import serial
import time


class bnc577:
    """BNC Pulse Generator"""

    TIMEOUT = 0.01  # Seconds to wait after sending command

    def __init__(self, devpath, address):
        """devpath = USB com port. address = GPIB device number"""
        self.devpath = devpath
        self.port = serial.Serial(self.devpath, 9600, timeout=0.5)
        self.addr = str(address)

        self.qAddr()
        self.setEOS()  # Set correct EOS mode
        self.sendCmd("++auto 0\n")  # Turn off auto read-after-write
        self.sendCmd("*RST\n")  # Reset to default

    def setEOS(self):
        """Specify correct gpib command end termination characters"""
        self.sendCmd("++eos 2\n")

    def sendCmd(self, cmd):
        """Sends command to device. cmd must be terminated with \\n"""
        self.port.write(bytes(cmd, "utf-8"))
        time.sleep(self.TIMEOUT)

    def qAddr(self):
        """Query address from controller"""
        self.sendCmd("++addr " + self.addr + "\n")

    def read(self):
        """Reads response from controller. Returns string"""
        self.sendCmd("++read\n")
        response = self.port.read(256)
        time.sleep(0.1)
        if len(response) > 0:
            return response.decode("utf-8")
        else:
            return "No response from bnc577"

    def burstMode(self, channel, numBursts):
        """Set burst mode for a channel [1 = A, 2 = B...]"""
        self.qAddr()
        self.setEOS()
        self.sendCmd(":PULSE" + str(int(channel)) + ":CMODE BURST\n")
        self.sendCmd(
            ":PULSE" + str(int(channel)) + ":BCOUNTER " + str(numBursts) + "\n"
        )

    def channelState(self, channel, state):
        """Enable/disable channel [1 = A, 2 = B...]"""
        self.qAddr()
        self.setEOS()
        if state:
            self.sendCmd(":PULSE" + str(int(channel)) + ":STATE ON\n")
        else:
            self.sendCmd(":PULSE" + str(int(channel)) + ":STATE OFF\n")
