#!/usr/bin/env python
#
# Generates one Pi pulse (Rabi) using two DS345 signal generators
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
        description="Generates one Pi pulse (Rabi) using two DS345 signal generators",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-pt",
        "--pulseTime",
        required=True,
        type=float,
        help="Pi pulse time",
    )
    parser.add_argument(
        "-f",
        "--frequency",
        required=True,
        type=float,
        help="RF Frequency [Hz]",
    )
    parser.add_argument(
        "-rfa",
        "--rfAmplitude",
        type=float,
        default=1,
        help="RF Amplitude [V]",
    )
    parser.add_argument(
        "-pga",
        "--pulseGateAmplitude",
        type=float,
        default=1,
        help="Amplitude of pulse gate [V]",
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
        default=19,
        help="GPIB address of DS345 acting as the pulse gate",
    )
    args = parser.parse_args()

    # Set dev 1 as RF pulse generator
    dev1 = devices.ds345(args.serial, args.gpib1)
    dev1.setFreq(args.frequency)
    dev1.setAmp(args.rfAmplitude)
    dev1.burstMode(
        int(math.ceil(args.pulseTime * args.frequency))
    )  # Need burst count to last pulse time
    dev1.setTrg(2)  # 0 = single, 1 = Int, 2 = +Ext, 3 = -Ext, 4 = line

    # Set dev2 as pulse generator
    dev2 = devices.ds345(args.serial, args.gpib2)
    dev2.squareWave()
    dev2.burstMode()  # Burst count = 1
    dev2.setFreq(1.0 / 2.0 / args.pulseTime)  # 1/2 period = width of pulse
    dev2.setAmp(args.pulseGateAmplitude)
    dev2.setTrg(2)


if __name__ == "__main__":
    main()
