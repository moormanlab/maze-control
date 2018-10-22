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

  def _run(self):
    if 'sensorHandler' in dir(self):
      sensorH = self.sensorHandler
    else:
      sensorH = None

    if 'buttonHandler' in dir(self):
      buttonH = self.buttonHandler
    else:
      buttonH = None
    self._mazehal = MazeHal(buttonHandler=buttonH,sensorHandler=sensorH)
    self._mazehal.init()
    self._mazehal.sync.setLow([1,2,3,4,5,6,7,8])
    self.init()
    self.run()
   
  def __exit_gracefully(self,a,b):
    print('Exiting MazeProtocol')
    self.exit()
    self._mazehal.exit()
    sys.exit()

  ## Buttons ##

  ## Sensors ##

  def getLastSensorActive(self):
    return self._mazehal.sensors.getLastSensorActive()

  def isSensorActive(self,key):
    return self._mazehal.sensors.isPressed(key)

  ## Valves ####

  def drop(self,key):
    self._mazehal.valves.drop(key)

  def multiDrop(self,key):
    self._mazehal.valves.multiDrop(key)

  def setMultiDrop(self,num):
    self._mazehal.valves.setMultidropsNum(num)  

  ## Gates ##

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
        self._mazehal.sync.setHigh([1,5])
    else:
        self._mazehal.sync.setHigh([2,6])

  def addTone(self,key,duration=1.0, freq=1000.0, volume=1.0):
    self._mazehal.sounds.addTone(key=key,duration=duration,freq=freq,volume=volume)

