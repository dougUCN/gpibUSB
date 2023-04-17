#!/usr/bin/env python
#
# Simple test of a device interfacting via Prologix GPIB USB
#
# DW 9/12/17
#

import os.path
import serial
import sys
import time
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Directly send command device connected via Prologix GPIB USB",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-gpib",
        "--gpib",
        type=int,
        required=True,
        help="Device GPIB address",
    )
    parser.add_argument(
        "-cmd",
        "--command",
        type=str,
        required=True,
        help="Command",
    )
    parser.add_argument(
        "-ser",
        "--serial",
        type=str,
        default="/dev/ttyUSB0",
        help="Serial communication port of Prologix controller",
    )
    parser.add_argument(
        "-br",
        "--baudRate",
        type=int,
        default=115200,
        help="baud rate",
    )
    args = parser.parse_args()

    ser = serial.Serial()

    try:
        ser = serial.Serial(args.serial, args.baudRate, timeout=0.5)
        sendCmd(f"++addr {args.gpib}", ser)  # Setting address
        sendCmd("++auto 1", ser)  # Read after write
        sendCmd(args.command, ser)

    except serial.SerialException as e:
        print(e)

    except KeyboardInterrupt as e:
        ser.close()

    return


def sendCmd(cmd, ser):
    print("Sending:", cmd)
    ser.write(bytes(cmd + "\n", "utf-8"))
    s = ser.read(256)
    time.sleep(0.1)
    if len(s) > 0:
        print(s)


if __name__ == "__main__":
    main()
