gpibUSB
================
Minimal library for gpib communication using a PROLOGIX GPIB-USB connector through pyserial

The only setup required is to make sure your user is added to the dialout user group

Currently Supported Devices
----------------------------
DS345 Function Generator 
 
DG535 Pulse Gate Generator

BNC577 Pulse Gate Generator

Not all possible commands have been implemented. This library should
be easily expandable, though. 

Examples
----------------------
Each example script accepts command line arguments.  
When writing your own code, just put it in the same folder as /devices/ and import devices

### rabiDS345.py ###
Performs a single pi pulse using two DS345 signal generators

### ramseyCtrl.py ###
Uses a DS345 signal generator and a DG535 pulse gate for a ramsey pulse.  
(Obviously by tweaking input parameters you can use this for a rabi flip)

### test.py ###
Send a command to a device. To figure out which port your device is on,
`dmesg | grep tty` is a useful command


Available Commands
-----------------------
In the /gpibUSB directory, run
```
$pydoc devices/ds345.py
$pydoc devices/dg535.py
pydoc devices/bnc577.py
```

Or whatever your favorite docstring interpreter is
