# Motor control for maze
# Author: Ariel Burman

import time
import logging

logger=logging.getLogger(__name__)

import adai2c as pwm
# Uncomment to enable debug output.
#logging.basicConfig(level=logging.DEBUG)

from multiprocessing import Process, Queue, Lock

# motor | open       | close       | key | position
# 0     | 220 -> 222 | 540 -> 534  | IUL | inner upper left 
# 1     | 545 -> 535 | 195 -> 205  | IBL | inner bottom left
# 2     | 210 -> 215 | 555 -> 545  | OBL | outter bottom left
# 3     | 545 -> 535 | 200 -> 205  | OUL | outter upper left
# 4     | 220 -> 222 | 520 -> 510  | OBR | outter bottom right
# 5     | 225 -> 230 | 550 -> 545  | OUR | outter upper right
# 6     | 195 -> 200 | 510 -> 505  | OBR | inner bottom right
# 7     | 545 -> 540 | 200 -> 205  | IUR | inner upper right

#        /--------------\   /--------------\
#       /                \-/                \
#      /   /-----------\     /-----------\   \
#     |   / OUL     IUL \   / IUR     OUR \   |
#     |   |             |   |             |   |
#     |   |             |   |             |   |
#     |   \ OBL     IBL /   \ IBR     OBR /   |
#      \   \-----------/     \-----------/   /
#       \                /-\                /
#        \--------------/   \--------------/


#def openGate(gateN):
#  pwm.set_pwm(gateN,0,pwmV[gateN][0])
#  time.sleep(0.5)
#  pwm.set_pwm(gateN,0,pwmV[gateN][1])
#
#def closeGate(gateN):
#  pwm.set_pwm(gateN,0,pwmV[gateN][2])
#  time.sleep(0.5)
#  pwm.set_pwm(gateN,0,pwmV[gateN][3])
#
## Helper function to make setting a servo pulse width simpler.
#def set_servo_pulse(channel, pulse):
#    pulse_length = 1000000    # 1,000,000 us per second
#    pulse_length //= 60       # 60 Hz
#    print('{0}us per period'.format(pulse_length))
#    pulse_length //= 4096     # 12 bits of resolution
#    print('{0}us per bit'.format(pulse_length))
#    pulse *= 1000
#    pulse //= pulse_length
#    pwm.set_pwm(channel, 0, pulse)

class MazerMotors(object):
  def __init__(self):
    # Initialise the PCA9685 using the default address (0x40).
    self.pwm = pwm.AdaI2C()
    # Set frequency to 60hz, good for servos.
    self.pwmV = {'IUL': (0,[220, 222, 540, 534]),
                 'IBL': (1,[545, 535, 195, 205]),
                 'OBL': (2,[210, 215, 555, 542]),
                 'OUL': (3,[545, 535, 200, 210]),
                 'OBR': (4,[520, 510, 220, 222]),
                 'OUR': (5,[225, 230, 550, 545]),
                 'OBR': (6,[195, 200, 500, 492]),
                 'IUR': (7,[545, 540, 200, 205]) }
    self.motors = {}
    self.queue = Queue()
    for key in self.pwmV:
        self.motors[key]=MazerMotors._Motor(key=key,index=self.pwmV[key][0],
                openGoal=self.pwmV[key][1][0],openAfter=self.pwmV[key][1][1],
                closeGoal=self.pwmV[key][1][2],closeAfter=self.pwmV[key][1][3])

  def _moveSlow(self,key,goal,after):
    gate = self.motors[key].index
    now = self.motors[key].position
    self.motors[key].lock.acquire()
    self.motors[key].moving = True
    try:
      if goal > now:
          diff = 1
      else:
          diff = -1
      #steps = 50
      #diff = int((goal-now)/steps)
      logger.info('gate %s | now %s | goal %s | after %s | diff %s',gate,now,goal,after,diff)
      while (goal != now):
        now += diff
        logger.info('gate now %s',now)
        self.pwm.set(gate,now)
        time.sleep(0.002)
        self.motors[key].position = now
      self.pwm.set(gate,goal)
      self.motors[key].position = goal
      time.sleep(0.1)
      self.pwm.set(gate,after)
      self.motors[key].position = after
    finally:
      self.motors[key].lock.release()
      self.motors[key].moving = False

  def _moveFast(self,key,goal,after):
    gate = self.motors[key].index
    self.motors[key].lock.acquire()
    self.motors[key].moving = True
    try:
      self.pwm.set(gate,goal)
      self.motors[key].position = goal
      time.sleep(0.5)
      self.pwm.set(gate,after)
      self.motors[key].position = after
    finally:
      self.motors[key].lock.release()
      self.motors[key].moving = False

  def openGateFast(self,key):
    logger.debug('openF %s',self.motors[key].index)
    goal = self.motors[key].openGoal
    after = self.motors[key].openAfter
    self.queue.put(['fast',[key,goal,after]])

  def closeGateFast(self,key):
    logger.debug('closeF %s',self.motors[key].index)
    goal = self.motors[key].closeGoal
    after = self.motors[key].closeAfter
    self.queue.put(['fast',[key,goal,after]])

  def openGate(self,key):
    logger.debug('openS %s',self.motors[key].index)
    goal = self.motors[key].openGoal
    after = self.motors[key].openAfter
    self.queue.put(['slow',[key,goal,after]])

  def closeGate(self,key):
    logger.debug('closeS %s',self.motors[key].index)
    goal = self.motors[key].closeGoal
    after = self.motors[key].closeAfter
    self.queue.put(['slow',[key,goal,after]])

  def exit(self):
    self.queue.put(['exit'])

  def openAll(self):
    logger.debug('open all')
    for key in self.motors:
      self.openGateFast(key)

  def closeAll(self):
    logger.debug('close all')
    for key in self.motors:
      self.closeGateFast(key)

  def releaseAll(self):
    for key in self.motors:
      self.motors[key].lock.acquire()
      try:
        self.pwm.set(self.motors[key].index,0)
      finally:
        self.motors[key].lock.release()

  def testGates(self):
    for key in self.motors:
      self.openGate(key)
      time.sleep(2)
      self.closeGate(key)
      time.sleep(2)

  def run(self):
    while True:
      if self.queue.empty() is not True:
        data = self.queue.get()
        if data[0] == 'exit':
          break
        elif data[0] == 'fast':
          p = Process(target=self._moveFast,args=(data[1][0],data[1][1],data[1][2],))
        elif data[0] == 'slow':
          p = Process(target=self._moveSlow,args=(data[1][0],data[1][1],data[1][2],))
        p.start()
    
  class _Motor(object):
    def __init__(self,key=None,index=None,openGoal=0,openAfter=0,closeGoal=0,closeAfter=0):
      self.key=key
      self.index=index
      self.closeGoal=closeGoal
      self.closeAfter=closeAfter
      self.openGoal=openGoal
      self.openAfter=openAfter
      self.position=0
      self.lock = Lock()
      self.moving = False

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
  motors = MazerMotors()
  try:
    p = Process(target=motors.run)
    p.start()
    time.sleep(2)
    motors.openGateFast('OUL')
    time.sleep(1)
    motors.closeGateFast('OUL')
    time.sleep(1)
    motors.openGate('OUL')
    motors.openGate('IUL')
    motors.closeAll()
    motors.openAll()
    motors.releaseAll()

    time.sleep(1)
    motors.exit()
    p.join()
  except:
    raise NameError ('aaa')
