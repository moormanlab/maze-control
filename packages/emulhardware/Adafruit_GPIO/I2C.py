

import logging
logger = logging.getLogger('Adafruit_I2C_emul')


def get_i2c_device(address, busnum=None, i2c_interface=None, **kwargs):
  logger.debug('Initializing i2c in address {a}'.format(a=address))
  return Device(address)

class Device(object):
  def __init__(self, address):
    self._address = address

  def write8(self, register, value):
    value = value & 0xFF
    logger.debug("Wrote 0x%02X to register 0x%02X", value, register)

  def writeRaw8(self, value):
    value = value & 0xFF
    logger.debug("Wrote 0x%02X, value")

