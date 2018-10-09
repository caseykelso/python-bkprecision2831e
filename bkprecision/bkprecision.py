import serial
import logging
import time
import sys
from threading import Thread


class BKPrecisionMultimeter:

    """
    This class provides basic functionality to operate with a BK Precision multimeter 2831E.
    """

    baud = 38400
    ser = None
    time_resolution = 0.008

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
            self.configure_connection()
            self.time_resolution = time_resolution

    def clear_buffer(self):
	self.ser.write("\n\n")
	self.ser.flush()
	time.sleep(0.2)

    def send_command(self,command):
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
        self.send_command(':READ?')

        return True

    def start(self):
	tMeasure = Thread(target=self.query_measurement)
	tMeasure.start()
        tSerial = Thread(target=self.read_serial)
	tSerial.start()
	while(True):
		time.sleep(1) # loop forever so that main doesn't exit and we can close the threads on ctrl-c
	return True

    def query_measurement(self):
        while(True):
        	logging.info('query multimeter.')
	        self.send_command(":FETC?")
		time.sleep(0.1)

    def read_serial(self):
	while(True):
		out = self.ser.read(1)
		sys.stdout.write(out)
#		sys.stdout.flush()
#        if out is not None and out != '':
#	        return out
#                return float(out)
#            except ValueError:
#                return None

    def close_connection(self):
        self.ser.close()
