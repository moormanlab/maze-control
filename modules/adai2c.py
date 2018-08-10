import time
import logging

logger=logging.getLogger(__name__)

# Import the PCA9685 module.
import Adafruit_PCA9685
from multiprocessing import Process, Lock

class AdaI2C(object):
  def __init__(self):
    # Initialise the PCA9685 using the default address (0x40).
    self.pwm = Adafruit_PCA9685.PCA9685()
    # Set frequency to 60hz, good for servos.
    self.pwm.set_pwm_freq(60)
    self.lock = Lock()
    
  def set(self,number,pwm):
    #bloquea proceso
    self.lock.acquire()
    try:
       self.pwm.set_pwm(number,0,pwm)
    finally:
        # liberar proceso
        self.lock.release()
        #pass

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
  data = [[x,x*10] for x in range(10)]
  procs = []
  for i in data:
      p = Process(target=motors.set,args=(i[0],i[1],))
      procs.append(p)

  for p in procs:
      p.start()

  for p in procs:
      p.join()

