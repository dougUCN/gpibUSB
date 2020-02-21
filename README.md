gpibUSB
================
Minimal library for gpib communication using a PROLOGIX GPIB-USB connector

Currently Supported Devices
----------------------------
DS345 Function Generator
DG535 Pulse Gate Generator

Not all possible commands have been implemented. This library should
be easily expandable, though. 

Examples
----------------------
Each example script accepts command line arguments
When writing your own code, just put it in the same folder as /devices/ and import devices

### rabiDS345.py ###
Performs a single pi pulse using two DS345 signal generators

### ramseyCtrl.py ###
Uses a DS345 signal generator and a DG535 pulse gate for a ramsey pulse. 
(Obviously by tweaking input parameters you can use this for a rabi flip)

### test.py ###
Send a command to a device. To figure out which port your device is on,
'dmesg | grep tty' is a useful command
