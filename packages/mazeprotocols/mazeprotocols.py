# Protocol base class for maze training
# Author: Ariel Burman

PROTOCOLSVERSION = 1.5

import time
import signal,sys
import logging
logger=logging.getLogger(__name__)
from multiprocessing import Process
from mazehal import MazeValves, MazeGates, MazeButtons, MazeSensors, MazeSounds, MazeLeds, MazeSyncOut


class MazeProtocols(object):
  def __init__(self,options=None):
    signal.signal(signal.SIGTERM, self.__exit_gracefully)  
    logger.info('Maze Protocols version {a}'.format(a=PROTOCOLSVERSION))
    self._options = options

  def _run(self):
    try:
      if 'sensorHandler' in dir(self):
        sensorH = self.sensorHandler
      else:
        sensorH = None
     
      if 'buttonHandler' in dir(self):
        buttonH = self.buttonHandler
      else:
        buttonH = None
     
      self._valves = MazeValves()
      self._buttons = MazeButtons(buttonH)
      self._sensors = MazeSensors(sensorH)
      self._sounds = MazeSounds()
      self._leds = MazeLeds()
      self._sync = MazeSyncOut()
      self._gates = MazeGates()
      self._gatesP=Process(target=self._gates.run)
      self._gatesP.start()
      self._sync.setLow([1])
      self._sync.setLow([2])
      self._sync.setLow([3])
      self._sync.setLow([4])
      self._sync.setLow([5])
      self._sync.setLow([6])
      self._sync.setLow([7])
      self._sync.setLow([8])
      self._buttons.setLedOff('B')
      self._buttons.setLedOff('Y')
      self._buttons.setLedOff('W')
      self._buttons.setLedOff('G')
      self.init(self._options)
      self.run()
    except Exception as e:
      logger.error(e)
      print('error in mazeprotocol')
      print(e)
    
   
  def __exit_gracefully(self,a,b):
    print('Exiting MazeProtocol')
    self._sync.endTraining()
    self._gates.exit()
    self.exit()
    sys.exit()

  ## Buttons ##

  ## Sensors ##

  def getLastSensorActive(self):
    return self._sensors.getLastSensorActive()

  def isSensorActive(self,key):
    return self._sensors.isPressed(key)

  ## Valves ####

  def drop(self,key):
    self._valves.drop(key)

  def multiDrop(self,key):
    self._valves.multiDrop(key)

  def setMultiDrop(self,num):
    self._valves.setMultidropsNum(num)  

  ## Gates ##

  def openGate(self,key):
    self._gates.openGate(key)

  def closeGate(self,key):
    self._gates.closeGate(key)

  def openGateFast(self,key):
    self._gates.openGateFast(key)

  def closeGateFast(self,key):
    self._gates.closeGateFast(key)

  ## Sounds ##

  def playSound(self,key):
    self._sounds.play(key)

  def stopSound(self):
    self._sounds.stop()

  def addTone(self,key,duration=1.0, freq=1000.0, volume=1.0):
    self._sounds.addTone(key=key,duration=duration,freq=freq,volume=volume)

  def addWhiteNoise(self,key,duration=1.0, volume=1.0):
    self._sounds.addWhiteNoise(key=key,duration=duration,volume=volume)

  ## Sync ##

  def setSyncTrial(self,trial=None):
    if trial==None:
        trial='N'
    self._sync.startTrial(trial)

  def startTraining(self):
    self._sync.startTraining()

  def endTraining(self):
    self._sync.stopTraining()

  def setSyncH(self,data):
    if type(data) is int:
      if data >=0 and data<=8:
        self._sync.setHigh([data])
      else:
        raise ValueError('Bad sync output number')
    elif type(data) is str:
      if data=='tLed':
        self._leds.tLedOn()
      else:
        raise ValueError('Bad sync output number')
    elif type(data) is list:
      data2 = []
      for i in data:
        if type(i) is str:
          if i == 'tLed':
            self._leds.tLedOn()
          else:
            raise ValueError('Bad sync output number')
        else:
          if i >=0 and i <=8:
            data2.append(i)
          else:
            raise ValueError('Bad sync output number')
      self._sync.setHigh(data2)

  def setSyncL(self,data):
    if type(data) is int:
      if data >=0 and data<=8:
        self._sync.setLow([data])
      else:
        raise ValueError('Bad sync output number')
    elif type(data) is str:
      if data=='tLed':
        self._leds.tLedOff()
      else:
        raise ValueError('Bad sync output number')
    elif type(data) is list:
      data2 = []
      for i in data:
        if type(i) is str:
          if i == 'tLed':
            self._leds.tLedOff()
          else:
            raise ValueError('Bad sync output number')
        else:
          if i >=0 and i <=8:
            data2.append(i)
          else:
            raise ValueError('Bad sync output number')
      self._sync.setLow(data2)

