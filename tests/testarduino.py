# Author: Ariel Burman
#
import logging

# Registers/etc:
ARDUINO_ADDRESS    = 0x60
MODE1              = 0x00
MODE2              = 0x01

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

if '__name__' == '__main__':
  import sys,os
  if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

  dateformat = '%Y/%m/%d %H:%M:%S'
  formatter_str = '%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s'
  logfile = 'logs/arduino.log'

  logging.basicConfig(filename=logfile,filemode='w+',level=logging.DEBUG,
          format=formatter_str, datefmt=dateformat)

  logger.info('Arduino Test')
