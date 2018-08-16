from time import sleep

import logging
logger=logging.getLogger(__name__)

class WaveObject(object):
  def __init__(self, audio_data, num_channels=2, bytes_per_sample=2,
                 sample_rate=44100):
    self.audio_data = audio_data
    self.num_channels = num_channels
    self.bytes_per_sample = bytes_per_sample
    self.sample_rate = sample_rate
    self.idn = id(self)

  def play(self):
    logger.debug('playing waveobject id {a}'.format(a=self.idn))
    return PlayObject(self.idn)

class PlayObject(object):
  def __init__(self, play_id):
    self.play_id = play_id

  def wait_done(self):
    while self.is_playing():
      sleep(0.05)

  def is_playing(self):
    logger.debug('someone ask if play {a} is done'.format(a=self.play_id))
    return False
