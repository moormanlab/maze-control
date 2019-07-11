#!/usr/bin/python3
# Manul Maze control
# Author: Ariel Burman

import termios, fcntl, sys, os
if sys.version_info < (3,5,3):
    print ('Python 3.5.3 and above is needed')
    exit(1)

if not os.path.exists('./logs/'):
  os.makedirs('./logs/')
import datetime
import logging
dateformat = '%H:%M:%S'
formatter_str = '%(asctime)s.%(msecs)03d;%(name)s;%(levelname)s;%(message)s'
logger = logging.getLogger('ManualControl')
today = datetime.date.today().strftime("%Y-%m-%d")
logfile = 'logs/manual.log'
logging.basicConfig(filename=logfile,filemode='w+',level=logging.DEBUG,
       format=formatter_str, datefmt=dateformat)
logger.info('Today\'s date: '+today)
logger.info('Manual Maze Control')

from mazehal.valves import MazeValves
from mazehal.gates import MazeGates
import time
fd = sys.stdin.fileno()
oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)
oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)


def printhelp():
    print ('------------------------------')
    print ('w : outter upper left')
    print ('s : outter bottom left')
    print ('e : inner upper left')
    print ('d : inner bottom left')
    print ('r : inner upper right')
    print ('f : inner bottom right')
    print ('t : outter upper right')
    print ('g : outter bottom right')
    print ('z : open left valve')
    print ('x : close left valve')
    print ('c : drop left valve')
    print ('n : open right valve')
    print ('b : close right valve')
    print ('v : drop right valve')
    print ('? o h : help')
    print ('q : exit')
    print ('------------------------------')

try:
    from multiprocessing import Process
    gates = MazeGates()
    valves = MazeValves()
    p = Process(target=gates.run)
    p.start()
    printhelp()
    gates.openAllFast()
    time.sleep(3)
    gates.releaseAll()
    while True:
        try:
            gate = None
            valve = None
            c = sys.stdin.read(1)
            if c == 'w':
                gate = 'OUL'
            elif c == 's':
                gate = 'OBL'
            elif c == 'e':
                gate = 'IUL'
            elif c == 'd':
                gate = 'IBL'
            elif c == 'r':
                gate = 'IUR'
            elif c == 'f':
                gate = 'IBR'
            elif c == 't':
                gate = 'OUR'
            elif c == 'g':
                gate = 'OBR'
            elif c == 'z':
                valve = 'L'
                cmd='open'
            elif c == 'x':
                valve = 'L'
                cmd='close'
            elif c == 'c':
                valve = 'L'
                cmd='drop'
            elif c == 'n':
                cmd='open'
                valve = 'R'
            elif c == 'b':
                valve = 'R'
                cmd='close'
            elif c == 'v':
                valve = 'R'
                cmd='drop'
            elif c == '?' or c == 'h':
                printhelp()
            elif c == 'q':
                print ('exiting')
                break
            if gate is not None:
              print(gate)
              logger.info('gate = {a}'.format(a=gate))
              if gates.isOpen(gate):
                gates.closeGateFast(gate)
              elif gates.isClose(gate):
                gates.openGateFast(gate)
              else:
                logger.info('{a} is moving'.format(a=gate))
            if valve is not None:
              print(cmd + ' ' + valve)
              logger.info('{a} valve {b}'.format(a=cmd,b=valve))
              if cmd == 'open':
                valves.open(valve)
              elif cmd == 'close':
                valves.close(valve)
              elif cmd == 'drop':
                valves.drop(valve)
              else:
                logger.error('Error in valves')
        except IOError:
            print ('error capturing')
finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
    gates.exit()
    p.join()
