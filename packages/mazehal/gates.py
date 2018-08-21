# Gates control for maze
# Author: Ariel Burman

GATEVERSION = 1.1

import time
from multiprocessing import Process, Queue, Lock, Value
from ctypes import c_bool,c_int

import logging
logger=logging.getLogger(__name__)

import adai2c as pwm

# motor | open       | close       | key | position
# 0     | 220 -> 222 | 540 -> 534  | IUL | inner upper left 
# 1     | 545 -> 535 | 195 -> 205  | IBL | inner bottom left
# 2     | 210 -> 215 | 555 -> 542  | OBL | outter bottom left
# 3     | 545 -> 542 | 200 -> 210  | OUL | outter upper left
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


pwmV = {'IUL': (0,[218, 228, 537, 530]),
        'IBL': (1,[545, 528, 195, 210]),
        'OBL': (2,[210, 220, 555, 544]),
        'OUL': (3,[570, 552, 206, 213]),
        'OBR': (4,[520, 510, 220, 222]),
        'OUR': (5,[225, 230, 550, 545]),
        'IBR': (6,[195, 200, 500, 492]),
        'IUR': (7,[545, 540, 200, 205]) }


class Motor(object):
  def __init__(self,index=None):
    logger.debug('Motors %s id %s ',index,id(self))
    self.index=index
    self.pwm = pwm.AdaI2C()
    self._position=Value(c_int,380) #start at middle point

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

  def isClose(self):
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
      steps = 20
      diff = ((goal-now)/steps)
      for i in range(steps):
        now += diff
        logger.debug('gate %s now %s',self.name,int(now))
        if now < 10 or now > 600:
          raise NameError('pwm value exceeded maximum safe value')
        self.motor.setPosition(int(now))
        time.sleep(.8/steps)
        #self.motors[key].setPosition(now)
      self.motor.setPosition(goal)
      time.sleep(0.05)
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
    logger.debug('Fast gate %s | now %s | goal %s | after %s',self.name,now,goal,after)
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
#    self.processRunning = []
    for key in pwmV:
        self.gate[key]=Gate(name=key,index=pwmV[key][0],
                openGoal=pwmV[key][1][0],openAfter=pwmV[key][1][1],
                closeGoal=pwmV[key][1][2],closeAfter=pwmV[key][1][3])
    logger.debug('Maze Gates id %s ',id(self))
    logger.info('Gates version {a}'.format(a=GATEVERSION))

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
    self.queue.put(['cs',key])

  def isMoving(self,key):
    return self.gate[key].isMoving()

  def isOpen(self,key):
    return self.gate[key].isOpen()

  def isClose(self,key):
    return self.gate[key].isClose()

  def exit(self):
    self.queue.put(['exit'])

  def openAll(self):
    #self._emptyQ()
    logger.debug('command open all')
    for key in self.gate:
      self.openGate(key)

  def closeAll(self):
    #self._emptyQ()
    logger.debug('command close all')
    for key in self.gate:
      self.closeGate(key)

  def openAllFast(self):
    #self._emptyQ()
    logger.debug('command open all fast')
    for key in self.gate:
      self.openGateFast(key)

  def releaseAll(self):
    self._emptyQ()
    logger.debug('close all')
    for key in self.gate:
      self.gate[key]._release()

  def testAllOnce(self):
    for key in self.gate:
      self.openGate(key)
    time.sleep(2)
    for key in self.gate:
      self.closeGate(key)
    time.sleep(2)

  def testGates(self):
    for key in self.gate:
      self.openGate(key)
      time.sleep(2)
      self.closeGate(key)
      time.sleep(2)

  def run(self):
    while True:
#      for p in self.proccess:
#        if p.
      

      if self.queue.empty() is not True:
        data = self.queue.get()
        logger.debug('new data %s',data)
        if data[0] == 'exit':
          logger.info('Exiting Gates Process')
          break
        elif data[0] == 'of':
          p = Process(target=self.gate[data[1]].openGateFast)
        elif data[0] == 'cf':
          p = Process(target=self.gate[data[1]].closeGateFast)
        elif data[0] == 'os':
          p = Process(target=self.gate[data[1]].openGate)
        elif data[0] == 'cs':
          p = Process(target=self.gate[data[1]].closeGate)
        else:
          raise NameError('Messege not implemented')
        p.start()
#        print(id(p))
#        self.processrunning.append(p)

      msg = "Moving: "
      for key in self.gate:
        if self.isMoving(key):
          msg = msg + "{index} ".format(index=key)
      logger.debug(msg)
      msg = "Open: "
      for key in self.gate:
        if self.isOpen(key):
          msg = msg + "{index} ".format(index=key)
      logger.debug(msg)
      msg = "Close: "
      for key in self.gate:
        if self.isClose(key):
          msg = msg + "{index} ".format(index=key)
      logger.debug(msg)
      time.sleep(0.1)
    self.releaseAll()
    

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
    gates.openGateFast('IUL')
    gates.openGateFast('IUL')
    gates.openGate('IUR')
    while gates.isOpen('IUR') == False:
        pass
    gates.closeGateFast('IUL')
    time.sleep(1.5)

    logger.info('Gates Clossing')
    gates.closeAll()
    while gates.isClose('IUR') == False:
        pass
    while gates.isClose('IUL') == False:
        pass
    logger.info('Gates Test')
    gates.testGates()
    gates.testAllOnce()
    time.sleep(1.5)
    logger.info('Exiting')
    gates.releaseAll()
    gates.exit()
    p.join()
  except:
    raise NameError ('aaa')
