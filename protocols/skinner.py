# Example protocol for maze training
# Author: Ariel Burman

from protocols.mazeprotocols import MazeProtocols
import time

import logging
logger=logging.getLogger(__name__)

class Skinner (MazeProtocols):
  def init(self):
    # initiazlization
    self.time = 0
    self.state = 'start'
    self.openGate('IUL')
    time.sleep(1)
    self.openGate('IUR')
    time.sleep(1)
    self.openGate('OUL')
    time.sleep(1)
    self.openGate('OUR')
    time.sleep(1)
    self.openGate('OBL') # maybe closed
    time.sleep(1)
    self.openGate('OBR') # maybe closed
    time.sleep(1)
    self.closeGate('IBL')
    time.sleep(1)
    self.closeGate('IBR')
    time.sleep(1)

  def myFunction(self,param):
    print(param)

#  def buttonHandler(obj):
#      print('if you dont use a handler this function should be commented')

#  def sensorHandler(obj):
#      print('if you dont use a handler this function should be commented')

  def run(self):
    try:
      while True:
        self.myFunction(self.state)
        if self.state == 'start':
          #if self.lastSensorActive()=='UL':
          if self.isSensorActive('UL')==True:
            self.closeGate('IBL')
            self.closeGate('IBR')
            self.closeGate('IUR')
            self.openGate('OBL')
            #the rat went left
            self.state='going left'
            # check for reward
            #self.drop('L')
          #elif self.lastSensorActive()=='UR':
          elif self.isSensorActive('UR')==True:
            #the rat went left
            self.closeGate('IBL')
            self.closeGate('IBR')
            self.closeGate('IUL')
            self.openGate('OBR')
            self.state='going right'
            # check for reward
            self.drop('L')
            # check for reward
            #self.drop('L')

        elif self.state == 'going left':
          #if self.lastSensorActive()=='L':
          if self.isSensorActive('L')==True:
            self.closeGate('IUL')
            self.openGate('IBL')
            self.state = 'reward left'

        elif self.state == 'reward left':
          #if self.lastSensorActive()=='BL':
          if self.isSensorActive('BL')==True:
            self.closeGate('OUL')
            self.openGate('IUL')
            self.openGate('IUR')
            self.state = 'returning left'

        elif self.state == 'returning left':
          #if self.lastSensorActive()=='C':
          if self.isSensorActive('C')==True:
            self.closeGate('OBL')
            self.openGate('OUL')
            self.openGate('OUR')
            self.state = 'start'


        elif self.state == 'going right':
          #if self.lastSensorActive()=='R':
          if self.isSensorActive('R')==True:
            self.closeGate('IUR')
            self.openGate('IBR')
            self.state = 'reward right'

        elif self.state == 'reward right':
          #if self.lastSensorActive()=='BR':
          if self.isSensorActive('BR')==True:
            self.closeGate('OUR')
            self.openGate('IUL')
            self.openGate('IUR')
            self.state = 'returning right'
                
        elif self.state == 'returning right':
          #if self.lastSensorActive()=='C':
          if self.isSensorActive('C')==True:
            self.closeGate('OBR')
            self.openGate('OUL')
            self.openGate('OUR')
            self.state = 'start'

        time.sleep(.2)

    except Exception as e:
      print(e)
    finally:
      print('bye')


