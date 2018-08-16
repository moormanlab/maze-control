import time
import logging

logger=logging.getLogger(__name__)

class PCA9685():
  def __init__(self):
    self.freq = 0

  def set_pwm_freq(self,val):
    self.freq = val

  def set_pwm(self,number,low,pwm):
    logger.debug('ADAFRUIT %s %s %s',number,low,pwm)  # solo para que parezca que no es inmediato
    #print('pwm gate {gateN} value {pwmValue}'.format(gateN=number,pwmValue=pwm) )
    pass

