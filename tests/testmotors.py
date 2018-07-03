# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time

import logging
logger=logging.getLogger(__name__)
# Import the PCA9685 module.
import Adafruit_PCA9685

# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 200  # Min pulse length out of 4096 150
servo_max = 300  # Max pulse length out of 4096 640

# motor | open       | close       | position
# 0     | 220 -> 222 | 540 -> 534  | inner upper left
# 1     | 545 -> 535 | 195 -> 205  | inner lower left
# 2     | 210 -> 215 | 555 -> 545  | outter lower left
# 3     | 545 -> 535 | 200 -> 205  | outter upper left
# 4     | 220 -> 222 | 520 -> 510  | outter lower right
# 5     | 225 -> 230 | 550 -> 545  | outter upper right
# 6     | 195 -> 200 | 510 -> 505  | inner lower right
# 7     | 545 -> 540 | 200 -> 205  | inner upper right

print('1.4')

pwmV = [ [220, 222, 540, 534],
         [545, 535, 195, 205],
         [210, 215, 555, 542],
         [545, 535, 200, 210],
         [520, 510, 220, 222],
         [225, 230, 550, 545],
         [195, 200, 500, 492],
         [545, 540, 200, 205] ]


def openGate(gateN):
  pwm.set_pwm(gateN,0,pwmV[gateN][0])
  time.sleep(0.5)
  pwm.set_pwm(gateN,0,pwmV[gateN][1])

def closeGate(gateN):
  pwm.set_pwm(gateN,0,pwmV[gateN][2])
  time.sleep(0.5)
  pwm.set_pwm(gateN,0,pwmV[gateN][3])

def releasall():
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
pwm.set_pwm_freq(60)


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
