# Motor control for maze
# Author: Ariel Burman
#from __future__ import division
import time
import logging

logger=logging.getLogger(__name__)

# Import the PCA9685 module.
import Adafruit_PCA9685

# Uncomment to enable debug output.
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 200  # Min pulse length out of 4096 150
servo_max = 300  # Max pulse length out of 4096 640

# motor | open       | close       | key | position
# 0     | 220 -> 222 | 540 -> 534  | IUL | inner upper left 
# 1     | 545 -> 535 | 195 -> 205  | IBL | inner bottom left
# 2     | 210 -> 215 | 555 -> 545  | OBL | outter bottom left
# 3     | 545 -> 535 | 200 -> 205  | OUL | outter upper left
# 4     | 220 -> 222 | 520 -> 510  | OBR | outter bottom right
# 5     | 225 -> 230 | 550 -> 545  | OUR | outter upper right
# 6     | 195 -> 200 | 510 -> 505  | OBR | inner bottom right
# 7     | 545 -> 540 | 200 -> 205  | IUR | inner upper right

print('1.4')

#        /--------------\   /--------------\
#       /                \-/                \
#      /   /-----------\     /-----------\   \
#     |   / OUL     IUL \   / IUR     OUR \   |
#     |   |             |   |             |   |
#     |   |             |   |             |   |
#     |   \ OBL     IBL /   \ IBR     OBR /   |
#      \   \-----------/     \-----------/   /
#       \                /-\                 /
#        \--------------/   \---------------/




def openGate(gateN):
  pwm.set_pwm(gateN,0,pwmV[gateN][0])
  time.sleep(0.5)
  pwm.set_pwm(gateN,0,pwmV[gateN][1])

def closeGate(gateN):
  pwm.set_pwm(gateN,0,pwmV[gateN][2])
  time.sleep(0.5)
  pwm.set_pwm(gateN,0,pwmV[gateN][3])

def releaseall():
  for i in range(8):
    pwm.set_pwm(i,0,0)

def testGates():
  for i in range(8):
    openGate(i)
    time.sleep(2)
    closeGate(i)
    time.sleep(2)

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.


class MazerMotors(object):
  def __init__(self):
    self.pwm = Adafruit_PCA9685.PCA9685()
    self.pwm.set_pwm_freq(60)
    self.pwmV = {'IUL': (0,[220, 222, 540, 534]),
                 'IBL': (1,[545, 535, 195, 205]),
                 'OBL': (2,[210, 215, 555, 542]),
                 'OUL': (3,[545, 535, 200, 210]),
                 'OBR': (4,[520, 510, 220, 222]),
                 'OUR': (5,[225, 230, 550, 545]),
                 'OBR': (6,[195, 200, 500, 492]),
                 'IUR': (7,[545, 540, 200, 205]) }
    
  def open(self,key):
    gateN = self.pwmV[key][0]
    action = self.pwmV[key][1][0]
    hold = self.pwmV[key][1][1]
    self.pwm.set_pwm(gateN,0,action)
    self.time.sleep(0.5)
    self.pwm.set_pwm(gateN,0,hold)

  def close(self,key):
    gateN = self.pwmV[key][0]
    action = self.pwmV[key][1][2]
    hold = self.pwmV[key][1][3]
    self.pwm.set_pwm(gateN,0,action)
    time.sleep(0.5)
    self.pwm.set_pwm(gateN,0,hold)
  
  class _Motor(object):
    def __init__(self,key=None,index=None,openAction=0,openHold=0,closeAction=0,closeHold=0):
      self.key=key
      self.index=index
      self.closeAction=closeAction
      self.closeHold=closeHold
      self.openAction=openAction
      self.openHold=openHold
      self.position=0

    def open(self):
      actual = position
      end = self.openAction
      steps = 10
      diff = int((end - actual)/step)
      for i in range(9):
        

if __name__ == '__main__':
  import sys,os
  if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

  dateformat = '%Y/%m/%d %H:%M:%S'
  formatter_str = '%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s'
  logfile = 'logs/motors.log'

  logging.basicConfig(filename=logfile,filemode='w+',level=logging.DEBUG,
          format=formatter_str, datefmt=dateformat)

  logger.info('Motor test')
  testGates()
  releaseall()
