# Sounds for maze
# Author: Ariel Burman

SOUNDSVERSION = 1.1

import numpy as np
import simpleaudio as sa

import logging
logger=logging.getLogger(__name__)

# using 16 bit sounds
# pi audio is a one instance class with multiple types of sounds

class MazeSounds():
  def __init__(self):
    self.sound = {}
    self.play_obj = None
    logger.debug('Maze Sounds id %s ',id(self))
    logger.info('Sounds version {a}'.format(a=SOUNDSVERSION))

  def play(self,key):
    self.play_obj = self.sound[key].play()
    logger.info('play audio %s',key)

  def stop(self):
    if self.isPlaying():
      self.play_obj.stop()
      logger.info('stop current sound')
    
  def playBlocking(self,key):
    self.play_obj = self.sound[key].play()
    logger.info('play audio %s',key)
    self.play_obj.wait_done()

  def isPlaying(self):
    if self.play_obj is None:
        return False
    else:
        return self.play_obj.is_playing()

  def addTone(self,key,duration=1.0, freq=1000.0, volume=1.0, sample_rate = 44100):
    volume = volume
    logger.info('Sound %s : Tone freq = %s Hz, duration = %s s, sample_rate = %s, volume = %s',key,freq,duration,sample_rate,volume)
  
    # get timesteps for each sample, T is note duration in seconds
    T = duration
    t = np.linspace(0, T, int(T * sample_rate), False)
  
    # generate sine wave notes
    buff = np.sin(freq * t * 2 * np.pi)
    logger.debug(str(buff))
  
    # normalize to 16-bit range
    buff *= 32767 * volume / np.max(np.abs(buff)) 
    # convert to 16-bit data
    buff = buff.astype(np.int16)
    self.sound[key] = sa.WaveObject(buff,1,2,sample_rate)
    logger.debug(str(buff))

  def addBufferSound(self,key,buff, sample_rate = 44100):
    ''' 
       buff should be a numpy array of np.int16 
       with one or two dimensions (mono or stereo)
    '''
    logger.info('Custom sound channels %s',len(buff))
    # convert to 16-bit data
    buff = buff.astype(np.int16)
    if len(buff)==2:
      chan = 2
    else:
      chan = 1
    self.sound[key] = sa.WaveObject(buff,chan,2,sample_rate)
    logger.debug(str(buff))

  def addWhiteNoise(self,key,duration=5.0,volume=1.0, sample_rate = 44100):
    noise = np.random.normal(0,1,duration*sample_rate)
    noise *= 32767/3.5 * volume
    noise = noise.astype(np.int16)
    self.sound[key] = sa.WaveObject(buff,1,2,sample_rate)

if __name__=='__main__':
  import sys,os
  if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

  dateformat = '%Y/%m/%d %H:%M:%S'
  formatter_str = '%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s'
  logfile = 'logs/audio.log'

  logging.basicConfig(filename=logfile,filemode='w+',level=logging.DEBUG,
          format=formatter_str, datefmt=dateformat)

  logger.info('Sound Test')

  sample_rate = 44100
  audio = MazeSounds()
  audio.addTone(key=1,duration=3.0,freq=1000.0,volume=0.5,sample_rate=sample_rate)
  audio.addTone(key=2,duration=3.0,freq=8000.0,volume=1.0,sample_rate=sample_rate)
  
  import time
  t = np.linspace(0, 2.0, int(2.0 * sample_rate), False)
  buff = np.array([np.sin(1000 * t * 2 * np.pi),np.sin(4000 * t * 2 * np.pi)])
  logger.debug(str(buff))
  buff *= 32767 / np.max(np.abs(buff)) 
  logger.debug(str(buff))
  buff = buff.astype(np.int16)
  logger.debug(str(buff))
  audio.addBufferSound(3,buff,sample_rate)
  print(audio.isPlaying())
  audio.play(1)
  print(audio.isPlaying())
  time.sleep(2)
  audio.play_obj.wait_done()
  audio.playBlocking(2)
  time.sleep(2)
  print(audio.isPlaying())
#  audio.play(3)
#  print(audio.isPlaying())
#  audio.play_obj.wait_done()


  audio.addTone(key=4,duration=10.0,volumen=1.0,sample_rate=sample_rate)
  audio.play(4)
  time.sleep(5)
  audio.stop()
  
