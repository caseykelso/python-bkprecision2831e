import serial
import logging
import time


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
                                     timeout=1,
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
	time.sleep(0.5)

    def send_command(self,command):
	self.ser.write(command+"\n")
	time.sleep(0.1)
	out = self.ser.read(2000)
#        print 'out: %s' % out
        return out

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

        out = self.send_command("*IDN?")
        logging.info('BKPrecision 2831E: %s' % out)
        time.sleep(self.time_resolution)
#        out = self.send_command('*TRG')
#        logging.info('trigger measurement: %s' % out)
#        time.sleep(self.time_resolution)
        out = self.send_command(':FUNC?')
        logging.info('function: %s' % out)
        out = self.send_command(':DISPlay:ENABle?')
        logging.info('display: %s' % out)
        time.sleep(0.5)	
        out = self.send_command(':DISPlay:ENABle 1')
        logging.info('display: %s' % out)
        time.sleep(0.5)	
        out = self.send_command(':FUNCtion CURRent:DC')
	time.sleep(0.5)
	out = self.send_command(':FUNCtion?')
	time.sleep(0.5)
        out = self.send_command(':READ?')
        logging.info('read: %s' % out)
        time.sleep(0.5)	

        return True

    def measure(self):
        """
        Query a measure command to the multimeter.
        :return: a float value representing the response from the multimeter at a given time_resolution. None if
                 conversion could not been completed.
        """
#        logging.info('query multimeter.')
        out = self.send_command(":FETC?")
#	time.sleep(0.1)
	print out
        if out is not None and out != '':
            try:
                return float(out)
            except ValueError:
                return None

    def close_connection(self):
        self.ser.close()
