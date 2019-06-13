# Leds control for maze
# Author: Ariel Burman

LEDSVERSION     = 1.1

import time

import logging
logger = logging.getLogger('MazeLeds')

# Registers/etc:
ARDUINO_ADDRESS  = 0x60

#register
TRIAL_LED =        0x12
TRIAL_LED_TOGGLE = 0x13

class MazeLeds(object):
  def __init__(self, address=ARDUINO_ADDRESS, i2c=None, **kwargs):
    # Setup I2C interface for the device.
    if i2c is None:
      import Adafruit_GPIO.I2C as I2C
      i2c = I2C
    self._device = i2c.get_i2c_device(address, **kwargs)
    self.leds = {}
    logger.debug('Leds initialized with id %s',id(self))
    logger.info('Leds version {a}'.format(a=LEDSVERSION))

  def tLedOn(self):
    logger.debug('Trial LED on')
    self._device.write8(TRIAL_LED,ord('H'))

  def tLedOff(self):
    logger.debug('Trial LED off')
    self._device.write8(TRIAL_LED,ord('L'))

  def tLedToggleN(self,N):
    logger.debug('Trial LED toggle {a} times'.format(a=N))
    self._device.write8(TRIAL_LED_TOGGLE,N)

if __name__ == '__main__':
  import sys,os
  if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

  dateformat = '%Y/%m/%d %H:%M:%S'
  formatter_str = '%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s'
  logfile = 'logs/arduino.log'

  logging.basicConfig(filename=logfile,filemode='w+',level=logging.DEBUG,
          format=formatter_str, datefmt=dateformat)

  logger.info('Leds Test')

  leds=MazeLeds()
  leds.tLedOn()
  time.sleep(1)
  leds.tLedOff()
  time.sleep(1)
  leds.tLedToggleN(5)
