from bkprecision.bkprecision import BKPrecisionMultimeter
import time
import serial
import logging

mult = BKPrecisionMultimeter(serial_port='/dev/ttyUSB0')
try:
    while True:
        print mult.measure()
except KeyboardInterrupt:
    mult.close_connection()
