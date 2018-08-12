import time
import logging

logger=logging.getLogger(__name__)

# Import the PCA9685 module.
import Adafruit_PCA9685
from multiprocessing import Process, Lock

class AdaI2C(object):
  class __impl:
    def __init__(self):
      # Initialise the PCA9685 using the default address (0x40).
      self.pwm = Adafruit_PCA9685.PCA9685()
      # Set frequency to 60hz, good for servos.
      self.pwm.set_pwm_freq(60)
      self.lock = Lock()
      logger.info("initializing adai2c with id %s",id(self))
      
    def set(self,number,pwm):
      logger.debug("setting pwm %s, with value %s, id %s",number,pwm,id(self))
      #bloquea proceso
      self.lock.acquire()
      try:
         self.pwm.set_pwm(number,0,pwm)
      finally:
          # liberar proceso
          self.lock.release()
          #pass

  __instance = None

  def __init__(self):
      """ Create singleton instance """
      # Check whether we already have an instance
      if AdaI2C.__instance is None:
          # Create and remember instance
          AdaI2C.__instance = AdaI2C.__impl()

      # Store instance reference as the only member in the handle
      #self.__dict__['_Singleton__instance'] = Singleton.__instance

  def __getattr__(self, attr):
      """ Delegate access to implementation """
      return getattr(self.__instance, attr)

  def __setattr__(self, attr, value):
      """ Delegate access to implementation """
      return setattr(self.__instance, attr, value)
    

if __name__ == '__main__':
  import sys,os
  if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

  dateformat = '%Y/%m/%d %H:%M:%S'
  formatter_str = '%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s'
  logfile = 'logs/adai2C.log'

  logging.basicConfig(filename=logfile,filemode='w+',level=logging.DEBUG,
          format=formatter_str, datefmt=dateformat)

  logger.info('Ada test')

  motors = AdaI2C()
  motors2 = AdaI2C()
  data = [[x,x*10] for x in range(10)]
  procs = []
  for i in data:
      p = Process(target=motors.set,args=(i[0],i[1],))
      procs.append(p)

  for p in procs:
      p.start()

  for p in procs:
      p.join()

