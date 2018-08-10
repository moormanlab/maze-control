# Motor control for maze
# Author: Ariel Burman

import time
import logging

logger=logging.getLogger(__name__)

import adai2c as pwm
# Uncomment to enable debug output.
#logging.basicConfig(level=logging.DEBUG)

from multiprocessing import Process, Queue, Lock, Value

# motor | open       | close       | key | position
# 0     | 220 -> 222 | 540 -> 534  | IUL | inner upper left 
# 1     | 545 -> 535 | 195 -> 205  | IBL | inner bottom left
# 2     | 210 -> 215 | 555 -> 542  | OBL | outter bottom left
# 3     | 545 -> 535 | 200 -> 210  | OUL | outter upper left
# 4     | 520 -> 510 | 220 -> 222  | OBR | outter bottom right
# 5     | 225 -> 230 | 550 -> 545  | OUR | outter upper right
# 6     | 195 -> 200 | 500 -> 492  | IBR | inner bottom right
# 7     | 545 -> 540 | 200 -> 205  | IUR | inner upper right


#        /----------------\   /----------------\
#       /                  \-/                  \
#      /   /-------------\     /-------------\   \
#     |   / OUL(3) (0)IUL \   / IUR(7) (5)OUR \   |
#     |   |               |   |               |   |
#     |   |               |   |               |   |
#     |   \ OBL(2) (1)IBL /   \ IBR(6) (4)OBR /   |
#      \   \-------------/     \-------------/   /
#       \                  /-\                  /
#        \----------------/   \----------------/

from ctypes import c_bool,c_int

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
                 'IBR': (6,[195, 200, 500, 492]),
                 'IUR': (7,[545, 540, 200, 205]) }
    self.motors = {}
    self.queue = Queue()
    for key in self.pwmV:
        self.motors[key]=MazerMotors.Motor(key=key,index=self.pwmV[key][0],
                openGoal=self.pwmV[key][1][0],openAfter=self.pwmV[key][1][1],
                closeGoal=self.pwmV[key][1][2],closeAfter=self.pwmV[key][1][3])
    logger.info('MazerMotors id %s ',id(self))

  def _moveSlow(self,key,goal,after):
    gate = self.motors[key].index
    now = self.motors[key].getPosition()
    self.motors[key].lock.acquire()
    self.motors[key].setMoving(True)
    try:
      if goal > now:
          diff = 1
      else:
          diff = -1
      #steps = 50
      #diff = int((goal-now)/steps)
      #logger.info('Slow gate %s | now %s | goal %s | after %s | diff %s moving %s',gate,now,goal,after,diff,self.motors[key].isMoving())
      while (goal != now):
        now += diff
        logger.info('gate %s now %s',gate,now)
        self.pwm.set(gate,now)
        time.sleep(0.002)
        self.motors[key].setPosition(now)
      self.pwm.set(gate,goal)
      self.motors[key].setPosition(goal)
      time.sleep(0.1)
      self.pwm.set(gate,after)
      self.motors[key].setPosition(after)
      logger.debug('gate %s position after = %s',self.motors[key].index,self.motors[key].getPosition())
    except Exception as e:
      print (e)
      self.motors[key].lock.release()
    finally:
      self.motors[key].lock.release()
      self.motors[key].setMoving(False)

  def _moveFast(self,key,goal,after):
    gate = self.motors[key].index
    self.motors[key].lock.acquire()
    self.motors[key].setMoving(True)
    now=self.motors[key].getPosition()
    logger.info('Fast gate %s | now %s | goal %s | after %s',gate,now,goal,after)
    try:
      self.pwm.set(gate,goal)
      self.motors[key].setPosition(goal)
      time.sleep(0.5)
      self.pwm.set(gate,after)
      self.motors[key].setPosition(after)
      logger.debug('gate %s position after = %s',self.motors[key].index,self.motors[key].getPosition())
    except Exception as e:
      print (e)
      self.motors[key].lock.release()
    finally:
      self.motors[key].lock.release()
      self.motors[key].setMoving(False)

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
      except Exception as e:
        print (e)
        self.motors[key].lock.release()
      finally:
        self.motors[key].lock.release()

  def testGates(self):
    for key in self.motors:
      self.openGate(key)
      time.sleep(3)
      self.closeGate(key)
      time.sleep(3)

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
      msg = ""
      for key in self.motors:
        msg = msg + "M {index} mv = {isit}|".format(index=self.motors[key].index,isit=self.motors[key].isMoving())
      logger.debug(msg)
      time.sleep(0.1)
    
  class Motor(object):
    def __init__(self,key=None,index=None,openGoal=0,openAfter=0,closeGoal=0,closeAfter=0):
      logger.info('Motors %s id %s ',index,id(self))
      self.key=key
      self.index=index
      self.closeGoal=closeGoal
      self.closeAfter=closeAfter
      self.openGoal=openGoal
      self.openAfter=openAfter
      self.lock = Lock()
      self._position=Value(c_int,0)
      self._moving = Value(c_bool,False)

    def setPosition(self,val):
      self._position.value = int(val)

    def getPosition(self):
      return int(self._position.value)

    def setMoving(self,val):
      self._moving.value = bool(val)

    def isMoving(self):
      return bool(self._moving.value)

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
    #time.sleep(2)
    motors.openGateFast('OUL')
    #time.sleep(3)
    motors.closeGateFast('OUL')
    #time.sleep(3)
    motors.closeAll()
    #time.sleep(3)
    motors.testGates()
    motors.releaseAll()
    motors.exit()
    p.join()
  except:
    raise NameError ('aaa')
