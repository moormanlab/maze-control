#!/usr/bin/python3
import Adafruit_GPIO.I2C as I2C
import os
from time import sleep

device = I2C.get_i2c_device(0x60)

while True:
  data=chr(device.readU8(0x01))
  if (data == 'H'):
    device.writeRaw8(0x02)
    os.system('halt')
  sleep(5) #debug 20 seconds/ running 5 seconds
