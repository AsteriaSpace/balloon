import smbus
from time import sleep
import csv

# one byte = 8 bits
# asteriapi2 raspberry pi password

# id of the i2c bus
DEVICE_BUS = 1

# id of mpu sensor (found through i2cdetect command)
DEVICE_ADDR_1 = 0x69
# define useful registers
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x1B
PWR_MGMT_1 = 0X6B

addr_x_h = 0x3b
addr_x_l = 0x3c

addr_y_h = 0x3d
addr_y_l = 0x3e

addr_z_h = 0x3f
addr_z_l = 0x40

# set up bus
bus = smbus.SMBus(DEVICE_BUS)

# initialise the sensor
def MPU_Init(dev_addr):
    # write to sample rate register
    bus.write_byte_data(dev_addr, SMPLRT_DIV, 7)    #check number 7
    # write to power management register
    bus.write_byte_data(dev_addr, PWR_MGMT_1, 1)
    # write to config register
    bus.write_byte_data(dev_addr, CONFIG, 0)
    # write to configure gyro register
    bus.write_byte_data(dev_addr, GYRO_CONFIG, 24)
    # write to interrupt enable register
    bus.write_byte_data(dev_addr, INT_ENABLE, 1)

# function to read data from given register
def read_raw_acc_data(dev_addr, reg_addr):
    high = bus.read_byte_data(dev_addr, reg_addr)
    low = bus.read_byte_data(dev_addr, reg_addr+1)

    value = (high << 8) | low

    # get signed value
    if(value > 32768):
        value -= 65536
    return value



# test code
# init sensor
MPU_Init(DEVICE_ADDR_1)
# read data into file
#COMMENT - lists not used - remove
acc_x_vals = []
acc_y_vals = []
acc_z_vals = []

with open('acc_vals.csv', mode='w') as acc_data:
    acc_writer = csv.writer(acc_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for i in range(0,10):
        acc_x = 9.81 * read_raw_acc_data(DEVICE_ADDR_1, addr_x_h)/16384.0
        acc_y = 9.81 * read_raw_acc_data(DEVICE_ADDR_1, addr_y_h)/16384.0
        acc_z = 9.81 * read_raw_acc_data(DEVICE_ADDR_1, addr_z_h)/16384.0

        acc_writer.writerow([acc_x, acc_y, acc_z])
        sleep(1)
