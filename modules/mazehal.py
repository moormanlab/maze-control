# Hardaware abstraction layer for maze
# Author: Ariel Burman

MAZEHALVERSION = 1.0

import time
from multiprocessing import Process, Queue

import logging
logger=logging.getLogger(__name__)

from modules.valves import MazeValves
from modules.gates import MazeGates
from modules.buttons import MazeButtons
from modules.sensors import MazeSensors
#from modules.sounds import MazeSounds

class MazeHal():

    def __init__(self,queueCommands,queueResponses):
        self.qC = queueCommands
        self.qR = queueResponses
#        self.p = []
#        self.valves = MazeValves()
        self.buttons = MazeButtons()
        self.sensors = MazeSensors()
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
                print (msg)
                if msg[0] == 'gate':
                    if msg[1] == 'openAllNow':
                        self.gates.openAllFast()
                    elif msg[1] == 'openAll':
                        self.gates.openAll()
                    elif msg[1] == 'open':
                        self.gates.openGate(msg[2])
                    
                if msg[0] == 'exit':
                  break
            else:
                print('cola vacia')
            time.sleep(1)

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
  hal.OpenValve()
  time.sleep(1)
  p.join()

