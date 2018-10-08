from bkprecision.bkprecision import BKPrecisionMultimeter
import time
import serial
import logging

mult = BKPrecisionMultimeter(serial_port='/dev/ttyUSB0')

mult.configure_connection()

try:
    while True:
        print mult.measure()
        time.sleep(1.0)
except KeyboardInterrupt:
    mult.close_connection()
