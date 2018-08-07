# Author: Ariel Burman
#
import logging
import time

# Registers/etc:
ARDUINO_ADDRESS  = 0x60
#MODE1            = 0x00
#MODE2            = 0x01

#register
VALVE_OPEN                 = 0x04
VALVE_CLOSE                = 0x05
VALVE_DROP                 = 0x06
VALVE_MULTIDROP            = 0x07
VALVE_SET_MULTINUM         = 0x08
VALVE_SET_DELAYDROP        = 0x09
VALVE_SET_DELAYMULTIDROP   = 0x0a
#TEST1            = 0x5a  #90  // 0x5a 01011010
#TEST2            = 0xa5  #165 // 0xa5 10100101

# Bits:

logger = logging.getLogger(__name__)


class MazeValves(object):
  """PCA9685 PWM LED/servo controller."""
  def __init__(self, address=ARDUINO_ADDRESS, i2c=None, **kwargs):
    """Initialize the PCA9685."""
    # Setup I2C interface for the device.
    if i2c is None:
      import Adafruit_GPIO.I2C as I2C
      i2c = I2C
    self._device = i2c.get_i2c_device(address, **kwargs)
    self.valves = {}
    self.valves['L'] = MazeValves.Valve('Left',ord('L'))
    self.valves['R'] = MazeValves.Valve('Right',ord('R'))
    self.multidrop=2
    self.dropdelay = 50
    self.multidropdelay = 2 # multiple of 500 ms (2 means 1 seconds)
    logger.debug('Valves initialized')

  def open(self,key):
    self._device.write8(VALVE_OPEN,self.valves[key].data)

  def close(self,key):
    self._device.write8(VALVE_CLOSE,self.valves[key].data)

  def setDropDelay(self,num):
    self.dropdelay = num
    self._device.write8(VALVE_SET_DELAYMULTIDROP,num)

  def setMultidropsNum(self,num):
    self.multidrop = num
    self._device.write8(VALVE_SET_MULTINUM,num)

  def setMultidropsDelay(self,num):
    self._device.write8(VALVE_SET_DELAYMULTIDROP,num)

  class Valve():
    def __init__(self,name,data):
      self.name = name
      self.data = data

if __name__ == '__main__':
  import sys,os
  if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

  dateformat = '%Y/%m/%d %H:%M:%S'
  formatter_str = '%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s'
  logfile = 'logs/arduino.log'

  logging.basicConfig(filename=logfile,filemode='w+',level=logging.DEBUG,
          format=formatter_str, datefmt=dateformat)

  logger.info('Arduino Test')

  valves=MazeValves()
  valves.open('L')
  time.sleep(1)
  valves.close('L')
  time.sleep(1)
  valves.open('R')
  time.sleep(1)
  valves.close('R')
