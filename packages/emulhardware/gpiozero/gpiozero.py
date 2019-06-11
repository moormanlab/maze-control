

import threading
import time

import logging
logger=logging.getLogger(__name__)

filename = './buttons.txt'

class Button(object):
    def __init__(self, pin=None, pull_up=True, bounce_time=None,hold_time=1, 
            hold_repeat=False):
        self.pin =pin
        self.pinname = self.ButtonName('GPIO'+str(pin))
        self.hold_time = hold_time
        self.hold_repeat = hold_repeat
        self.when_pressed= None
        logger.debug('function to call {a} with id {b}'.format(a=self.when_pressed,b=id(self.when_pressed)))
        self._is_pressed= False
        self.th = threading.Thread(target=self.run, daemon=True)
        self.t = TrueButton()
        
    def __getattr__(self, attr):
      if attr == 'is_pressed':
        return self._is_pressed

    @property
    def when_pressed(self):
      return self.__when_pressed

    @when_pressed.setter
    def when_pressed(self,handler):
      self.__when_pressed = handler
      if handler is not None:
        self.th.start()

    def run(self):
        while True:
          a = self.t.buttonPress(self.pin)
          if self._is_pressed != a:
            logger.debug('pin changed {a}'.format(a=self.pin))
            self._is_pressed = self.t.buttonPress(self.pin)
            if self.when_pressed is not None:
              logger.debug('calling handler {a} with id {b} name {c}'.format(a=self.when_pressed,b=id(self.when_pressed),c=str(self.when_pressed)))
              self.when_pressed(self.pinname)
          time.sleep(.05)

    # inner class only for the name
    class ButtonName(object):
        def __init__(self,name):
            self.pin = name


import csv

class TrueButton(object):
  class __impl:
    def __init__(self):
      self.file = filename
      self.tr = threading.Thread(target=self.run,daemon=True)
      self.button = {12:False, #button
                     13:False, #button
                     5: False,  #button
                     6: False,  #button
                     18:False, #sensor
                     23:False, #sensor
                     4: False,  #sensor
                     24:False, #sensor
                     17:False, #sensor
                     27:False, #sensor
                     22:False  #sensor
                     }
      logger.debug('starting truebutton daemon')
      self.tr.start()
      
    def buttonPress(self,pin):
      return self.button[pin]

    def run(self):
      while True:
        try:
          line = []
          with open(self.file,'r') as f:
            fr = csv.reader(f)
            for row in fr:
              line.append(row)
          for l in line:
            if l[1]=='F':
              self.button[int(l[0])] = False
            else:
              self.button[int(l[0])] = True
        except Exception as e:
          logger.error('Exception in gpiozero module Truebutton')
          logger.error(e)
        time.sleep(.25)

  __instance = None
  __num = 0

  def __init__(self):
      """ Create singleton instance """
      # Check whether we already have an instance
      if TrueButton.__instance is None:
          # Create and remember instance
          TrueButton.__instance = TrueButton.__impl()
      # Store instance reference as the only member in the handle
      #self.__dict__['_Singleton__instance'] = Singleton.__instance
      TrueButton.__num +=1
      logger.debug('Trubutton num = {a}'.format(a=TrueButton.__num))

  def __getattr__(self, attr):
      """ Delegate access to implementation """
      return getattr(self.__instance, attr)

  def __setattr__(self, attr, value):
      """ Delegate access to implementation """
      return setattr(self.__instance, attr, value)

  def __del__(self):
      TrueButton.__num -=1
      logger.debug("deleting trubutton. {a} remaining".format(a=TrueButton.__num))


class DigitalOutputDevice(object):
    def __init__(self, pin=None, initial_value=False):
        self.pin = pin
        self.value = initial_value

    def on(self):
        self.value = True

    def off(self):
        self.value = False
