#!/usr/bin/python3
# Maze control
# Author: Ariel Burman

MAZEVERSION = 1.3

import logging
import time
from importlib import util
from multiprocessing import Process, Queue

from mazeprotocols import MazeProtocols

logger = logging.getLogger('Maze')

def check_module(module_name):
  """
  Checks if module can be imported without actually
  importing it
  """
  module_spec = util.find_spec(module_name)
  if module_spec is None:
      logger.debug('Module: {} not found'.format(module_name))
      return None
  else:
      logger.debug('Module: {} can be imported!'.format(module_name))
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

def isfloat(val):
  try:
    float(val)
    return True
  except:
    return False

def parserProtocol(subject):
  filename = 'subjects/' + subject + '.cfg'
  try:
    filen = open(filename,'r')
  except:
    print('Configuration File is missing. Creating one from template Test.example')
    import shutil
    shutil.copy('subjects/Test.example',filename)
    logger.info('Using configuration template')
    filen = open(filename,'r')
  lines = filen.readlines()
  filen.close()
  import re

  protocolOptions = {}
  protocolFile = ''
  protocolClass = ''

  for line in lines:
    #get rid of comments
    line = re.split('#', line)
    line = [i.strip() for i in line]
    if line[0] == '':
      continue
    line = re.split('=', line[0])
    line = [i.strip() for i in line]
    if len(line) == 1:
      pass
    if line[0] == 'protocolFile':
      protocolFile = line[1]
    elif line[0] == 'protocolClass':
      protocolClass = line[1]
    else:
      if line[1].isdecimal():
        protocolOptions[line[0]] = int(line[1])
      elif isfloat(line[1]):
        protocolOptions[line[0]] = float(line[1])
      else:
        #is not a float or int, so we pass it as string
        protocolOptions[line[0]] = line[1]
 
  # validate options
  if protocolFile == '':
    raise NameError("Protocol file name not defined")
  if protocolClass == '':
    raise NameError("Protocol Class name not defined")
  return protocolFile,protocolClass,protocolOptions

class Maze(object):
  def __init__(self,protocolFile,protocolClass,protocolOptions=None):
    module_spec = check_module('protocols.'+protocolFile)
    if module_spec:
        module = util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
    else:
        raise NameError("Module doesn't exist")

    if protocolClass in dir(module):
        Protokol = getattr(module,protocolClass)
    else:
        raise NameError("Class doesn't exist")

    logger.info('Initializing Maze')
    logger.info('Maze version {a}'.format(a=MAZEVERSION))


    self.protocol = Protokol(protocolOptions)

  def start(self):
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
    time.sleep(.2)
    sys.exit()

def main(argv=None):
  import sys,os
  if sys.version_info < (3,5,3):
      print ('Python 3.5.3 and above is needed')
      exit(1)
  if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

  try:
    subjectname = argv[1]
  except:
    print('''Warning: Subject Name is missing. Using 'Test' ''') # 'Reed' 'Sue' 'Jhonny' 'Ben'
    subjectname='Test'
  print('Subject Name: {a}'.format(a=subjectname))
  
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
  
  loglevel=logging.INFO
  dateformat = '%H:%M:%S'
  formatter_str = '%(asctime)s.%(msecs)03d;%(name)s;%(levelname)s;%(message)s'
  try:
    if argv[2]=='--debug':
      print('Loggin DEBUG mode')
      formatter_str = '%(asctime)s.%(msecs)03d;%(name)s;%(levelname)s;p%(process)s{%(filename)s:%(lineno)d};%(message)s'
      loglevel=logging.DEBUG
  except:
    pass

  logging.basicConfig(filename=logfile,filemode='w+',level=loglevel,
         format=formatter_str, datefmt=dateformat)
  logger.info('Today\'s date: '+today)
  [protocolFile,protocolClass,protocolOptions] = parserProtocol(subjectname)
  print('Using Protocol: {}'.format(protocolClass))
  maze = Maze(protocolFile,protocolClass,protocolOptions)

  try:
    maze.start()

  except Exception as inst:
    print ('Exception ocurred')
    print(inst)
    logger.exeption('Exception ocurred')
    logger.error(inst.args)


if __name__ == '__main__':
    import sys
    main(sys.argv)
