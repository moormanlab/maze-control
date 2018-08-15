# Protocol base class for maze training
# Author: Ariel Burman

PROTOCOLSVERSION = 1.0

import time

import logging
logger=logging.getLogger(__name__)

class MazeProtocols(object):
  def __init__(self,queueCommands,queueResponses):
    logger.info('Maze Protocols version {a}'.format(a=PROTOCOLSVERSION))
    self.qC = queueCommands
    self.qR = queueResponses
   

  def lastSensorActive(self):
    self.qC.put(['sensors','last'])
    while self.qR.empty():
      time.sleep(1)
      print('bloqued')

    a = self.qR.get()
    return a


  def drop(self,key):
    msg = ['valve','drop',key]
    self.qC.put(msg)
    logger.debug(msg)

  def openGate(self,key):
    msg = ['gate','open',key]
    self.qC.put(msg)
    logger.debug(msg)

  def closeGate(self,key):
    msg = ['gate','close',key]
    self.qC.put(msg)
    logger.debug(msg)
