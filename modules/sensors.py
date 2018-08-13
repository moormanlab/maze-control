# Sensors control for maze
# Author: Ariel Burman
import time
import logging

logger=logging.getLogger(__name__)

import gpiozero


#        /---------------\   /---------------\
#       /        UL       \-/       UR        \
#      /   /------------\     /------------\   \
#     |   /              \   /              \   |
#     |   |              |   |              |   |
#     | L |              | C |              | R |
#     |   |              |   |              |   |
#     |   \              /   \              /   |
#      \   \------------/     \------------/   /
#       \        BL       /-\       BR        /
#        \---------------/   \---------------/


sensors = {'UL':4,
           'UR':17,
           'BL':18,
           'BR':27,
           'L':22,
           'C':23,
           'R': 24
           }


import gpiozero

class Sensor(object):
  def __init__(self,gpioN=0, whenP = None):
    logger.info('Sensor connected to gpio %s with id %s',gpioN,id(self))
    self.sensor=gpiozero.Button(gpioN)
    self.sensor.when_pressed = whenP
    print('gpiozero button gpio {a} id {b} and handler id {c}'.format(a=gpioN,b=id(self.sensor),c=id(whenP)))

  def isPressed(self):
    return self.sensor.is_pressed

class MazeSensors(object):
  def __init__(self):
    # Initialise the PCA9685 using the default address (0x40).
    self.sensor = {}
    for key in sensors:
      self.sensor[key] = Sensor(gpioN=sensors[key] , whenP = self._sensorsHandler)
      print(' button {a} id {b}'.format(a=key, b=id(self.sensor[key])))
      
    logger.info('MazeSensors id %s ',id(self))

  def _sensorsHandler(self):
    print("going well")

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

  print(sn.sensor['C'].isPressed())
  gpiozero.Button.change(sn.sensor['C'].sensor)
  print(sn.sensor['C'].isPressed())
