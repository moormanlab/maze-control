# Hardaware abstraction layer for maze
# Author: Ariel Burman

MAZEHALVERSION = 1.0

import time
from multiprocessing import Process, Queue

import logging
logger=logging.getLogger(__name__)

from .valves import MazeValves
from .gates import MazeGates
from .buttons import MazeButtons
from .sensors import MazeSensors
from .sounds import MazeSounds

class MazeHal():

    def __init__(self,queueCommands,queueResponses,sensorHandler=None,buttonHandler=None):
        self.qC = queueCommands
        self.qR = queueResponses
#        self.p = []
        self.valves = MazeValves()
        self.buttons = MazeButtons(buttonHandler)
        self.sensors = MazeSensors(sensorHandler)
        self.subject = None
        self.gates = MazeGates()
        self.gatesP=Process(target=self.gates.run)
        self.gatesP.start()
        logger.debug('MazeHal id %s ',id(self))
        logger.info('MazeHal version {a}'.format(a=MAZEHALVERSION))

    def _run(self):
      try:
        while True:
            #leer de la cola
            if self.qC.empty() is False:
                msg = self.qC.get()
                logger.debug(msg)
                if msg[0] == 'gate':
                    if msg[1] == 'openAllNow':
                        self.gates.openAllFast()
                    elif msg[1] == 'openAll':
                        self.gates.openAll()
                    elif msg[1] == 'open':
                        self.gates.openGate(msg[2])
                    elif msg[1] == 'close':
                        self.gates.closeGate(msg[2])
                    elif msg[1] == 'openF':
                        self.gates.openGate(msg[2])
                    elif msg[1] == 'closeF':
                        self.gates.closeGate(msg[2])
                elif msg[0] == 'sensor':
                    resp = self.sensors.isPressed(msg[1])
                    self.qR.put(['sensor',resp])
                elif msg[0] == 'valve':
                    if msg[1] == 'drop':
                        self.valves.drop(msg[2])
                    elif msg[1] == 'multidrop':
                        self.valves.multiDrop(msg[2])
                    elif msg[1]=='open':
                        self.valves.open(msg[2])
                    elif msg[1]=='close':
                        self.valves.close(msg[2])
                    elif msg[1]=='sdd':
                        self.valves.setDropDelay(msg[2])
                    elif msg[1]=='smd':
                        self.valves.setMultidropsNum(msg[2])
                    elif msg[1]=='smdd':
                        self.valves.setMultidropsDelay(msg[2])
                elif msg[0] == 'sound':
                    if msg[1] == 'play':
                        self.valves.drop(msg[2])
                    elif msg[1]=='set':
                        self.valves.open(msg[2])
                if msg[0] == 'exit':
                  break
            #else:
            #    print('cola vacia')
            time.sleep(.05)

            # si es una accion, enviar el comando a la clase correspondiente, que deberian ser procesos independientes
            # pero el sistema seguira funcionando

      finally:
          pass




if __name__ == '__main__':
  import sys,os
  if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

  dateformat = '%Y/%m/%d %H:%M:%S'
  formatter_str = '%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s'
  logfile = 'logs/motors.log'

  logging.basicConfig(filename=logfile,filemode='w+',level=logging.DEBUG,
          format=formatter_str, datefmt=dateformat)

  logger.info('Hal test')

  qC = Queue()
  qR = Queue()
  hal = MazeHal(qC,qR)
  p = Process(target=hal._run)
  p.start()
  time.sleep(1)
  qC.put(['gates','openall'])
  time.sleep(1)
  p.join()

