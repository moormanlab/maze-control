#!/usr/bin/python3
import Adafruit_GPIO.I2C as I2C
import os
from time import sleep

device = I2C.get_i2c_device(0x60)

while True:
  data=chr(device.readU8(0x01))
  if (data == 'H'):
    os.system('halt')
  sleep(10)

