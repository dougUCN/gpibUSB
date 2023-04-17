#!/usr/bin/env python
#
# Generates up to two RF pulses with precession time in between
# Does NOT scan across RF freq or pulse time
#
#
# DW 9/15/17

import sys
import argparse
import math

sys.path.append("..")
import devices


def main():
    parser = argparse.ArgumentParser(
        description="Generates up to two RF pulses with precession time in between. Uses a DS345 and DG535",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-rfFreq",
        "--rfFreq",
        required=True,
        type=float,
        help="Pi/2 pulse frequency [Hz]",
    )
    parser.add_argument(
        "-rfAmp",
        "--rfAmp",
        required=True,
        type=float,
        help="Pi/2 pulse amplitude [V]",
    )
    parser.add_argument(
        "-p1Time",
        "--p1Time",
        required=True,
        type=float,
        help="Pi/2 pulse 1 time [s]",
    )
    parser.add_argument(
        "-p2Time",
        "--p2Time",
        required=True,
        type=float,
        help="Pi/2 pulse 2 time [s]",
    )
    parser.add_argument(
        "-pg1Amp",
        "--pg1Amp",
        required=True,
        type=float,
        help="Pulse gate 1 amplitude [V]",
    )
    parser.add_argument(
        "-pg2Amp",
        "--pg2Amp",
        required=True,
        type=float,
        help="Pulse gate 2 amplitude [V]",
    )
    parser.add_argument(
        "-precTime",
        "--precTime",
        required=True,
        type=float,
        help="Free precession time [s]",
    )
    parser.add_argument(
        "-ser",
        "--serial",
        type=str,
        default="/dev/ttyUSB0",
        help="Serial communication port of Prologix controller",
    )
    parser.add_argument(
        "-gpib1",
        "--gpib1",
        type=int,
        default=13,
        help="GPIB address of DS345 giving the RF pulse",
    )
    parser.add_argument(
        "-gpib2",
        "--gpib2",
        type=int,
        default=20,
        help="GPIB address of DG6=535 Pulse generator",
    )
    args = parser.parse_args()

    # Set dev 1 as RF pulse generator
    dev1 = devices.ds345(args.serial, args.gpib1)
    dev1.setFreq(args.rfFreq)
    dev1.setAmp(args.rfAmp)
    # Burst count needs to last for duration of both pulses + precession
    dev1.burstMode(
        int(math.ceil(args.rfFreq * (args.p1Time + args.p2Time + args.precTime)))
    )
    dev1.setTrg(2)  # External trigger

    # Set dev2 as gate pulse generator
    dev2 = devices.dg535(args.serial, args.gpib2)
    dev2.setTrg(1)  # External trigger
    dev2.setPulse1(args.p1Time)
    dev2.setPulse2(args.precTime, args.p2Time)
    dev2.setAmp(4, args.pg1Amp)
    dev2.setAmp(7, args.pg2Amp)


if __name__ == "__main__":
    main()
