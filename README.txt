gpibUSB
-----------------------

Quick library for gpib communication using a PROLOGIX GPIB-USB connector
Currently supported devices: DS345 Function Generator, DG535 SRS Pulse Generator 

devices.py -- class file. Refer here for available devices and daq commands. Should be easily expandable

Examples
----------------------
When writing your own code, just put it in the same folder as /devices/ and import .devices

rabiDS345.py -- performs a single pi pulse using two DS345 signal generators

ramseyCtrl.py -- Accepts command line arguments for integration with Qt gui. 
		Uses a DS345 signal generator and a DG535 pulse gate for a ramsey pulse. 
		(Obviously by tweaking input parameters you can use this for a rabi flip)

		NOTE: might require some minor alteration like additional commands 
		to get exactly what is required. Wish I had a chance to test it out.

test.py -- Send a command to a device. To figure out which port your device is on,
	   'dmesg | grep tty' is a useful command
