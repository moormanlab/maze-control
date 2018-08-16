# Valves control for maze
# Author: Ariel Burman

VALVEVERSION     = 1.0

import time

import logging
logger = logging.getLogger(__name__)

# Registers/etc:
ARDUINO_ADDRESS  = 0x60

#register
VALVE_OPEN                 = 0x04
VALVE_CLOSE                = 0x05
VALVE_DROP                 = 0x06
VALVE_MULTIDROP            = 0x07
VALVE_SET_MULTINUM         = 0x08
VALVE_SET_DELAYDROP        = 0x09
VALVE_SET_DELAYMULTIDROP   = 0x0a


valves = {'L':['Left',ord('L')],
          'R':['Right',ord('R')]
          }

class Valve():
  def __init__(self,name,data):
    self.name = name
    self.data = data

class MazeValves(object):
  def __init__(self, address=ARDUINO_ADDRESS, i2c=None, **kwargs):
    # Setup I2C interface for the device.
    if i2c is None:
      import Adafruit_GPIO.I2C as I2C
      i2c = I2C
    self._device = i2c.get_i2c_device(address, **kwargs)
    self.valve = {}
    for key in valves:
      self.valve[key] = Valve(valves[key][0],valves[key][1])
    self.multidrop=2
    self.dropdelay = 50
    self.multidropdelay = 2 # multiple of 500 ms (2 means 1 seconds)
    logger.debug('Valves initialized with id %s',id(self))
    logger.info('Valves version {a}'.format(a=VALVEVERSION))

  def open(self,key):
    self._device.write8(VALVE_OPEN,self.valve[key].data)

  def close(self,key):
    self._device.write8(VALVE_CLOSE,self.valve[key].data)

  def drop(self,key):
    self._device.write8(VALVE_DROP,self.valve[key].data)

  def setDropDelay(self,num):
    self.dropdelay = num
    self._device.write8(VALVE_SET_DELAYMULTIDROP,num)

  def setMultidropsNum(self,num):
    self.multidrop = num
    self._device.write8(VALVE_SET_MULTINUM,num)

  def setMultidropsDelay(self,num):
    self.multidropdelay = num
    self._device.write8(VALVE_SET_DELAYMULTIDROP,num)

  def getDropDelay(self):
    return self.dropdelay

  def getMultidropsNum(self):
    return self.multidrop

  def getMultidropsDelay(self):
    return self.multidropdelay

if __name__ == '__main__':
  import sys,os
  if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

  dateformat = '%Y/%m/%d %H:%M:%S'
  formatter_str = '%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s'
  logfile = 'logs/arduino.log'

  logging.basicConfig(filename=logfile,filemode='w+',level=logging.DEBUG,
          format=formatter_str, datefmt=dateformat)

  logger.info('Valve Test')

  valves=MazeValves()
  valves.open('L')
  time.sleep(1)
  valves.close('L')
  time.sleep(1)
  valves.open('R')
  time.sleep(1)
  valves.close('R')
