#!/usr/bin/python3
# Maze control
# Author: Ariel Burman

MAZEVERSION = 1.0

import logging
import time
import importlib
from importlib import util as imputil
from multiprocessing import Process, Queue

from mazehal import MazeHal
from mazeprotocols import MazeProtocols

logger = logging.getLogger(__name__)

def check_module(module_name):
    """
    Checks if module can be imported without actually
    importing it
    """
    logger.debug(module_name)
    logger.debug(dir(importlib))
    module_spec = imputil.find_spec(module_name)
    if module_spec is None:
        logger.info('Module: {} not found'.format(module_name))
        return None
    else:
        logger.info('Module: {} can be imported!'.format(module_name))
        return module_spec

def printhelp():
    print ('------------------------------')
    print ('e : open left')
    print ('d : close left')
    print ('c : drop left')
    print ('t : open right')
    print ('g : close right')
    print ('b : drop right')
    print ('u : set drops')
    print ('j : set delay drop')
    print ('m : set delay multi drop')
    print ('? o h : help')
    print ('q : exit')
    print ('------------------------------')


class Maze(object):

  def __init__(self,protocolFile=None,protocolClass=None):
    module_spec = check_module('protocols.'+protocolFile)
    if module_spec:
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
    else:
        raise NameError("Module doesn't exist")

    if protocolClass in dir(module):
        Protokol = getattr(module,protocolClass)
    else:
        raise NameError("Class doesn't exist")

    logger.info('Initializing Maze')
    logger.debug('Maze id %s ',id(self))
    logger.info('Maze version {a}'.format(a=MAZEVERSION))
    self.qC = Queue()
    self.qR = Queue()

    self.protocol = Protokol(queueCommands=self.qC,queueResponses=self.qR)
    self.protocol.init()
    self.protocolP = Process(target=self.protocol.run)

    if 'sensorHandler' in dir(self.protocol):
      sensorHandler = self.protocol.sensorHandler
    else:
      sensorHandler = None

    if 'buttonHandler' in dir(self.protocol):
      buttonHandler = self.protocol.buttonHandler
    else:
      buttonHandler = None

    self.hal = MazeHal(queueCommands=self.qC,queueResponses=self.qR,
            sensorHandler=sensorHandler,buttonHandler=buttonHandler)
    self.halP = Process(target=self.hal._run)

  def start(self):
    if self.protocol == None:
      logger.debug('No protocol assigned')
    else:
      self.halP.start()
      self.protocolP.start()

  def run(self):
    import termios, fcntl, sys, os
    fd = sys.stdin.fileno()
    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)
    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
    printhelp()
    try:

      while True:
        time.sleep(.5)
        c = sys.stdin.read(1)
        if c == 'e':
          msg = ['valve','open','L']
          self.qC.put(msg)
          print('open left')
        elif c == 'd':
          msg = ['valve','close','L']
          self.qC.put(msg)
          print('close left')
        elif c == 'c':
          msg = ['valve','drop','L']
          self.qC.put(msg)
          print('drop left')
        elif c == 't':
          msg = ['valve','open','R']
          self.qC.put(msg)
          print('open right')
        elif c == 'g':
          msg = ['valve','close','R']
          self.qC.put(msg)
          print('close right')
        elif c == 'b':
          msg = ['valve','drop','R']
          self.qC.put(msg)
          print('drop right')
        elif c == 'u':
          print ('set how many drops : ')
          c = sys.stdin.read(1)
          while c == '':
            c = sys.stdin.read(1)
          print ('will set {a} drops'.format(a=c))
          msg = ['valve','smd',c]
          self.qC.put(msg)
        elif c == 'j':
          print ('set delay drop : ')
          c = sys.stdin.read(1)
          while c == '':
            c = sys.stdin.read(1)
            n = 0
            while c != 'e':
              n *= 10
              n += int(c)
              c = sys.stdin.read(1)
            print ('will set drop delay {a}'.format(a=n))
          #msg = ['valve','sdd',c]
          #self.qC.put(msg)
        elif c == 'm':
          print ('set delay multi drop : ')
          c = sys.stdin.read(1)
          while c == '':
            c = sys.stdin.read(1)
          print ('will set multidrop delay {a}'.format(a=c))
          #msg = ['valve','smdd',c]
          #self.qC.put(msg)
        elif c == '?' or c == 'h':
            printhelp()
        elif c == 'q':
            print ('exiting')
            break
    except IOError:
      print ('error capturing HEERERERERE')
      logger.error('error capturing HEERERERERE')
    except Exception as e:
        print ('#################################')
        print (e)
        print ('#################################')
        logger.error('#################################')
        logger.error(e)
        logger.error('#################################')
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
    finally:
        print ('#####FINALYY#######')
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
        self.exit()
#        self.protocolP.join()
#        self.halP.join()

  def forceOpenAllGates(self):
    msg = ['gate','openAllNow']
    self.qC.put(msg)

  def forceDrop(self,key):
    pass

  def pause(self):
    logger.warning('pausing')

  def exit(self):
    logger.warning('exiting')
    self.halP.terminate()
    self.protocolP.terminate()
    sys.exit()
      
if __name__ == '__main__':
  import sys,os
  if not os.path.exists('./logs/'):
    os.makedirs('./logs/')
  dateformat = '%Y/%m/%d %H:%M:%S'
  formatter_str = '%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s'
  subjectname = 'Test' # 'Reed' 'Sue' 'Jhonny' 'Ben'
  import datetime
  today = datetime.date.today().strftime("%Y-%m-%d")
  Snum = 0
  while True:
    Snum += 1
    logfile = 'logs/' + subjectname + '-' + today + '-S' + format(Snum, '02d') + '.log'
    if os.path.isfile(logfile) == False:
        break
    if Snum == 99:
        raise NameError('Too many sessions in one day')

  logging.basicConfig(filename=logfile,filemode='w+',level=logging.DEBUG,
         format=formatter_str, datefmt=dateformat)

  logger.info('maze test')
  #maze = Maze('skinner','Skinner')
  maze = Maze('classic','Classic')
  maze.start()
  
  try:
    maze.run()
    print('im here')

  except Exception as inst:
    print ('im heeeeeereeeeeeEEEEEEEEEEEEEEEEEEEEEE')
    print(inst)

    logger.warning(type(inst))
    logger.warning(inst.args)
    maze.exit()
    sys.exit()
