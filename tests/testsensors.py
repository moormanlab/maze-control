import logging
import gpiozero
from signal import pause

logger=logging.getLogger(__name__)

def giveWarning(labl):
  print ("rat is at sensor: ",labl)


sensors={'A': gpiozero.Button(4), #southeast    yellow  
         'B': gpiozero.Button(17), # east       brown
         'C': gpiozero.Button(18), #northeast   orange
         'D': gpiozero.Button(27), #middle      white
         'E': gpiozero.Button(22), #west        yellow
         'F': gpiozero.Button(23), #nortwest    brown
         'G': gpiozero.Button(24) } #southwest  white


for sensK,sensV in sensors.items():
    sensors[sensK].when_pressed = lambda: giveWarning(sensK)
    print(sensK)

#sensors['A'].when_pressed = lambda: giveWarning('A')
#sensors['B'].when_pressed = lambda: giveWarning('B')
#sensors['C'].when_pressed = lambda: giveWarning('C')
#sensors['D'].when_pressed = lambda: giveWarning('D')
#sensors['E'].when_pressed = lambda: giveWarning('E')
#sensors['F'].when_pressed = lambda: giveWarning('F')
#sensors['G'].when_pressed = lambda: giveWarning('G')


if __name__ == '__main__':
  import sys,os
  if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

  dateformat = '%Y/%m/%d %H:%M:%S'
  formatter_str = '%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s'
  logfile = 'logs/sensors.log'

  logging.basicConfig(filename=logfile,filemode='w+',level=logging.DEBUG,
          format=formatter_str, datefmt=dateformat)

  logger.info('Sensors Test')
  pause()

