

from multiprocessing import Process,Value,Lock
from ctypes import c_bool,c_int
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
        self._is_pressed= Value(c_bool,False)
        self.p = Process(target=self.run)
        self.p.daemon = True
        self.t = TrueButton()
        
    def __getattr__(self, attr):
      if attr == 'is_pressed':
        return self._is_pressed.value

    @property
    def when_pressed(self):
      return self.__when_pressed

    @when_pressed.setter
    def when_pressed(self,handler):
      self.__when_pressed = handler
      if handler is not None:
        self.p.start()

    def run(self):
      try:
        while True:
          a = self.t.buttonPress(self.pin)
          if self._is_pressed.value != a:
            logger.debug('pin changed {a}'.format(a=self.pin))
            self._is_pressed.value = self.t.buttonPress(self.pin)
            if self.when_pressed is not None:
              logger.debug('calling handler {a} with id {b} name {c}'.format(a=self.when_pressed,b=id(self.when_pressed),c=str(self.when_pressed)))
              self.when_pressed(self.pinname)
          time.sleep(.05)
      except Exception as e:
          print('hubo excepcion')
          logger.error('Exception in gpiozero module')
          logger.error(e)
      finally:
          print('se termino')

    # inner class only for the name
    class ButtonName(object):
        def __init__(self,name):
            self.pin = name


import csv

class TrueButton(object):
  class __impl:
    def __init__(self):
      self.file = filename
      self.p = Process(target=self.run)
      self.button = {12:Value(c_bool,False), #button
                     13:Value(c_bool,False), #button
                     5:Value(c_bool,False),  #button
                     6:Value(c_bool,False),  #button
                     18:Value(c_bool,False), #sensor
                     23:Value(c_bool,False), #sensor
                     4:Value(c_bool,False),  #sensor
                     24:Value(c_bool,False), #sensor
                     17:Value(c_bool,False), #sensor
                     27:Value(c_bool,False), #sensor
                     22:Value(c_bool,False)  #sensor
                     }
      self.p.daemon = True
      self.p.start()
      
    def buttonPress(self,pin):
      return self.button[pin].value

    def run(self):
      try:
        while True:
          line = []
          with open(self.file) as f:
            fr = csv.reader(f)
            for row in fr:
              line.append(row)
          for l in line:
            if l[1]=='F':
              self.button[int(l[0])].value = False
            else:
              self.button[int(l[0])].value = True
          time.sleep(.25)
      except Exception as e:
          print('Exception in gpiozero module Truebutton')
          logger.error('Exception in gpiozero module Truebutton')
          logger.error(e)
      finally:
          print('se termino el principal')

  __instance = None

  def __init__(self):
      """ Create singleton instance """
      # Check whether we already have an instance
      if TrueButton.__instance is None:
          # Create and remember instance
          TrueButton.__instance = TrueButton.__impl()

      # Store instance reference as the only member in the handle
      #self.__dict__['_Singleton__instance'] = Singleton.__instance

  def __getattr__(self, attr):
      """ Delegate access to implementation """
      return getattr(self.__instance, attr)

  def __setattr__(self, attr, value):
      """ Delegate access to implementation """
      return setattr(self.__instance, attr, value)

