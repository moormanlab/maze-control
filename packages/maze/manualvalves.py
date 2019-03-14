from mazehal.valves import MazeValves
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

try:
    a = MazeValves()
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
            c = sys.stdin.read(1)
            if c == 'e':
                a.open('L')
                print('open left')
            elif c == 'd':
                a.close('L')
                print('close left')
            elif c == 'c':
                a.drop('L')
                print('drop left')
            elif c == 't':
                a.open('R')
                print('open right')
            elif c == 'g':
                a.close('R')
                print('close right')
            elif c == 'b':
                a.drop('R')
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
                    while c == '':
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
                break
        except IOError:
            print ('error capturing')
finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
    gates.exit()
    p.join()
