import logging
import numpy as np
import simpleaudio as sa

logger=logging.getLogger(__name__)

def tone(duration=1.0, freq=1000.0, volume=1.0, sample_rate = 44100) :
  volume = volume
  logger.info('Tone freq = %s Hz, duration = %s s, sample_rate = %s, volume = %s',freq,duration,sample_rate,volume)

  # get timesteps for each sample, T is note duration in seconds
  T = duration
  t = np.linspace(0, T, T * sample_rate, False)

  # generate sine wave notes
  sound = np.sin(freq * t * 2 * np.pi)

  # normalize to 16-bit range
  sound *= 32767 * volume / np.max(np.abs(sound)) 
  # convert to 16-bit data
  sound = sound.astype(np.int16)

  logger.debug(str(sound))
  return sound



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
  s1 = tone(duration=1.0,freq=1000.0,volume=1.0)
  play_obj = sa.play_buffer(s1, 1, 2, sample_rate)
  play_obj.wait_done()

  s2 = tone(duration=1.0,freq=8000.0,volume=1.0)
  play_obj = sa.play_buffer(s2, 1, 2, sample_rate)
  play_obj.wait_done()

