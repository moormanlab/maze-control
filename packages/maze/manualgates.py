from mazehal.gates import MazeGates


import termios, fcntl, sys, os
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
    print ('q : open left')
    print ('a : close left')
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

try:
    from multiprocessing import Process
    gates = MazeGates()
    p = Process(target=gates.run)
    p.start()
    printhelp()
    gates.openAllFast()
    time.sleep(2)
    gates.releaseAll()
    while True:
        try:
            gate = None
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
            elif c == '?' or c == 'h':
                printhelp()
            elif c == 'q':
                print ('exiting')
                break
            if gate is not None:
              if gates.isOpen(gate):
                gates.closeGateFast(gate)
              elif gates.isClose(gate):
                gates.openGateFast(gate)
        except IOError:
            print ('error capturing')
finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
    gates.exit()
    p.join()
