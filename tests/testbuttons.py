

import time
import sys,os
import logging
sys.path.append('./../')
from modules.buttons import MazeButtons
if not os.path.exists('./logs/'):
  os.makedirs('./logs/')

dateformat = '%Y/%m/%d %H:%M:%S'
formatter_str = '%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s'
logfile = 'logs/testbuttons.log'

logging.basicConfig(filename=logfile,filemode='w+',level=logging.DEBUG,
        format=formatter_str, datefmt=dateformat)

logger=logging.getLogger(__name__)
logger.info('Buttons test')
bt = MazeButtons()

for key in bt.button:
  bt.button[key].ledOff()

while True:
  if bt.isPressed('B'):
     bt.setLedOn('B')
  else:
     bt.setLedOff('B')

  if bt.isPressed('Y'):
     bt.setLedOn('Y')
  else:
     bt.setLedOff('Y')

  if bt.isPressed('W'):
     bt.setLedOn('W')
  else:
     bt.setLedOff('W')

  if bt.isPressed('G'):
     bt.setLedOn('G')
  else:
     bt.setLedOff('G')

  time.sleep(0.1)
