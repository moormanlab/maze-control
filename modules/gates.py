# Motor control for maze
# Author: Ariel Burman

import time
import logging

logger=logging.getLogger(__name__)

#import modules.adai2c as pwm
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

pwmV = {'IUL': (0,[220, 222, 540, 534]),
        'IBL': (1,[545, 535, 195, 205]),
        'OBL': (2,[210, 215, 555, 542]),
        'OUL': (3,[545, 535, 200, 210]),
        'OBR': (4,[520, 510, 220, 222]),
        'OUR': (5,[225, 230, 550, 545]),
        'IBR': (6,[195, 200, 500, 492]),
        'IUR': (7,[545, 540, 200, 205]) }

class Motor(object):
  def __init__(self,index=None):
    logger.info('Motors %s id %s ',index,id(self))
    self.index=index
    self.pwm = pwm.AdaI2C()
    self._position=Value(c_int,0)

  def setPosition(self,val):
    self.pwm.set(self.index,val)
    if val > 0 :
        self._position.value = int(val)

  def getPosition(self):
    return int(self._position.value)



class Gate(object):
  def __init__(self,name=None,index=None,openGoal=0,openAfter=0,closeGoal=0,closeAfter=0):
    self.name = name
    self.openGoal=openGoal
    self.openAfter=openAfter
    self.closeGoal=closeGoal
    self.closeAfter=closeAfter
    self.motor = Motor(index=index)
    self._moving = Value(c_bool,False)
    self.lock = Lock()

  def setMoving(self,val):
    self._moving.value = bool(val)

  def isMoving(self):
    return bool(self._moving.value)

  def isOpen(self):
    return self.motor.getPosition()==self.openAfter

  def isiClose(self):
    return self.motor.getPosition()==self.closeAfter

  def _moveSlow(self,goal,after):
    self.lock.acquire()
    logger.debug('started move Slow %s',self.name)
    now = self.motor.getPosition()
    self.setMoving(True)
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
        logger.info('gate %s now %s',self.name,now)
        self.motor.setPosition(now)
        time.sleep(0.002)
        #self.motors[key].setPosition(now)
      self.motor.setPosition(goal)
      time.sleep(0.1)
      self.motor.setPosition(after)
      logger.debug('gate %s position after = %s',self.name,self.motor.getPosition())
    except Exception as e:
      print (e)
      self.lock.release()
    finally:
      logger.debug('ended move Slow %s',self.name)
      self.lock.release()
      self.setMoving(False)

  def _moveFast(self,goal,after):
    self.lock.acquire()
    logger.debug('started move Fast %s',self.name)
    self.setMoving(True)
    now=self.motor.getPosition()
    logger.info('Fast gate %s | now %s | goal %s | after %s',self.name,now,goal,after)
    try:
      self.motor.setPosition(goal)
      time.sleep(0.5)
      self.motor.setPosition(after)
      logger.debug('gate %s position after = %s',self.name,self.motor.getPosition())
    except Exception as e:
      print (e)
      self.lock.release()
    finally:
      logger.debug('ended move Fast %s',self.name)
      self.lock.release()
      self.setMoving(False)

  def openGateFast(self):
    logger.debug('openF %s',self.name)
    self._moveFast(self.openGoal,self.openAfter)

  def closeGateFast(self):
    logger.debug('closeF %s',self.name)
    self._moveFast(self.closeGoal,self.closeAfter)

  def openGate(self):
    logger.debug('openS %s',self.name)
    self._moveSlow(self.openGoal,self.openAfter)

  def closeGate(self):
    logger.debug('closeS %s',self.name)
    self._moveSlow(self.closeGoal,self.closeAfter)

  def _release(self):
    logger.debug('release %s',self.name)
    self.motor.setPosition(0)


class MazeGates(object):
  def __init__(self):
    # Initialise the PCA9685 using the default address (0x40).
    # Set frequency to 60hz, good for servos.
    self.gate = {}
    self.queue = Queue()
    for key in pwmV:
        self.gate[key]=Gate(name=key,index=pwmV[key][0],
                openGoal=pwmV[key][1][0],openAfter=pwmV[key][1][1],
                closeGoal=pwmV[key][1][2],closeAfter=pwmV[key][1][3])
    logger.info('MazerMotors id %s ',id(self))

  def _emptyQ(self):
    while self.queue.empty() is not True:
      data = self.queue.get()

  def openGateFast(self,key):
    logger.debug('command openF %s',key)
    self.queue.put(['of',key])

  def closeGateFast(self,key):
    logger.debug('command closeF %s',key)
    self.queue.put(['cf',key])

  def openGate(self,key):
    logger.debug('command openS %s',key)
    self.queue.put(['os',key])

  def closeGate(self,key):
    logger.debug('command closeS %s',key)
    self.queue.put(['os',key])

  def isMoving(self,key):
    return self.gate[key].isMoving()

  def isOpen(self,key):
    return self.gate[key].isClose()

  def isClose(self,key):
    return self.gate[key].isOpen()

  def exit(self):
    self.queue.put(['exit'])

  def openAll(self):
    self._emptyQ()
    logger.debug('command open all')
    for key in self.gate:
      self.openGateFast(key)

  def closeAll(self):
    self._emptyQ()
    logger.debug('command close all')
    for key in self.gate:
      self.closeGateFast(key)

  def releaseAll(self):
    self._emptyQ()
    logger.debug('close all')
    for key in self.gate:
      self.gate[key]._release()

  def testGates(self):
    for key in self.gate:
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
        elif data[0] == 'of':
          p = Process(target=self.gate[data[1]].openGateFast)
        elif data[0] == 'cf':
          p = Process(target=self.gate[data[1]].closeGateFast)
        elif data[0] == 'os':
          p = Process(target=self.gate[data[1]].openGate)
        elif data[0] == 'oc':
          p = Process(target=self.gate[data[1]].closeGate)
        p.start()
      msg = ""
      for key in self.gate:
        msg = msg + "M {index} mv = {isit}|".format(index=key,isit=self.isMoving(key))
      logger.debug(msg)
      time.sleep(0.1)
    

if __name__ == '__main__':
  import sys,os
  if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

  dateformat = '%Y/%m/%d %H:%M:%S'
  formatter_str = '%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s'
  logfile = 'logs/gates.log'

  logging.basicConfig(filename=logfile,filemode='w+',level=logging.DEBUG,
          format=formatter_str, datefmt=dateformat)

  logger.info('Gates test')
  gates = MazeGates()
  try:
    p = Process(target=gates.run)
    p.start()
    time.sleep(0.5)
    gates.openGateFast('OUL')
    gates.openGate('IUL')
    gates.openGate('IBL')
    time.sleep(1.5)
    gates.closeGateFast('OUL')
    time.sleep(1.5)
    gates.closeAll()
    time.sleep(1.5)
    gates.testGates()
    time.sleep(0.1)
    gates.releaseAll()
    time.sleep(1.5)
    gates.exit()
    p.join()
  except:
    raise NameError ('aaa')
