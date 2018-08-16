# Button control for maze
# Author: Ariel Burman

BUTTONSVERSION = 1.0

import time

import logging
logger=logging.getLogger(__name__)

import adai2c as pwm
import gpiozero

buttons = {'B':[12,15,'blue'],
           'W':[13,12,'white'],
           'Y':[5,14,'yellow'],
           'G':[6,13,'green']
           }


class ledButton(object):
  def __init__(self,gpioN=0,ledN=0,color=''):
    logger.info('Button connected to gpio %s with led %s is color %s id %s ',gpioN,ledN,color,id(self))
    self.button=gpiozero.Button(gpioN,pull_up=True,bounce_time=0.2,hold_time=0.4,hold_repeat=False)
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
    self.pwm.set(self.ledN,int(value*4095))

  def ledOn(self):
    self.pwm.set(self.ledN,4095)

  def ledOff(self):
    self.pwm.set(self.ledN,0)

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
    logger.info('Buttons version {a}'.format(a=BUTTONSVERSION))

  def _buttonsHandler(self):
    try:
      if self.handler is not None:
        self.handler(self)
      else:
        for key in self.button:
          if self.isPressed(key):
            logger.debug('key pressed {a}'.format(a=key))
    except Exception as e:
      logger.debug(e)
      print('error handled')


  def setLedOn(self,key):
    logger.info('New Led %s on',self.button[key].color)
    self.button[key].ledOn()

  def setLedOff(self,key):
    logger.info('New Led %s off',self.button[key].color)
    self.button[key].ledOff()

  def setLedPwm(self,key,val):
    logger.info('New Led %s pwm %s',self.button[key].color,val)
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
  bt = MazeButtons()

  while True:
      msg = ''
      for i in bt.button:
          msg = msg + str(i) + '=' + str(bt.isPressed(i)) + '|'
      logger.info(msg)
      time.sleep(2)
