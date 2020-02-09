#useful libraries
import time
import csv
import quick2wire.i2c as i2c
from quick2wire.i2c import I2CMaster, writing_bytes, reading
import math

#code template from: https://github.com/rsolomon/py-MS5607

#useful registers
#PLEASE CHECK
RESET = 0x1E
ADC_READ = 0x00
ADC_CONV = 0x40
ADC_D1 = 0x00
ADC_D2 = 0x10
ADC_256 = 0x00
ADC_512 = 0x02
ADC_1024 = 0x04
ADC_2048 = 0x06
ADC_4096 = 0x08
PROM_RD = 0xA0


def __read_adc(device_addr, cmd):
		with I2CMaster() as master:
			master.transaction(
				writing_bytes(device_addr, (DC_CONV | cmd)))  # Send conversion command

		# Map of times to delay for conversions
		delay_time = {}
		delay_time[_CMD_ADC_256] = 0.001
		delay_time[_CMD_ADC_512] = 0.003
		delay_time[_CMD_ADC_1024] = 0.004
		delay_time[_CMD_ADC_2048] = 0.006
		delay_time[_CMD_ADC_4096] = 0.01

		time.sleep(delay_time[cmd & 0x0f]) # Wait necessary conversion time

		with I2CMaster() as master:
			read_bytes = master.transaction(
				writing_bytes(device_addr, ADC_READ),
				reading(address, 3))

		tmp = 65536 * read_bytes[0][0] # Read MSB
		tmp = tmp + 256 * read_bytes[0][1] # Read byte
		tmp = tmp + read_bytes[0][2] # Read LSB
		return tmp


def get_pressure():
    pressure = self.__read_adc(_CMD_ADC_D1 | _CMD_ADC_4096)

#defining start time
t0 = time.time()

with  open('pres_Vals.csv', mode='w') as pres_data:
    pres_writer = csv.writer(pres_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    t0 = time.time()
    # keep reading data when elapse time is less than 2 hours
    while (t0 - time.time()) < 7200:
        #returns temperature in celsius
        pres = adt.temperature()
        pres_writer.writerow([temp, time.time())
        #delay to allow for data to be collected
        sleep(1)
