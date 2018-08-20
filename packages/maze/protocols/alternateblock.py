# Example protocol for maze training
# Author: Ariel Burman


from mazeprotocols import MazeProtocols
import time

import logging
logger=logging.getLogger(__name__)

PROTOCOL_NAME= 'AlternateBlock'
PROTOCOL_VERSION = '1.0'

import numpy as np


class AlternateBlock (MazeProtocols):
  def init(self):
    # initialization
    # put here the code you want to run only once, at first
    logger.info('Protocol: {a}, Version: {b}'.format(a=PROTOCOL_NAME,b=PROTOCOL_VERSION))
    self.blockSize = 10
    logger.info('Block Size: {a}'.format(a=self.blockSize))
    self.time = 0
    self.state = 'start'
    self.openGate('IUL')
    self.openGate('IUR')
    self.openGate('OUL')
    self.openGate('OUR')
    self.openGate('OBL') # maybe closed
    self.openGate('OBR') # maybe closed
    self.closeGate('IBL')
    self.closeGate('IBR')
    self.multidone = False
    self.toneDone = False
    self.setMultiDrop(3)
    logger.info('set multidrop to 3')
    self.nextTone = 0
    self.trialType = None
    self.trialNum = 0
    self.addTone(2,duration=1.0,freq=1000,volume=1.0)
    self.addTone(1,duration=1.0,freq=8000,volume=1.0)
    logger.info('Tone 2 asociated with Left 1 kHz')
    logger.info('Tone 1 asociated with Right 8 kHz')
    time.sleep(1)
    pass # leave this line in case 'init' is empty

  def exit(self):
    # ending protocol. cleanup code. probably loggin stats.
    print('bye bye')
    pass # leave this line in case 'exit' is empty

#  def buttonHandler(obj,button):
#      ''' If you dont use a handler this function should be commented'''
#      pass
#
#  def sensorHandler(obj,sensor):
#      ''' If you dont use a handler this function should be commented'''
#      pass

  # Write your own methods

  
  def chooseNextTone(self,count):
    self.nextTone = int((count-1)/self.blockSize) % 2 + 1

  def myFunction(self,param):
    logger.debug(param)


  def run(self):
    ''' 
    This is the main loop. It should have a 'while True:' statement
    also it is recomended to have a time.slep(.05) or bigger delay
    
    '''
    try:
      self.trialNum = 0
      self.closeGate('IUR')
      while True:
        self.myFunction(self.state)
        if self.state == 'start':
          #if self.lastSensorActive()=='UL':
          self.multidone = False
          # only for the first trial, should re-think the scheme
          if self.isSensorActive('C')==True:
            logger.info('Rat at {a}'.format(a='C'))
            if self.toneDone == False:
              self.trialNum +=1
              self.chooseNextTone(self.trialNum)
              self.playSound(self.nextTone)
              logger.info('Played tone {a} trialNum {b}'.format(a=self.nextTone,b=self.trialNum))
              self.toneDone = True

          if self.isSensorActive('UL')==True:
            logger.info('Rat at {a}'.format(a='UL'))
            self.closeGate('IBL')
            self.closeGate('IBR')
            #self.closeGate('IUR')
            self.openGate('OBL')
            #the rat went left
            self.state='going left'
            # check for reward
            self.toneDone = False
            logger.info('reward on left')
          #elif self.lastSensorActive()=='UR':
          elif self.isSensorActive('UR')==True:
            logger.info('Rat at {a}'.format(a='UR'))
            #the rat went right
            self.closeGate('IBL')
            self.closeGate('IBR')
            #self.closeGate('IUL')
            self.openGate('OBR')
            self.state='going right'
            self.toneDone = False
            # check for reward
            logger.info('reward on right')

        elif self.state == 'going left':
          #if self.lastSensorActive()=='L':
          if self.isSensorActive('L')==True:
            logger.info('Rat at {a}'.format(a='L'))
            self.closeGate('IUL')
            self.openGate('IBL')
            self.state = 'reward left'
            if self.multidone == False:
              logger.info('Giving reward')
              self.multiDrop('L')
              self.multidone = True

        elif self.state == 'reward left':
          #if self.lastSensorActive()=='BL':
          if self.isSensorActive('BL')==True:
            logger.info('Rat at {a}'.format(a='BL'))
            self.closeGate('OUL')

            self.trialNum +=1
            self.chooseNextTone(self.trialNum)
            if self.nextTone == 1:
                self.openGate('IUL')
            else:
                self.openGate('IUR')
            self.state = 'returning left'

          if self.isSensorActive('L')==True:
            logger.info('Rat at {a}'.format(a='L'))

        elif self.state == 'returning left':
          #if self.lastSensorActive()=='C':
          if self.isSensorActive('C')==True:
            logger.info('Rat at {a}'.format(a='C'))
            self.closeGate('OBL')
            if self.nextTone == 1:
                self.openGate('OUL')
            else:
                self.openGate('OUR')
            self.state = 'start'
            self.playSound(self.nextTone)
            logger.info('Played tone {a} trialNum {b}'.format(a=self.nextTone,b=self.trialNum))
            self.toneDone = True


        elif self.state == 'going right':
          #if self.lastSensorActive()=='R':
          if self.isSensorActive('R')==True:
            logger.info('Rat at {a}'.format(a='R'))
            self.closeGate('IUR')
            self.openGate('IBR')
            self.state = 'reward right'
            if self.multidone == False:
              self.multiDrop('R')
              self.multidone = True

        elif self.state == 'reward right':
          #if self.lastSensorActive()=='BR':
          if self.isSensorActive('BR')==True:
            logger.info('Rat at {a}'.format(a='BR'))
            self.closeGate('OUR')

            self.trialNum +=1
            self.chooseNextTone(self.trialNum)
            if self.nextTone == 1:
                self.openGate('IUL')
            else:
                self.openGate('IUR')

            self.state = 'returning right'

          if self.isSensorActive('R')==True:
            logger.info('Rat at {a}'.format(a='R'))
                
        elif self.state == 'returning right':
          #if self.lastSensorActive()=='C':
          if self.isSensorActive('C')==True:
            logger.info('Rat at {a}'.format(a='C'))
            self.closeGate('OBR')
            if self.nextTone == 1:
                self.openGate('OUL')
            else:
                self.openGate('OUR')
            self.state = 'start'
            self.playSound(self.nextTone)
            logger.info('Played tone {a} trialNum {b}'.format(a=self.nextTone,b=self.trialNum))
            self.toneDone = True

        time.sleep(.025)

    except Exception as e:
      logger.error(e)
      print(e)

