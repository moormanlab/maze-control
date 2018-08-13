# Button control for maze
# Author: Ariel Burman

import time
import logging

logger=logging.getLogger(__name__)

import adai2c as pwm
# Uncomment to enable debug output.
#logging.basicConfig(level=logging.DEBUG)


buttons = {'B':[17,15,'blue'],
           'W':[17,14,'white'],
           'Y':[17,13,'yellow'],
           'G':[17,12,'green']
           }


import gpiozero

#from multiprocessing import Process, Queue, Lock, Value

class Button(object):
  def __init__(self,gpioN=0,ledN=0,color=''):
    logger.info('Button connected to gpio %s with led %s is color %s id %s ',gpioN,ledN,color,id(self))
    self.button=gpiozero.Button(gpioN,pull_up=True,bounce_time=0.2,hold_time=0.4,hold_repeat=False)
    self.button.when_pressed = None
    self.ledN=ledN
    self.pwm = pwm.AdaI2C()
    self.color = color
    print(" gpiozero button %s id %d" , self.color, id(self.button))

  def ledPwm(self,value):
    self.pwm.set(self.ledN,value)

  def ledOn(self):
    self.pwm.set(self.ledN,1024)

  def ledOff(self):
    self.pwm.set(self.ledN,0)

  def isPressed(self):
    return self.button.is_pressed


class MazeButtons(object):
  def __init__(self):
    # Initialise the PCA9685 using the default address (0x40).
    self.button = {}
    for key in buttons:
      self.button[key] = Button(gpioN=buttons[key][0],ledN=buttons[key][1],color=buttons[key][2])
      print(" button %s id %d" , key, id(self.button[key]))
      
    logger.info('MazeButtons id %s ',id(self))

  def setLedOn(self,key):
    self.button[key].ledOn()

  def setLedOff(self,key):
    self.button[key].ledOff()

  def setLedPwm(self,key,val):
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

  print(bt.button['B'].isPressed())
  gpiozero.Button.change(bt.button['B'].button)
  print(bt.button['B'].isPressed())
