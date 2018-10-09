from bkprecision.bkprecision import BKPrecisionMultimeter
import time
import serial
import logging
import signal
import sys

mult = None

def signal_handler(sig, frame):
	logging.info('CTRL-C pressed, exiting program.')
	app_running = False
	global mult
	mult.stop()
	sys.exit(0)

app_running = True
logging.basicConfig(filename="debug.log", level=logging.DEBUG)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
mult = BKPrecisionMultimeter(serial_port='/dev/ttyUSB0')
mult.start()

while app_running:
	try:
		time.sleep(0.01)
	except KeyboardInterrupt:
            logging.info('KI CTRL-C pressed, exiting program.')
	    app_running = False
	    mult.stop()
            sys.exit(0)



