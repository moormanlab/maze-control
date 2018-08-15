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
    self.openGate('IUR')
    self.openGate('OUL')
    self.openGate('OUR')
    self.openGate('OBL') # maybe closed
    self.openGate('OBR') # maybe closed
    self.closeGate('IBL')
    self.closeGate('IBR')

  def myFunction(self,param):
    print(param)

  def run(self):
    try:
      while True:
        self.myFunction(self.state)
        if self.state == 'start':
          if self.lastSensorActive()=='UL':
            self.closeGate('IBL')
            self.closeGate('IBR')
            self.closeGate('IUR')
            self.openGate('OBL')
            #the rat went left
            self.state='going left'
            # check for reward
            #self.drop('L')
          elif self.lastSensorActive()=='UR':
            #the rat went left
            self.closeGate('IBR')
            self.closeGate('IUL')
            self.openGate('OBR')
            self.state='going right'
            # check for reward
            self.drop('L')
            # check for reward
            #self.drop('L')

        elif self.state == 'going left':
          if self.lastSensorActive()=='L':
            self.closeGate('IUL')
            self.openGate('IBL')
            self.state = 'reward left'

        elif self.state == 'reward left':
          if self.lastSensorActive()=='BL':
            self.closeGate('OUL')
            self.openGate('IUL')
            self.openGate('IUR')
            self.state = 'returning left'

        elif self.state == 'returning left':
          if self.lastSensorActive()=='C':
            self.closeGate('OBL')
            self.openGate('OUL')
            self.openGate('OUR')
            self.state = 'start'


        elif self.state == 'going right':
          if self.lastSensorActive()=='R':
            self.closeGate('IUR')
            self.openGate('IBR')
            self.state = 'reward right'

        elif self.state == 'reward right':
          if self.lastSensorActive()=='BL':
            self.closeGate('OUR')
            self.openGate('IUL')
            self.openGate('IUR')
            self.state = 'returning right'
                
        elif self.state == 'returning right':
          if self.lastSensorActive()=='C':
            self.closeGate('OBL')
            self.openGate('OUL')
            self.openGate('OUR')
            self.state = 'start'

        time.sleep(.1)

    except Exception as e:
      print(e)
    finally:
      print('bye')


