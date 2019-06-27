# Button control for maze
# Author: Ariel Burman

BUTTONSVERSION = 1.2

import time

import traceback
import logging
logger=logging.getLogger('MazeButtons')

import adai2c as pwm
import gpiozero

buttons = {'B':[12,15,'blue'],
           'W':[13,12,'white'],
           'Y':[5,14,'yellow'],
           'G':[6,13,'green']
           }


class ledButton(object):
  def __init__(self,gpioN=0,ledN=0,color=''):
    logger.debug('Button connected to gpio %s with led %s is color %s id %s ',gpioN,ledN,color,id(self))
    self.button=gpiozero.Button(gpioN,pull_up=True,bounce_time=0.1,hold_time=1,hold_repeat=False)
    self.button.when_pressed = None
    self.ledN=ledN
    self.pwm = pwm.AdaI2C()
    self.color = color
    logger.debug(" gpiozero button %s id %d", self.color, id(self.button))

  def setWhenPressed(self,handler):
    self.button.when_pressed = handler

  def ledPwm(self,value):
    if value > 1.0:
        value = 1.0
    elif value < 0.0:
        value = 0.0
    self.pwm.set(self.ledN,int((1-value)*4095))

  def ledOn(self):
    self.pwm.set(self.ledN,0)

  def ledOff(self):
    self.pwm.set(self.ledN,4095)

  def isPressed(self):
    return self.button.is_pressed


class MazeButtons(object):
  def __init__(self,handler=None):
    self.button = {}
    self.handler = handler
    for key in buttons:
      self.button[key] = ledButton(gpioN=buttons[key][0],ledN=buttons[key][1],color=buttons[key][2])

    for key in self.button:
      self.button[key].setWhenPressed(self._buttonsHandler)

    logger.debug('MazeButtons id %s ',id(self))
    logger.debug('Buttons version {a}'.format(a=BUTTONSVERSION))

  def _buttonsHandler(self,buttonObj):
    try:
      logger.debug(buttonObj.pin)
      buttonPin = int(str(buttonObj.pin)[4:])
      for key,value in buttons.items():
          if buttonPin == value[0]:
              buttonName = key
      logger.debug('Button activated {a}'.format(a=buttonName))
      self.lastSensorActive = buttonName
      if self.handler is not None:
        self.handler(buttonName)
    except Exception as e:
      logger.error(traceback.format_exc())
      print('error handled in button module')

  def setLedOn(self,key):
    logger.debug('New Led %s on',self.button[key].color)
    self.button[key].ledOn()

  def setLedOff(self,key):
    logger.debug('New Led %s off',self.button[key].color)
    self.button[key].ledOff()

  def setLedPwm(self,key,val):
    logger.debug('New Led %s pwm %s',self.button[key].color,val)
    self.button[key].ledPwm(val)

  def isPressed(self,key):
    return self.button[key].isPressed()

if __name__ == '__main__':
  import sys,os
  if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

  dateformat = '%Y/%m/%d %H:%M:%S'
  formatter_str = '%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s'
  logfile = 'logs/buttons.log'

  logging.basicConfig(filename=logfile,filemode='w+',level=logging.DEBUG,
          format=formatter_str, datefmt=dateformat)

  logger.info('Buttons test')

  class Test(object):
    def __init__(self):
      self.lastactive = None
      logger.debug('Tests id %s ',id(self))
      logger.debug('property id %s',id(self.lastactive))
      logger.info('Using handler {a}'.format(a=self.anotherHandler))
      logger.debug('procces id {}'.format(os.getpid()))
      self.bt = None
      logger.debug('MazeButtons id %s ',id(self.bt))


    def anotherHandler(self,button):
      print('last {a}'.format(a=self.lastactive))
      print('now {a}'.format(a=button))
      self.lastactive=button
      self.bt.setLedOn(button)
      logger.debug('Tests id %s ',id(self))
      logger.debug('property id %s',id(self.lastactive))
      logger.debug('procces id {}'.format(os.getpid()))
      logger.info(button)

    def run(self):
      self.bt = MazeButtons(self.anotherHandler)
      while True:
        time.sleep(3)
        print('restarting')
        self.bt.setLedOff('B')
        self.bt.setLedOff('Y')
        self.bt.setLedOff('W')
        self.bt.setLedOff('G')


  test = Test()

  from multiprocessing import Process
  p = Process(target=test.run)
  p.start()

#  while True:
#      msg = ''
#      for i in bt.button:
#          msg = msg + str(i) + '=' + str(bt.isPressed(i)) + '|'
#      logger.info(msg)
#      print(msg)
#      time.sleep(2)
#      for i in range(20):
#        bt.setLedPwm('B',i/19)
#        time.sleep(.05)
#      for i in range(20):
#        bt.setLedPwm('B',1-i/19)
#        bt.setLedPwm('Y',i/19)
#        time.sleep(.05)
#      for i in range(20):
#        bt.setLedPwm('Y',1-i/19)
#        bt.setLedPwm('W',i/19)
#        time.sleep(.05)
#      for i in range(20):
#        bt.setLedPwm('W',1-i/19)
#        bt.setLedPwm('G',i/19)
#        time.sleep(.05)
#      for i in range(20):
#        bt.setLedPwm('G',1-i/19)
#        time.sleep(.05)
#      bt.setLedOn('B')
#      bt.setLedOn('Y')
#      bt.setLedOn('W')
#      bt.setLedOn('G')
#      time.sleep(.5)
#      bt.setLedOff('B')
#      bt.setLedOff('Y')
#      bt.setLedOff('W')
#      bt.setLedOff('G')
