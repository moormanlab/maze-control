# Sensors control for maze
# Author: Ariel Burman

SENSORVERSION = 1.3

import time

import traceback
import logging
logger=logging.getLogger(__name__)

import gpiozero

#        /---------------\   /---------------\
#       /      UL(18)     \-/     UR(23)      \
#      /   /------------\     /------------\   \
#     |   /              \   /              \   |
#     |   |              |   |              |   |
#     | L |(17)          | C |(27)      (22)| R |
#     |   |              |   |              |   |
#     |   \              /   \              /   |
#      \   \------------/     \------------/   /
#       \       BL(4)     /-\     BR(24)      /
#        \---------------/   \---------------/


sensors = {'UL':18,
           'UR':23,
           'BL':4,
           'BR':24,
           'L':17,
           'C':27,
           'R':22
           }

import os

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
    logger.debug('Using handler {a}'.format(a=handler))

  def _sensorsHandler(self,sensorObj):
    try:
      logger.info(sensorObj.pin)
      sensorPin = int(str(sensorObj.pin)[4:])
      for key,value in sensors.items():
          if value == sensorPin:
              sensorName = key
      logger.debug('Sensor activated {a}'.format(a=sensorName))
      self.lastSensorActive = sensorName
      if self.handler is not None:
        self.handler(sensorName)
    except Exception as e:
      logger.error(traceback.format_exc())
      print('error handled module sensor')

  def isPressed(self,key):
    return self.sensor[key].isPressed()

  def getLastSensorActive(self):
    logger.debug('returning {a}'.format(a=self.lastSensorActive))
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
  lastactive = None

  class Test(object):
    def __init__(self):
      self.lastactive = None
      logger.debug('Tests id %s ',id(self))
      logger.debug('property id %s',id(self.lastactive))
      logger.info('Using handler {a}'.format(a=self.anotherHandler))
      logger.debug('procces id {}'.format(os.getpid()))
      self.sn = None
      logger.debug('MazeSensors id %s ',id(self.sn))


    def anotherHandler(self,sensor):
      print('last {a}'.format(a=self.lastactive))
      print('now {a}'.format(a=sensor))
      self.lastactive=sensor
      logger.debug('Tests id %s ',id(self))
      logger.debug('property id %s',id(self.lastactive))
      logger.debug('procces id {}'.format(os.getpid()))
      logger.info(sensor)

    def run(self):
      self.sn = MazeSensors(self.anotherHandler)
      while True:
        time.sleep(2)
        print(self.sn.getLastSensorActive())
        print(self.lastactive)
        print('procces id {}'.format(os.getpid()))


  test = Test()

#  while True:
#    time.sleep(2)
#    print(test.sn.getLastSensorActive())
#    print(test.lastactive)

  from multiprocessing import Process
  p = Process(target=test.run)
  p.start()

