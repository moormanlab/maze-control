# Signal to I/O sycronization between recording system, video camera, etc.
# Author: Ariel Burman

SYNCVERSION     = 1.2

import time
import gpiozero

import logging
logger = logging.getLogger(__name__)

# Registers/etc:
ARDUINO_ADDRESS  = 0x60

#register
TRAINSTART = 0x20
TRAINEND   = 0x21
TRIALSTART = 0x22
HDMI_ON    = 0x10
HDMI_OFF   = 0x11

syncouts = {1:['ARD',1],
            2:['ARD',2],
            3:['ARD',4],
            4:['ARD',8],
            5:['RPI',21],
            6:['RPI',20],
            7:['RPI',19],
            8:['RPI',16]
           }

class SyncOut(object):
    def setHigh(self):
        pass

    def setLow(self):
        pass

    def setToggle(self):
        pass

class SyncOutPi(SyncOut):
    def __init__(self, num):
      self._state = False  #False = Low  / True = high
      self._num = num
      self._device = gpiozero.DigitalOutputDevice(self._num)

    def setHigh(self):
      self._device.on()
      self._state = True

    def setLow(self):
      self._device.off()
      self._state = False

class SyncOutArd(SyncOut):
    def __init__(self, device, num):
      self._state = False  #False = Low  / True = high
      self._device = device
      self._num = num

    def setHigh(self):
      self._device.write8(HDMI_ON,self._num)
      self._state = True

    def setLow(self):
      self._device.write8(HDMI_OFF,self._num)
      self._state = False

class MazeSyncOut(object):
  def __init__(self, address=ARDUINO_ADDRESS, i2c=None, **kwargs):
    # Setup I2C interface for the device.
    self.syncOut = {}
    if i2c is None:
      import Adafruit_GPIO.I2C as I2C
      i2c = I2C
    self._device = i2c.get_i2c_device(address, **kwargs)
    for key in syncouts:
      if (syncouts[key][0] == 'ARD'):
        self.syncOut[key] = SyncOutArd(self._device,syncouts[key][1])
      elif (syncouts[key][0] == 'RPI'):
        self.syncOut[key] = SyncOutPi(syncouts[key][1])

    logger.debug('Sync output initialized with id %s',id(self))
    logger.info('Sync Output version {a}'.format(a=SYNCVERSION))

  def setHigh(self,outputs):
    if len(outputs)>0:
      for i in outputs:
        if i in self.syncOut:
          logger.debug('Syncout High {a}'.format(a=i))
          self.syncOut[i].setHigh()

  def setLow(self,outputs):
    if len(outputs)>0:
      for i in outputs:
        if i in self.syncOut:
          logger.debug('Syncout Low {a}'.format(a=i))
          self.syncOut[i].setLow()

  def startTraining(self):
    logger.debug('Sending Start Training')
    self._device.writeRaw8(TRAINSTART)

  def endTraining(self):
    logger.debug('Sending End Training')
    self._device.writeRaw8(TRAINEND)

  def startTrial(self,trial):
    logger.debug('Sending start Trial, trial type {a}'.format(a=trial))
    self._device.write8(TRIALSTART,ord(trial))

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
  sync.setHigh([1,3,5])
  time.sleep(1)
  sync.setLow([2,3,4])
  sync.setHigh([1,2,3,4,5,6,7,8])
  time.sleep(1)
  sync.setLow([1,2,3,4,5,6,7,8])
  time.sleep(1)
