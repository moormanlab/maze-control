#!/usr/bin/python3
# Maze control
# Author: Ariel Burman

MAZEVERSION = 1.0

import logging
import time
import importlib
from importlib import util as imputil
from multiprocessing import Process, Queue

from modules.mazehal import MazeHal
from protocols.mazeprotocols import MazeProtocols

logger = logging.getLogger(__name__)

def check_module(module_name):
    """
    Checks if module can be imported without actually
    importing it
    """
    logger.debug(module_name)
    logger.debug(dir(importlib))
    module_spec = imputil.find_spec(module_name)
    if module_spec is None:
        logger.info('Module: {} not found'.format(module_name))
        return None
    else:
        logger.info('Module: {} can be imported!'.format(module_name))
        return module_spec


class Maze(object):

  def __init__(self,protocolFile=None,protocolClass=None):
    module_spec = check_module('protocols.'+protocolFile)
    if module_spec:
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
    else:
        raise NameError("Module doesn't exist")

    if protocolClass in dir(module):
        Protokol = getattr(module,protocolClass)
    else:
        raise NameError("Class doesn't exist")

    self.variable = 1
    self.qC = Queue()
    self.qR = Queue()

    self.protocol = Protokol(queueCommands=self.qC,queueResponses=self.qR)
    self.protocol.init()
    self.protocolP = Process(target=self.protocol.run)

    self.hal = MazeHal(queueCommands=self.qC,queueResponses=self.qR)
    self.halP = Process(target=self.hal._run)

    self.protocol.init()

  def start(self):
    if self.protocol == None:
      logger.debug('no protocol')
    else:
      self.halP.start()
      self.protocolP.start()

  def run(self):
    while True:
      logger.info('logged')
      time.sleep(2)
    self.protocolP.join()
    self.halP.join()

  def forceOpenAllGates(self):
    msg = ['gate','openAllNow']
    self.qC.put(msg)

  def forceDrop(self,key):
    pass

  def pause(self):
    logger.warning('exiting')

  def exit(self):
    logger.warning('exiting')
      
if __name__ == '__main__':
  import sys,os
  if not os.path.exists('./logs/'):
    os.makedirs('./logs/')
  dateformat = '%Y/%m/%d %H:%M:%S'
  formatter_str = '%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s'
  logfile = 'logs/mazer.log'

  logging.basicConfig(filename=logfile,filemode='w+',level=logging.DEBUG,
         format=formatter_str, datefmt=dateformat)

  logger.info('maze test')
  maze = Maze('skinner','Skinner')
  maze.start()
  try:
    while True:

        pass

  except Exception as inst:
    logger.warning(type(inst))
    logger.warning(inst.args)
    self.proccess.exit()
    sys.exit()
    maze.exit()

    


