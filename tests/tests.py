from bkprecision.bkprecision import BKPrecisionMultimeter
import time
import serial
import logging

mult = BKPrecisionMultimeter(serial_port='/dev/ttyUSB0')
try:
    while True:
        mult.start()
except KeyboardInterrupt:
    mult.close_connection()
