gibUSB
================
Library for gpib communication using a PROLOGIX GPIB-USB connector through pyserial


Currently Supported Devices
----------------------------
DS345 Function Generator 

BNC577 Pulse Gate Generator

DG535 Pulse Gate Generator

Please note that some Prologix controllers may have issues communicating with the DG535, where every other message bit gets droppped. You can check what the DG535 is recieving by making it replay the last received message (refer to page 6 of the [manual](https://www.thinksrs.com/downloads/pdfs/manuals/DG535m.pdf)). If this is the case for your controller, set DOUBLE_BITS=True when initializing the dg535 device object

Not all possible commands have been implemented. This library should
be easily expandable, though. 

Gettings started
-----------------------
1. Make sure your user is added to the dialout user group (Linux) to allow pyserial to talk to the USB port

2. Run this command in terminal: `git clone https://github.com/dougUCN/gpibUSB.git`

3. Use `dmesg | grep tty` to figure out which COM port your prologix controller is on,
and note what gpib address that your device is on

4. Send a command (such as `*IDN?`) using the test.py in the examples/ folder. This script is great for
troubleshooting as it will echo back your device response, and is not dependent on the devices module

5. When writing your own code, just put it in the same folder as gpibUSB/ and import devices


Examples
----------------------

Communicating with your device should be as simple as

```
import devices
COM_PORT = '/dev/ttyUSB0'
GPIB_ADDR = 10 # Whatever number you set on your device
dev = devices.ds345(COM_PORT, GPIB_ADDR)
dev.setFreq(1000) # Or whatever command you want 
```

See the `examples/` folder for more

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
$pydoc3 devices/ds345.py
$pydoc3 devices/dg535.py
$pydoc3 devices/bnc577.py
```

Or whatever your favorite docstring interpreter is
