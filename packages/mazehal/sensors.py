# Sensors control for maze
# Author: Ariel Burman

SENSORVERSION = 1.2

import time

import logging
logger=logging.getLogger(__name__)

import gpiozero
#import modules.gpiozero as gpiozero


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

class Sensor(object):
  def __init__(self,gpioN=0):
    self.sensor=gpiozero.Button(gpioN)

  def setWhenPressed(self,handler):
    self.sensor.when_pressed = handler

  def isPressed(self):
    return self.sensor.is_pressed

class MazeSensors(object):
  def __init__(self,handler=None):
    self.sensor = {}
    self.handler = handler
    self.lastSensorActive = None
    for key in sensors:
      self.sensor[key] = Sensor(gpioN=sensors[key])

    for key in self.sensor:
      self.sensor[key].setWhenPressed(self._sensorsHandler)

    logger.debug('MazeSensors id %s ',id(self))
    logger.info('Sensors version {a}'.format(a=SENSORVERSION))

  def _sensorsHandler(self,sensorObj):
    try:
      logger.info(sensorObj.pin)
      sensorPin = int(str(sensorObj.pin)[4:])
      for key,value in sensors.items():
          if value == sensorPin:
              sensorName = key
      if self.handler is not None:
        self.handler(self,sensorName)
      else:
        logger.debug('Sensor activated {a}'.format(a=sensorName))
        self.lastSensorActive = sensorName
    except Exception as e:
      logger.error(e)
      print('error handled module sensor')

  def isPressed(self,key):
    return self.sensor[key].isPressed()

  def getLastSensorActive(self):
    return self.lastSensorActive

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

  def anotherHandler(obj):
    for key in obj.sensor:
      if obj.isPressed(key):
        print(key)
    logger.info(obj.sensor)

  logger.info(id(anotherHandler))
  sn = MazeSensors(anotherHandler)
  logger.info(id(sn))

  while True:
    time.sleep(2)
