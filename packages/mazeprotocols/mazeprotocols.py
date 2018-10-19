# Protocol base class for maze training
# Author: Ariel Burman

PROTOCOLSVERSION = 1.3

import time
import signal,sys
import logging
logger=logging.getLogger(__name__)
from mazehal import MazeHal

class MazeProtocols(object):
  def __init__(self):
    signal.signal(signal.SIGTERM, self.__exit_gracefully)  
    logger.info('Maze Protocols version {a}'.format(a=PROTOCOLSVERSION))
    #self.qC = queueCommands
    #self.qR = queueResponses

    if 'sensorHandler' in dir(self):
      sensorH = self.protocol.sensorHandler
    else:
      sensorH = None

    if 'buttonHandler' in dir(self):
      buttonH = self.protocol.buttonHandler
    else:
      buttonH = None
    self._mazehal = MazeHal(buttonHandler=buttonH,sensorHandler=sensorH)
    self._mazehal.init()
   
#  def __del__(self):
#    print('hhhhe')
#    logger.debug(dir(self))
#    logger.debug(id(self))
#    self.exit()

  def __exit_gracefully(self,a,b):
    print('exiting mazeprotocol')
    self.exit()
    self._mazehal.exit()
    #sys.exit()

  ## Buttons ##

  ## Sensors ##

  def getLastSensorActive(self):
    return self._mazehal.sensors.getLastSensorActive()
#    self.qC.put(['sensor','last'])
#    while self.qR.empty():
#      time.sleep(0.01)
#    a = self.qR.get()
#    if a[0]=='sensor':
#      return a[1]
#    else:
#      raise NameError('Unespected error')

  def isSensorActive(self,key):
    return self._mazehal.sensors.isPressed(key)
#    self.qC.put(['sensor',key])
#    while self.qR.empty():
#      time.sleep(.01)
#    a = self.qR.get()
#    if a[0]=='sensor':
#      return a[1]
#    else:
#      raise NameError('Unespected error')

  ## Valves ####

#                    if msg[1] == 'drop':
#                    elif msg[1] == 'multidrop':
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
  def drop(self,key):
    self._mazehal.valves.drop(key)

  def multiDrop(self,key):
    self._mazehal.valves.multiDrop(key)

  def setMultiDrop(self,num):
    self._mazehal.valves.setMultidropsNum(num)  

  ## Gates ##

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
  def openGate(self,key):
    self._mazehal.gates.openGate(key)

  def closeGate(self,key):
    self._mazehal.gates.closeGate(key)

  def openGateFast(self,key):
    self._mazehal.gates.openGateFast(key)

  def closeGateFast(self,key):
    self._mazehal.gates.closeGateFast(key)

  ## Sounds ##

  def playSound(self,key):
    self._mazehal.leds.irOn()
    self._mazehal.sounds.play(key)
    self._mazehal.leds.irOff()
    if key=='1':
        self._mazehal.sync.setTrial('L')
    else:
        self._mazehal.sync.setTrial('R')

  def addTone(self,key,duration=1.0, freq=1000.0, volume=1.0):
    self._mazehal.sounds.addTone(key=key,duration=duration,freq=freq,volume=volume)

