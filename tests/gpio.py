import gpiozero
#from signal import pause
import signal
import time


import logging

logger = logging.getLogger(__name__)



class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    self.kill_now = True

def giveWarning1():
  logger.info("paso la rata 1")
  print ("paso la rata 1")

def giveWarning2():
  logger.info("paso la rata 2")
  print ("paso la rata 2")

def giveWarning3():
  logger.info("paso la rata 3")
  print ("paso la rata 3")

def giveWarning4():
  logger.info("paso la rata 4")
  print ("paso la rata 4")

def giveWarning5():
  logger.info("paso la rata 5")
  print ("paso la rata 5")

def giveWarning6():
  logger.info("paso la rata 6")
  print ("paso la rata 6")

def giveWarning7():
  logger.info("paso la rata 7")
  print ("paso la rata 7")


sensor1 = gpiozero.Button(4)
sensor2 = gpiozero.Button(17)
sensor3 = gpiozero.Button(18)
sensor4 = gpiozero.Button(27)
sensor5 = gpiozero.Button(22)
sensor6 = gpiozero.Button(23)
sensor7 = gpiozero.Button(24)

sensor1.when_pressed = giveWarning1
sensor2.when_pressed = giveWarning2
sensor3.when_pressed = giveWarning3
sensor4.when_pressed = giveWarning4
sensor5.when_pressed = giveWarning5
sensor6.when_pressed = giveWarning6
sensor7.when_pressed = giveWarning7

if __name__ == '__main__':
    import sys,os
    if not os.path.exists('./logs/'):
      os.makedirs('./logs/')
    dateformat = '%Y/%m/%d %H:%M:%S'
    formatter_str = '%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s'
    logfile = 'logs/gpio.log'

    logging.basicConfig(filename=logfile,filemode='w+',level=logging.DEBUG,
           format=formatter_str, datefmt=dateformat)

    logger.info('GPIO Test')
    killer = GracefulKiller()
    while True:
        time.sleep(.1)
        if killer.kill_now:
          break
    
    logger.info('Final')
