# Hardaware abstraction layer for maze
# Author: Ariel Burman

MAZEHALVERSION = 1.4

import time
from multiprocessing import Process

import logging
logger=logging.getLogger(__name__)

from mazehal.valves import MazeValves
from mazehal.gates import MazeGates
from mazehal.buttons import MazeButtons
from mazehal.sensors import MazeSensors
from mazehal.sounds import MazeSounds
from mazehal.leds import MazeLeds
from mazehal.syncout import MazeSyncOut

class MazeHal(object):
  def __init__(self,buttonHandler=None,sensorHandler=None):
    logger.debug('MazeHal id %s ',id(self))
    logger.info('MazeHal version {a}'.format(a=MAZEHALVERSION))
    self.valves = MazeValves()
    self.buttons = MazeButtons(buttonHandler)
    self.sensors = MazeSensors(sensorHandler)
    self.sounds = MazeSounds()
    self.leds = MazeLeds()
    self.sync = MazeSyncOut()
    self.gates = MazeGates()
    self.gatesP=Process(target=self.gates.run)

  def init(self):
    self.gatesP.start()
    self.sync.setHigh([1,2,3,4,5,6,7,8])
    self.sync.setLow([1])
    self.sync.setLow([2])
    self.sync.setLow([3])
    self.sync.setLow([4])
    self.sync.setLow([5])
    self.sync.setLow([6])
    self.sync.setLow([7])
    self.sync.setLow([8])
    self.buttons.setLedOff('B')
    self.buttons.setLedOff('Y')
    self.buttons.setLedOff('W')
    self.buttons.setLedOff('G')

  def exit(self):
    self.sync.setHigh([1,2,3,4,5,6,7,8])
    self.sync.setLow([1])
    self.sync.setLow([2])
    self.sync.setLow([3])
    self.sync.setLow([4])
    self.sync.setLow([5])
    self.sync.setLow([6])
    self.sync.setLow([7])
    self.sync.setLow([8])
    self.gates.exit()

#  def __del__(self):
#    print('exiting mazehal')
#    print(dir(self))
#    #self.gates.exit()
#    #self.gatesP.join()

if __name__ == '__main__':
  import sys,os
  if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

  dateformat = '%Y/%m/%d %H:%M:%S'
  formatter_str = '%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s'
  logfile = 'logs/mazehal.log'

  logging.basicConfig(filename=logfile,filemode='w+',level=logging.DEBUG,
          format=formatter_str, datefmt=dateformat)

  logger.info('Hal test')
  hal = MazeHal()
  p = Process(target=hal._run)
  p.start()
  time.sleep(1)
  hal.exit()
  p.join()

