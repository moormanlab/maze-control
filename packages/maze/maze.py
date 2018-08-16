#!/usr/bin/python3
# Maze control
# Author: Ariel Burman

MAZEVERSION = 1.0

import logging
import time
import importlib
from importlib import util as imputil
from multiprocessing import Process, Queue

from mazehal import MazeHal
from mazeprotocols import MazeProtocols

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

    logger.info('Initializing Maze')
    logger.debug('Maze id %s ',id(self))
    logger.info('Maze version {a}'.format(a=MAZEVERSION))
    self.qC = Queue()
    self.qR = Queue()

    self.protocol = Protokol(queueCommands=self.qC,queueResponses=self.qR)
    self.protocol.init()
    self.protocolP = Process(target=self.protocol.run)

    if 'sensorHandler' in dir(self.protocol):
      sensorHandler = self.protocol.sensorHandler
    else:
      sensorHandler = None

    if 'buttonHandler' in dir(self.protocol):
      buttonHandler = self.protocol.buttonHandler
    else:
      buttonHandler = None

    self.hal = MazeHal(queueCommands=self.qC,queueResponses=self.qR,
            sensorHandler=sensorHandler,buttonHandler=buttonHandler)
    self.halP = Process(target=self.hal._run)

  def start(self):
    if self.protocol == None:
      logger.debug('No protocol assigned')
    else:
      self.halP.start()
      self.protocolP.start()

  def run(self):
    while True:
      logger.info('Logged')
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
  subjectname = 'Reed' # 'Reed' 'Sue' 'Jhonny' 'Ben'
  import datetime
  today = datetime.date.today().strftime("%Y-%m-%d")
  Snum = 0
  while True:
    Snum += 1
    logfile = 'logs/' + subjectname + '-' + today + '-S' + format(Snum, '02d') + '.log'
    if os.path.isfile(logfile) == False:
        break
    if Snum == 99:
        raise NameError('Too many sessions in one day')

  logging.basicConfig(filename=logfile,filemode='w+',level=logging.DEBUG,
         format=formatter_str, datefmt=dateformat)

  logger.info('maze test')
  maze = Maze('skinner','Skinner')
  maze.start()
  try:
    while True:
        time.sleep(1)
        pass

  except Exception as inst:
    logger.warning(type(inst))
    logger.warning(inst.args)
    self.proccess.exit()
    sys.exit()
    maze.exit()
