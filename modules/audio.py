import logging
import numpy as np
import simpleaudio as sa

logger=logging.getLogger(__name__)

# using 16 bit sounds
# pi audio is a one instance class with multiple types of sounds


class Sound():
  def __init__(self,sample_rate=0, channels=1, buff=None):
    self.sample_rate=sample_rate
    self.channels=channels
    self.buff=None
    #self.duration=0  #only for info should be len(buff)/samplerate

  def play(self):
    play_obj = sa.play_buffer(self.buff, self.channels, 2, self.sample_rate)
    return play_obj

class MazeSounds():
  def __init__(self):
    self.sound = {}
    self.play_obj = None

  def play(self,key):
    self.play_obj = self.audio[key].play()
    logger.info('play audio %s',key)
    
  def playBlocking(self,key):
    self.play_obj = self.audio[key].play()
    logger.info('play audio %s',key)
    self.play_obj.wait_done()

  def addTone(key,duration=1.0, freq=1000.0, volume=1.0, sample_rate = 44100):
    volume = volume
    logger.info('Sound %s : Tone freq = %s Hz, duration = %s s, sample_rate = %s, volume = %s',key,freq,duration,sample_rate,volume)
  
    # get timesteps for each sample, T is note duration in seconds
    T = duration
    t = np.linspace(0, T, int(T * sample_rate), False)
  
    # generate sine wave notes
    buff = np.sin(freq * t * 2 * np.pi)
  
    # normalize to 16-bit range
    buff *= 32767 * volume / np.max(np.abs(buff)) 
    # convert to 16-bit data
    buff = buff.astype(np.int16)
    self.sound[key] = Sound(sample_rate,channels=1,buff=buff)
    logger.debug(str(self.sound[key].buffer))

  def addBufferSound(buff=buff, sample_rate = 44100):
    ''' 
       buff should be a numpy array of np.int16 
       with one or two dimensions (mono or stereo)
    '''
    logger.info('Tone freq = %s Hz, duration = %s s, sample_rate = %s, volume = %s',freq,duration,sample_rate,volume)
    # convert to 16-bit data
    buff = buff.astype(np.int16)
    if len(buff)==2:
      chan = 2
    else:
      chan = 1
    self.sound[key] = Sound(sample_rate = sample_rate,channels=chan,buff=buff)
    logger.debug(str(self.sound[key].buff))


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
  audio.addTone(1,duration=1.0,freq=1000.0,volume=1.0,sample_rate=sample_rate)
  audio.addTone(2,duration=1.0,freq=8000.0,volume=1.0,sample_rate=sample_rate)
  
  buff = np.array([np.sin(1000 * 44100 * 2 * np.pi),np.sin(4000 * 44100 * 2 * np.pi)])
  buff *= 32767 / np.max(np.abs(buff)) 
  buff = buff.astype(np.int16)
  audio.addBufferSound(3,buff=buff,sample_rate=sample_rate)
  audio.play(1)
  audio.play_obj.wait_done()
  audio.playBlocking(2)
  audio.play(3)


