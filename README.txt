DW 9/17/17

Quick library for gpib communication using a PROLOGIX GPIB-USB connector

devices.py -- class file. Refer here for available daq commands. Should be easily expandable

rabiDS345.py -- performs a single pi pulse using two DS345 signal generators

ramseyCtrl.py -- Accepts command line arguments for integration with Qt gui. 
		Uses a DS345 signal generator and a DG535 pulse gate for a ramsey pulse. 
		(Obviously by tweaking input parameters you can use this for a rabi flip)

		NOTE: might require some minor alteration like additional commands 
		to get exactly what is required. Wish I had a chance to test it out.

test.py -- Send a command to a device
