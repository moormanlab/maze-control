import gpiozero
from signal import pause

def giveWarning1():
  print ("paso la rata 1")

def giveWarning2():
  print ("paso la rata 2")

def giveWarning3():
  print ("paso la rata 3")

def giveWarning4():
  print ("paso la rata 4")

def giveWarning5():
  print ("paso la rata 5")

def giveWarning6():
  print ("paso la rata 6")

def giveWarning7():
  print ("paso la rata 7")







sensor1 = gpiozero.Button(4)
sensor2 = gpiozero.Button(17)
sensor3 = gpiozero.Button(18)
sensor4 = gpiozero.Button(27)
sensor5 = gpiozero.Button(22)
sensor6 = gpiozero.Button(23)
sensor7 = gpiozero.Button(24)

sensor1.when_pressed = giveWarning1
sensor2.when_pressed = giveWarning2
sensor3.when_pressed = giveWarning3
sensor4.when_pressed = giveWarning4
sensor5.when_pressed = giveWarning5
sensor6.when_pressed = giveWarning6
sensor7.when_pressed = giveWarning7

pause()

