# Example protocol for maze training
# Author: Ariel Burman

from mazeprotocols import MazeProtocols
import logging
logger=logging.getLogger(__name__)

# import any module you want to use
import time
import numpy as np

# Name your protocol FileName and version (One file can have multiple protocol variants, 

PROTOCOL_NAME= 'RandomChoice'
PROTOCOL_VERSION = '1.2'

class RandomChoice (MazeProtocols):
  def init(self,options):
    # initialization
    # put here the code you want to run only once, at first
    # 'options' is a dictionary with every option written in the configuration file wich can differ for every
    # subject
    logger.info('Protocol: {a}, Version: {b}'.format(a=PROTOCOL_NAME,b=PROTOCOL_VERSION))
    self.rewardWindow = options['rewardWindow']
    logger.info('Reward Window: {a}'.format(a=self.rewardWindow))
    self.multidropNum = options['multidropNum']
    logger.info('set multidrop to {a}'.format(a=self.multidropNum))
    self.setMultiDrop(self.multidropNum)
    self.state = 'start'
    pass # leave this line in case 'init' is empty

  def exit(self):
    # ending protocol. cleanup code. probably loggin stats.
    self.printStats()
    logger.info(self.trials)
    print('bye bye')
    pass # leave this line in case 'exit' is empty

#  def buttonHandler(obj,button):
#      ''' If you dont use a handler this function should be commented'''
#      pass
#

  def sensorHandler(self,sensor):
      ''' If you dont use a handler this function should be commented'''
      logger.info('sensor activated {a}'.format(a=sensor))
      self.myLastSensor = sensor
      pass

  # Write your own methods
  
  def chooseTone(self):
    return round(np.random.random()+1)

  def myFunction(self,param):
    logger.debug(param)

  def printStats(self):
    tt = time.time() - self.timeInitTraining
    msg1 = 'Trial Num: {c} | Total time = {a} minutes {b} seconds'.format(a=int(tt/60),b=int(tt)%60,c = self.trialNum)
    msg2 = 'Total trial: {a}/{b} = {c}% | Left: {d}/{e} = {f}% | Right: {g}/{h} = {i}%'.format(
        a = (self.trialsCorrect['L']+self.trialsCorrect['R']),
        b = (self.trialsCount['L']+self.trialsCount['R']),
        c = round(100*(self.trialsCorrect['L']+self.trialsCorrect['R'])/(self.trialsCount['L']+self.trialsCount['R']+0.0001)),
        d = self.trialsCorrect['L'] ,
        e = self.trialsCount['L'] ,
        f = round(100*self.trialsCorrect['L']/(self.trialsCount['L']+0.0001)),
        g = self.trialsCorrect['R'] ,
        h = self.trialsCount['R'] ,
        i = round(100*self.trialsCorrect['R']/(self.trialsCount['R']+0.0001)))
    print (msg1)
    print (msg2)
    logger.info(msg1)
    logger.info(msg2)

  # main loop

  def run(self):
    ''' 
    This is the main loop. It should have a 'while True:' statement
    also it is recomended to have a time.slep(.05) or bigger delay
    
    '''
    try:
      self.trialNum = 0
      # waiting to rat to pass the sensor
      #while self.getLastSensorActive()!='C':
      while self.myLastSensor is not 'C':
          time.sleep(.1)
          pass
      self.timeInitTraining = time.time()
      self.startTrial()
      while True:

        # write your main loop

        time.sleep(.01)

    except Exception as e:
      logger.error(e)
      print('Error in Protocol Program')
      print(e)


