# Hardaware abstraction layer for maze
# Author: Ariel Burman

MAZEHALVERSION = 1.3

import time
from multiprocessing import Process, Queue

import logging
logger=logging.getLogger(__name__)

from mazehal.valves import MazeValves
from mazehal.gates import MazeGates
from mazehal.buttons import MazeButtons
from mazehal.sensors import MazeSensors
from mazehal.sounds import MazeSounds


class MazeHal(object):
  def __init__(self,buttonHandler=None,sensorHandler=None):
    logger.debug('MazeHal id %s ',id(self))
    logger.info('MazeHal version {a}'.format(a=MAZEHALVERSION))
    self.valves = MazeValves()
    self.buttons = MazeButtons(buttonHandler)
    self.sensors = MazeSensors(sensorHandler)
    self.sounds = MazeSounds()
    self.gates = MazeGates()
    self.gatesP=Process(target=self.gates.run)

  def init(self):
    print('init mazehal')
    self.gatesP.start()
    #self.gatesP.join()
  def exit(self):
    self.gates.exit()
    self.gatesP.join()

  def __del__(self):
    print('exiting mazehal')
    #self.gates.exit()
    #self.gatesP.join()


#
#
#    def _run(self):
#      try:
#        self.
#        self.
#        while True:
#            #leer de la cola
#            if self.qC.empty() is False:
#                msg = self.qC.get()
#                logger.debug(msg)
#                if msg[0] == 'gate':
#                    if msg[1] == 'openAllNow':
#                        self.gates.openAllFast()
#                    elif msg[1] == 'openAll':
#                        self.gates.openAll()
#                    elif msg[1] == 'open':
#                        self.gates.openGate(msg[2])
#                    elif msg[1] == 'close':
#                        self.gates.closeGate(msg[2])
#                    elif msg[1] == 'openF':
#                        self.gates.openGateFast(msg[2])
#                    elif msg[1] == 'closeF':
#                        self.gates.closeGateFast(msg[2])
#                elif msg[0] == 'sensor':
#                    if msg[1] == 'last':
#                        resp = self.sensors.getLastSensorActive()
#                        self.qR.put(['sensor',resp])
#                    else:
#                        # TODO should check if it is a valid sensor
#                        resp = self.sensors.isPressed(msg[1])
#                        self.qR.put(['sensor',resp])
#                elif msg[0] == 'valve':
#                    if msg[1] == 'drop':
#                        self.valves.drop(msg[2])
#                    elif msg[1] == 'multidrop':
#                        self.valves.multiDrop(msg[2])
#                    elif msg[1]=='open':
#                        self.valves.open(msg[2])
#                    elif msg[1]=='close':
#                        self.valves.close(msg[2])
#                    elif msg[1]=='sdd':
#                        self.valves.setDropDelay(msg[2])
#                    elif msg[1]=='smd':
#                        self.valves.setMultidropsNum(msg[2])
#                    elif msg[1]=='smdd':
#                        self.valves.setMultidropsDelay(msg[2])
#                elif msg[0] == 'sound':
#                    if msg[1] == 'play':
#                        self.sounds.play(msg[2])
#                    elif msg[1]=='add':
#                        self.sounds.addTone(key=msg[2][0],duration=msg[2][1],freq=msg[2][2],volume=msg[2][3])
#                elif msg[0] == 'exit':
#                  self.                  break
#                else:
#                  raise NameError('Messege not defined')
#                  logger.error('Messegge {a} not defined'.format(a=msg[0]))
#            time.sleep(.01)
#      except Exception as e:
#        logger.debug('Exception ocurred in module mazehal')
#        logger.debug(e)
#      finally:
#          pass
#
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

  start()
  p = Process(target=hal._run)
  p.start()
  time.sleep(1)
  qC.put(['gate','openAll'])
  time.sleep(3)
  qC.put(['exit'])
  p.join()

