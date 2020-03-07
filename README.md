gpibUSB
================
Minimal library for gpib communication using a PROLOGIX GPIB-USB connector through pyserial


Currently Supported Devices
----------------------------
DS345 Function Generator 
 
DG535 Pulse Gate Generator

BNC577 Pulse Gate Generator

Not all possible commands have been implemented. This library should
be easily expandable, though. 

Installation
-----------------------
1. Make sure your user is added to the dialout user group

2. Run this command in terminal: `git clone https://github.com/dougUCN/gpibUSB.git`

3. Use `dmesg | grep tty` to figure out which COM port your prologix controller is on,
and note what gpib address that your device is on

4. Send a command (such as `*IDN?`) using the test.py in the examples/ folder. This script is great for
troubleshooting as it will echo back your device response, and is not dependent on the devices module

5. When writing your own code, just put it in the same folder as gpibUSB/ and import devices


Examples
----------------------
Each example script accepts command line arguments.  

### rabiDS345.py ###
Performs a single pi pulse using two DS345 signal generators

### ramseyCtrl.py ###
Uses a DS345 signal generator and a DG535 pulse gate for a ramsey pulse.  
(Obviously by tweaking input parameters you can use this for a rabi flip)

### test.py ###
Send a command to a device


Available Commands
-----------------------
In the /gpibUSB directory, run
```
$pydoc devices/ds345.py
$pydoc devices/dg535.py
$pydoc devices/bnc577.py
```

Or whatever your favorite docstring interpreter is
