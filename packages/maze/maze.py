#!/usr/bin/python3
# Maze control
# Author: Ariel Burman

MAZEVERSION = 1.1

import logging
import time
import importlib
#from importlib import util as imputil
from multiprocessing import Process, Queue

from mazeprotocols import MazeProtocols

logger = logging.getLogger(__name__)

def check_module(module_name):
  """
  Checks if module can be imported without actually
  importing it
  """
  logger.debug(module_name)
  logger.debug(dir(importlib))
  module_spec = importlib.util.find_spec(module_name)
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
    logger.info('Maze version {a}'.format(a=MAZEVERSION))


    self.protocol = Protokol()
    #protocolP.daemon = True
    #self.keyboardP = Process(target=self.keyboardCap)
    #self.keyboardP.daemon=True

  def start(self):
      #self.keyboardP.start()
      self.protocolP = Process(target=self.protocol._run)
      self.protocolP.start()
      self.run()
  
#  def keyboardCap(self):
#    with keyboard.Listener(on_press=self.keyPress) as listener:
#      listener.join()

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
          time.sleep(.2)
          c = sys.stdin.read(1)
          if c == 'e':
            print('open left')
            self.protocol._mazehal.valves.open('L')
          elif c == 'd':
            self.protocol._mazehal.valves.close('L')
            print('close left')
          elif c == 'c':
            print('drop left')
            self.protocol.drop('L')
          elif c == 't':
            self.protocol._mazehal.valves.open('R')
            print('open right')
          elif c == 'g':
            self.protocol._mazehal.valves.close('R')
            print('close right')
          elif c == 'b':
            self.protocol.drop('R')
            print('drop right')
          elif c == 'u':
            print ('set how many drops : ')
            c = sys.stdin.read(1)
            while c == '':
              c = sys.stdin.read(1)
            print ('will set {a} drops'.format(a=c))
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
          elif c == 'm':
            print ('set delay multi drop : ')
            c = sys.stdin.read(1)
            while c == '':
              c = sys.stdin.read(1)
            print ('will set multidrop delay {a}'.format(a=c))
          elif c == '?' or c == 'h':
              printhelp()
          elif c == 'q':
              print ('exiting')
              self.exit()

      except Exception as e:
          logger.error('#################################')
          logger.error(e)
          logger.error('#################################')
      finally:
          print ('#####Program ended#######')
          termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
          fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

  def forceOpenAllGates(self):
    self.protocol.mazehal.gates.openAllFast()

  def forceDrop(self,key):
    pass

  def pause(self):
    logger.warning('pausing')

  def exit(self):
    logger.warning('Exiting')
    self.protocolP.terminate()
    sys.exit()
      
if __name__ == '__main__':
  import sys,os
  if not os.path.exists('./logs/'):
    os.makedirs('./logs/')
  dateformat = '%H:%M:%S'
  formatter_str = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
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
  logger.info('Today\'s date: '+today)
  logger.info('maze test')
  #maze = Maze('skinner','Skinner')
  protocolFile = 'blockchoice'
  protocolClass = 'BlockChoice'
  protocolOption = None
  maze = Maze(protocolFile,protocolClass)
  
  try:
    maze.start()

  except Exception as inst:
    print ('Exception ocurred')
    print(inst)
    logger.exeption('Exception ocurred')
    logger.error(inst.args)
