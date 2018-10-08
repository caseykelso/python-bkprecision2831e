from bkprecision.bkprecision import BKPrecisionMultimeter
import time

mult = BKPrecisionMultimeter(serial_port='/dev/ttyUSB0')

mult.configure_connection()

try:
    while True:
        print mult.measure()
        time.sleep(0.1)
except KeyboardInterrupt:
    mult.close_connection()
