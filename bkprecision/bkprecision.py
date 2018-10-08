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
                                     timeout=0,
                                     parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE)
            logging.basicConfig(filename=logging_file, level=logging.DEBUG)
	    self.ser.flush()
            self.configure_connection()
            self.time_resolution = time_resolution

    def clear_buffer(self):
	self.ser.write("\r\r")
	self.ser.flush()
	time.sleep(0.5)

    def send_command(self,command):
	self.ser.write(command+"\r")
	time.sleep(0.1)
	return self.ser.read(2000)

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
        logging.info('BKPrecision 2831E: (%d) %s' % (len(out), out))

#        out = self.send_command(':FUNC?')
#        logging.info('function: %s' % out)

        return True

    def measure(self):
        """
        Query a measure command to the multimeter.
        :return: a float value representing the response from the multimeter at a given time_resolution. None if
                 conversion could not been completed.
        """
        #logging.info('query multimeter.')
#        self.ser.write(':FETCh?\r')
#        self.ser.flush()
#        time.sleep(self.time_resolution)
        out = self.ser.read(2000)
        if out is not None and out != '':
            try:
                return float(out)
            except ValueError:
                return None

    def close_connection(self):
        self.ser.close()
