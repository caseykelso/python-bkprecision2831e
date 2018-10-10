import serial
import logging
import time
import sys
import string
import re
import csv
import os
import signal
from threading import Thread



class BKPrecisionMultimeter:

    """
    This class provides basic functionality to operate with a BK Precision multimeter 2831E.
    """

    baud     = 38400
    ser      = None
    running  = True
    setup    = True


    def __init__(self, serial_port=None):
        """
        Initialize the serial port in which the multimeter is connected.
        :param serial_port: is the ID (Windows) or dev resource (Linux) which the multimeter is connected.
        :param time_resolution: is the time between measures.
        :param logging_file: optional, is the file which the log messages will be stored.
        """
        logging.info("***multimeter class");
        if serial_port is not None:
            self.ser = serial.Serial(port=serial_port,
                                     baudrate=self.baud,
                                     bytesize=serial.EIGHTBITS,
                                     timeout=0,
				     xonxoff=False,
				     rtscts=False,
                                     parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE)


	    self.ser.flush()
            self.tSerial  = None
            self.tMeasure = None
	    self.tTimeout = None



    def clear_buffer(self):
	self.ser.write("\n\n")
	self.ser.flush()
	time.sleep(0.2)

    def send_command(self,command):
	time.sleep(0.3)
	self.ser.write(command+"\n")

    def send_fetch(self,command):
	self.ser.write(command+"\n")


    def configure_connection(self):
        """
        Configure the connection.
        :return: True if connection and configuration is successful: otherwise, return False.
        """
        if self.ser.is_open:
            logging.info('The serial port %s is opened.' % (self.ser.port) )
        else:
            logging.error('The error could not been opened! Check serial port configuration.')
            return False

	self.clear_buffer()
#	self.send_command("*RST") # reset
#       time.sleep(10)
        logging.info('starting configuration of muiltimeter')
        self.send_command("*IDN?")
        self.send_command(':FUNC?')
        self.send_command(':DISPlay:ENABle?')
        self.send_command(':DISPlay:ENABle 1')
        self.send_command(':FUNCtion CURRent:DC')
	self.send_command(':FUNC?')
        self.send_command(':CURR:DC:NPLC 0.1')
        self.send_command(':CURR:DC:NPLC?')
        self.send_command(':CURR:DC:RANG:UPP 0.2') # set expected DC range of 0 to 0.2A (at 55V)
        self.send_command(':CURR:DC:RANG:UPP?')
#        self.send_command(':READ?')
        logging.info('completed configuration of muiltimeter')
        time.sleep(1)
	self.setup = False #setup complete
 

        return True

    def start(self):
        self.tSerial  = Thread(target=self.read_serial)
	self.tSerial.start()
        self.configure_connection()
        self.tMeasure = Thread(target=self.query_measurement)
	self.tMeasure.start()
        self.tTimeout = Thread(target=self.timeout_and_exit)
	self.tTimeout.start()
	return True

    def stop(self):
	logging.info("bkprecision.stop() called")
	self.running = False
	if (self.tSerial is not None):
		self.tSerial.join()
	
	if (self.tMeasure is not None):
		self.tMeasure.join()

	if (self.tTimeout is not None):
		self.tTimeout.join()

        self.ser.close()
	logging.info("bkprecision.stop() complete\n")



    def is_running(self):
	logging.info("is_running() called\n")
	return self.running

    def timeout_and_exit(self):
	logging.info("timeout_and_exit() thread started\n")
	cycle=0
	while(self.running and cycle < 300):
		time.sleep(1)
		cycle=cycle+1
	os.kill(os.getpid(), signal.SIGTERM)
	logging.info("timeout_and_exit() thread complete\n")

    def query_measurement(self):
	logging.info("query_measurement() thread started\n")
        while(self.running):
#        	logging.info('query multimeter.')
	        self.send_fetch(":FETC?")
		time.sleep(0.15) # sample near 10Hz, note that 38.4kbps cannot keep up at 10Hz and there is corruption
	logging.info("query_measurement() thread stopped\n")

    def read_serial(self):
	print("read_serial() thread started")
	with open('current.csv', mode='w') as current_file:
		current_writer = csv.writer(current_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		current_writer.writerow(['sample_index', 'current'])
		row_index = 0
		regex_measurement = re.compile(r'^\d+\.\d+e-\d+$')
		regex_command  = re.compile(r'^:')
#		misaligned_frame = ""

		while(self.running):
			out              = self.ser.read(1000)
#			last_linefeed    = out.rfind('\n')
#			if (out is not None and last_linefeed is not -1 and not self.setup and (len(out)) != last_linefeed+1):
#				print ("original out:"+  out +"," +str(len(out)))
#				print ("last linefeed position: %d" % last_linefeed)
#				misaligned_frame = out[last_linefeed:]
#				print ("misaligned_frame: %s" % misaligned_frame)
#				out              = out[:last_linefeed]
#				print ("new out: %s" % out) 

			for line in out.splitlines():
				if regex_measurement.match(line):
					print((line))
					current_writer.writerow([row_index, float(line)])
					if (0 == (row_index % 10)):
						current_file.flush()
					row_index=row_index+1
				elif ((regex_command.match(line)) and (":FETC" not in line) and not self.setup):
					logging.info('command: %s' % line)
				elif (":FETC" not in line and not self.setup):
					logging.info('malformed: %s' % line)
			time.sleep(0.1)
	print("read_serial() thread stopped");



