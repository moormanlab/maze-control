# Author: Ariel Burman
#
import logging

# Registers/etc:
ARDUINO_ADDRESS  = 0x60
MODE1            = 0x00
MODE2            = 0x01

SYS_KEEPALIVE    = 0x01
VALVE_OPEN       = 0x02
VALVE_CLOSE      = 0x03
VALVE_DROP       = 0x04
VALVE_MULTIDROP  = 0x05
VALVE_SET_MULTI  = 0x06
TEST1            = 0x5a  #90  // 0x5a 01011010
TEST2            = 0xa5  #165 // 0xa5 10100101



# Bits:


logger = logging.getLogger(__name__)


class Arduino(object):
    """PCA9685 PWM LED/servo controller."""

  def __init__(self, address=ARDUINO_ADDRESS, i2c=None, **kwargs):
    """Initialize the PCA9685."""
    # Setup I2C interface for the device.
    if i2c is None:
        import Adafruit_GPIO.I2C as I2C
        i2c = I2C
    self._device = i2c.get_i2c_device(address, **kwargs)
    logger.debug('Device initialized')

  def transmitt(self,data):
    self._device.write16()

if __name__ == '__main__':
  import sys,os
  if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

  dateformat = '%Y/%m/%d %H:%M:%S'
  formatter_str = '%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s'
  logfile = 'logs/arduino.log'

  logging.basicConfig(filename=logfile,filemode='w+',level=logging.DEBUG,
          format=formatter_str, datefmt=dateformat)

  logger.info('Arduino Test')

  arduino=Arduino()
  data = VALVE_OPEN<<8 + ord('L')
  arduino.transmitt(data)
  time.sleep(1)
  data = VALVE_CLOSE<<8 + ord('L')
  arduino.transmitt(data)
  


