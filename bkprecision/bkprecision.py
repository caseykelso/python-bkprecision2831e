import serial
import logging
import time
import sys
import string
import re
import csv
from threading import Thread


class BKPrecisionMultimeter:

    """
    This class provides basic functionality to operate with a BK Precision multimeter 2831E.
    """

    baud = 38400
    ser = None

    def __init__(self, serial_port=None, time_resolution=0.008, logging_file='debug.log'):
        """
        Initialize the serial port in which the multimeter is connected.
        :param serial_port: is the ID (Windows) or dev resource (Linux) which the multimeter is connected.
        :param time_resolution: is the time between measures.
        :param logging_file: optional, is the file which the log messages will be stored.
        """
        if serial_port is not None:
            self.ser = serial.Serial(port=serial_port,
                                     baudrate=self.baud,
                                     bytesize=serial.EIGHTBITS,
                                     timeout=0,
				     xonxoff=False,
				     rtscts=False,
                                     parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE)

            logging.basicConfig(filename=logging_file, level=logging.DEBUG)

	    self.ser.flush()
#            self.configure_connection()
#            self.time_resolution = time_resolution

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
	self.send_command("*RST") # reset
        time.sleep(10)
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
 

        return True

    def start(self):
        tSerial = Thread(target=self.read_serial)
	tSerial.start()
        self.configure_connection()
	tMeasure = Thread(target=self.query_measurement)
	tMeasure.start()
        
	while(True):
		time.sleep(1000) # loop forever so that main doesn't exit and we can close the threads on ctrl-c
	return True

    def query_measurement(self):
        while(True):
#        	logging.info('query multimeter.')
	        self.send_fetch(":FETC?")
		time.sleep(0.11) # sample near 10Hz, note that 38.4kbps cannot keep up at 10Hz and there is corruption

    def read_serial(self):
	with open('current.csv', mode='w') as current_file:
		current_writer = csv.writer(current_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		current_writer.writerow(['sample_index', 'current'])
		row_index = 0
		regex_measurement = re.compile(r'^\d+\.\d+e-\d+$')
		regex_command  = re.compile(r'^:')

		while(True):
			out = self.ser.read(100)

			for line in out.splitlines():
				if regex_measurement.match(line):
#					print(float(line))
					current_writer.writerow([row_index, float(line)])
					if (0 == (row_index % 20)):
						current_file.flush()
					row_index=row_index+1
				elif ((regex_command.match(line)) and (":FETC" not in line)):
					logging.info('command: %s' % line)
			time.sleep(0.1)

    def close_connection(self):
        self.ser.close()
