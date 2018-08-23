# Example protocol for maze training
# Author: Ariel Burman


from mazeprotocols import MazeProtocols
import time

import logging
logger=logging.getLogger(__name__)

PROTOCOL_NAME= 'BlockChoice'
PROTOCOL_VERSION = '1.0'

import numpy as np


class BlockChoice (MazeProtocols):
  def init(self):
    # initialization
    # put here the code you want to run only once, at first
    logger.info('Protocol: {a}, Version: {b}'.format(a=PROTOCOL_NAME,b=PROTOCOL_VERSION))
    self.blockSize = 30
    self.rewardWindow = 4.0
    logger.info('Block Size: {a}'.format(a=self.blockSize))
    self.state = 'start'
    self.openGate('IUL')
    self.openGate('IUR')
    self.openGate('OUL')
    self.openGate('OUR')
    self.openGate('OBL') # maybe closed
    self.openGate('OBR') # maybe closed
    self.closeGate('IBL')
    self.closeGate('IBR')
    self.rewardDone = False
    self.toneDone = False
    self.setMultiDrop(4)
    logger.info('set multidrop to 3')
    self.trialNum = 0
    self.rewardDone = False
    self.timeInitTraining = 0
    self.trialInit = 0
    self.trialCount = [0,0]
    self.trialCorrect = [0,0]
    self.addTone(1,duration=1.0,freq=1000,volume=1.0)
    self.addTone(2,duration=1.0,freq=8000,volume=1.0)
    logger.info('Tone 1 asociated with Left 1 kHz')
    logger.info('Tone 2 asociated with Right 8 kHz')
    time.sleep(1)
    pass # leave this line in case 'init' is empty

  def exit(self):
    # ending protocol. cleanup code. probably loggin stats.
    self.printStats()
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

  
  def chooseTone(self,trial):
    return int((trial-1)/self.blockSize) % 2 + 1

  def myFunction(self,param):
    logger.debug(param)

  def startTrial(self):
    self.trialNum +=1
    nextTone=self.chooseTone(self.trialNum)
    self.playSound(nextTone)
    logger.info('Played tone {a} trialNum {b}'.format(a=nextTone,b=self.trialNum))
    self.trialInit = time.time()
    self.trialCount[nextTone-1] +=1

  def printStats(self):
    tt = time.time() - self.timeInitTraining
    msg1 = 'Trial Num: {c} | Total time = {a} minutes {b} seconds'.format(a=int(tt/60),b=int(tt)%60,c = self.trialNum)
    msg2 = 'Total trial: {a}/{b} = {c}% | Left: {d}/{e} = {f}% | Right: {g}/{h} = {i}%'.format(
        a = sum(self.trialCorrect), b = sum(self.trialCount),c=round(100*sum(self.trialCorrect)/sum(self.trialCount)),
        d = self.trialCorrect[0] , e = self.trialCount[0] , f = round(100*self.trialCorrect[0]/(self.trialCount[0]+0.0001)),
        g = self.trialCorrect[1] , h = self.trialCount[1] , i = round(100*self.trialCorrect[1]/(self.trialCount[1]+0.0001)))
    print (msg1)
    print (msg2)
    logger.info(msg1)
    logger.info(msg2)

  def run(self):
    ''' 
    This is the main loop. It should have a 'while True:' statement
    also it is recomended to have a time.slep(.05) or bigger delay
    
    '''
    try:
      self.trialNum = 0
      # waiting to rat to pass the sensor
      while self.isSensorActive('C')==False:
          pass
      self.timeInitTraining = time.time()
      self.startTrial()
      while True:
        self.myFunction(self.state)
        if self.state == 'start':
          #if self.lastSensorActive()=='UL':
          self.rewardDone = False

          if self.isSensorActive('UL')==True:
            logger.info('Rat at {a}'.format(a='UL'))
            #the rat went left
            self.closeGate('IBL')
            self.closeGate('IBR')
            self.closeGate('IUR')
            self.openGate('OBL')
            self.state='going left'
            logger.info('reward on left')
          #elif self.lastSensorActive()=='UR':
          elif self.isSensorActive('UR')==True:
            logger.info('Rat at {a}'.format(a='UR'))
            #the rat went right
            self.closeGate('IBL')
            self.closeGate('IBR')
            self.closeGate('IUL')
            self.openGate('OBR')
            self.state='going right'
            # check for reward
            logger.info('reward on right')

        elif self.state == 'going left':
          #if self.lastSensorActive()=='L':
          if self.isSensorActive('L')==True:
            logger.info('Rat at {a}'.format(a='L'))
            self.closeGate('IUL')
            self.openGate('IBL')
            self.state = 'reward left'
            if self.rewardDone == False:
              self.rewardDone = True
              now = time.time()
              if now > (self.trialInit + self.rewardWindow):
                logger.info('Not Giving reward, exceeding window')
              elif self.chooseTone(self.trialNum)==2:
                logger.info('Not Giving reward, wrong side')
              else:
                logger.info('Giving reward')
                self.multiDrop('L')
                self.trialCorrect[self.chooseTone(self.trialNum)-1] += 1

        elif self.state == 'reward left':
          #if self.lastSensorActive()=='BL':
          if self.isSensorActive('BL')==True:
            logger.info('Rat at {a}'.format(a='BL'))
            self.openGate('IUL')
            self.openGate('IUR')
            self.closeGate('OUL')
            self.state = 'returning left'

          if self.isSensorActive('L')==True:
            logger.info('Rat at {a}'.format(a='L'))

        elif self.state == 'returning left':
          #if self.lastSensorActive()=='C':
          if self.isSensorActive('C')==True:
            logger.info('Rat at {a}'.format(a='C'))
            self.closeGate('OBL')
            self.openGate('OUL')
            self.openGate('OUR')
            self.state = 'start'
            self.printStats()
            self.startTrial()


        elif self.state == 'going right':
          #if self.lastSensorActive()=='R':
          if self.isSensorActive('R')==True:
            logger.info('Rat at {a}'.format(a='R'))
            self.closeGate('IUR')
            self.openGate('IBR')
            self.state = 'reward right'
            if self.rewardDone == False:
              now = time.time()
              self.rewardDone = True
              if now > (self.trialInit + self.rewardWindow):
                logger.info('NOT Giving reward, exceeding window')
              elif self.chooseTone(self.trialNum)==1:
                logger.info('Not Giving reward, wrong side')
              else:
                logger.info('Giving reward')
                self.multiDrop('R')
                self.trialCorrect[self.chooseTone(self.trialNum)-1] += 1

        elif self.state == 'reward right':
          #if self.lastSensorActive()=='BR':
          if self.isSensorActive('BR')==True:
            logger.info('Rat at {a}'.format(a='BR'))
            self.openGate('IUL')
            self.openGate('IUR')
            self.closeGate('OUR')

            self.state = 'returning right'

          if self.isSensorActive('R')==True:
            logger.info('Rat at {a}'.format(a='R'))
                
        elif self.state == 'returning right':
          #if self.lastSensorActive()=='C':
          if self.isSensorActive('C')==True:
            logger.info('Rat at {a}'.format(a='C'))
            self.closeGate('OBR')
            self.openGate('OUL')
            self.openGate('OUR')
            self.state = 'start'
            self.printStats()
            self.startTrial()

        time.sleep(.01)

    except Exception as e:
      logger.error(e)
      print(e)

