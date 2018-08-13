# Sensors control for maze
# Author: Ariel Burman
import time
import logging

logger=logging.getLogger(__name__)

import gpiozero


#        /---------------\   /---------------\
#       /        UL(18)   \-/       UR(23)    \
#      /   /------------\     /------------\   \
#     |   /              \   /              \   |
#     |   |              |   |              |   |
#     | L |(17)          | C |(27)      (22)| R |
#     |   |              |   |              |   |
#     |   \              /   \              /   |
#      \   \------------/     \------------/   /
#       \        BL(4)    /-\       BR(24)    /
#        \---------------/   \---------------/


sensors = {'UL':18,
           'UR':23,
           'BL':4,
           'BR':24,
           'L':17,
           'C':27,
           'R':22
           }


import gpiozero

class Sensor(object):
  def __init__(self,gpioN=0, whenP = None):
    logger.info('Sensor connected to gpio %s with id %s',gpioN,id(self))
    self.sensor=gpiozero.Button(gpioN)
    self.sensor.when_pressed = whenP
    logger.debug('gpiozero button gpio {a} id {b} and handler id {c}'.format(a=gpioN,b=id(self.sensor),c=id(whenP)))

  def isPressed(self):
    return self.sensor.is_pressed

class MazeSensors(object):
  def __init__(self):
    # Initialise the PCA9685 using the default address (0x40).
    self.sensor = {}
    for key in sensors:
      self.sensor[key] = Sensor(gpioN=sensors[key] , whenP = self._sensorsHandler)
      logger.debug(' button {a} id {b}'.format(a=key, b=id(self.sensor[key])))
      
    logger.info('MazeSensors id %s ',id(self))

  def _sensorsHandler(self):
    if self.isPressed('C'):
      logger.debug('H C')
    if self.isPressed('L'):
      logger.debug('H L')
    if self.isPressed('R'):
      logger.debug('H R')
    if self.isPressed('UL'):
      logger.debug('H UL')
    if self.isPressed('UR'):
      logger.debug('H UR')
    if self.isPressed('BL'):
      logger.debug('H BL')
    if self.isPressed('BR'):
      logger.debug('H BR')

  def isPressed(self,key):
    return self.sensor[key].isPressed()

if __name__ == '__main__':
  import sys,os
  if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

  dateformat = '%Y/%m/%d %H:%M:%S'
  formatter_str = '%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s'
  logfile = 'logs/sensors.log'

  logging.basicConfig(filename=logfile,filemode='w+',level=logging.DEBUG,
          format=formatter_str, datefmt=dateformat)

  logger.info('Sensors test')
  sn = MazeSensors()

  while True:
      if sn.isPressed('C'):
        print('C')
      if sn.isPressed('L'):
        print('L')
      if sn.isPressed('R'):
        print('R')
      if sn.isPressed('UL'):
        print('UL')
      if sn.isPressed('UR'):
        print('UR')
      if sn.isPressed('BL'):
        print('BL')
      if sn.isPressed('BR'):
        print('BR')
      time.sleep(0.1)
