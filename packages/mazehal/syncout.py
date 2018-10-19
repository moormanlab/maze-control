# Leds control for maze
# Author: Ariel Burman

SYNCVERSION     = 1.0

import time

import logging
logger = logging.getLogger(__name__)

# Registers/etc:
ARDUINO_ADDRESS  = 0x60

#register
TRIAL =        0x20


class MazeSyncOut(object):
  def __init__(self, address=ARDUINO_ADDRESS, i2c=None, **kwargs):
    # Setup I2C interface for the device.
    if i2c is None:
      import Adafruit_GPIO.I2C as I2C
      i2c = I2C
    self._device = i2c.get_i2c_device(address, **kwargs)
    logger.debug('Leds initialized with id %s',id(self))
    logger.info('Leds version {a}'.format(a=LEDSVERSION))

  def setTrial(self,trialType):
    logger.debug('Trial sync {a}'.format(a=trialType))
    self._device.write8(TRIAL,trialType)

if __name__ == '__main__':
  import sys,os
  if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

  dateformat = '%Y/%m/%d %H:%M:%S'
  formatter_str = '%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s'
  logfile = 'logs/syncout.log'

  logging.basicConfig(filename=logfile,filemode='w+',level=logging.DEBUG,
          format=formatter_str, datefmt=dateformat)

  logger.info('Sync out Test')

  sync=MazeSyncOut()
  sync.trial('L')
  time.sleep(1)
  sync.trial('R')
  time.sleep(1)
