import logging
import numpy as np
import simpleaudio as sa

logger=logging.getLogger(__name__)

# using 16 bit sounds
# pi audio is a one instance class with multiple types of sounds
class MazeAudio():
  def __init__(self):
    self.audios = {}
    self.play_obj = None

  def add(self,key,sound):
    self.audios[key] = sound

  def play(self,key):
    self.play_obj = self.audios[key].play()
    logger.info('play audio %s',key)
    
  def playBlocking(self,key):
    self.play_obj = self.audios[key].play()
    self.play_obj.wait_done()

  def tone(duration=1.0, freq=1000.0, volume=1.0, sample_rate = 44100):
    sound = MazeAudio.Sound(sample_rate,channels=1)
    volume = volume
    logger.info('Tone freq = %s Hz, duration = %s s, sample_rate = %s, volume = %s',freq,duration,sample_rate,volume)
  
    # get timesteps for each sample, T is note duration in seconds
    T = duration
    t = np.linspace(0, T, int(T * sample_rate), False)
  
    # generate sine wave notes
    buff = np.sin(freq * t * 2 * np.pi)
  
    # normalize to 16-bit range
    buff *= 32767 * volume / np.max(np.abs(buff)) 
    # convert to 16-bit data
    buff = buff.astype(np.int16)
    sound.buffer = buff
    sound.duration = duration
    logger.debug(str(sound.buffer))
    return sound

  class Sound():
    def __init__(self,sample_rate=0, channels=1):
      self.sample_rate=sample_rate
      self.channels=channels
      self.duration=0  #only for info
      self.buffer=None

    def play(self):
      play_obj = sa.play_buffer(self.buffer, self.channels, 2, self.sample_rate)
      return play_obj


if __name__=='__main__':
  import sys,os
  if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

  dateformat = '%Y/%m/%d %H:%M:%S'
  formatter_str = '%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s'
  logfile = 'logs/audio.log'

  logging.basicConfig(filename=logfile,filemode='w+',level=logging.DEBUG,
          format=formatter_str, datefmt=dateformat)

  logger.info('Audio Test')

  sample_rate = 44100
  audio = MazeAudio()
  audio.add(1,MazeAudio.tone(duration=1.0,freq=1000.0,volume=1.0,sample_rate=sample_rate))
  audio.add(2,MazeAudio.tone(duration=1.0,freq=8000.0,volume=1.0,sample_rate=sample_rate))
  audio.play(1)
  audio.play_obj.wait_done()
  audio.playBlocking(2)


