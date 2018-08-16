from distutils.core import setup

setup(name='mazeHardwareEmulation',
      version='0.1',
      packages=['Adafruit_GPIO','Adafruit_PCA9685','gpiozero','simpleaudio'],

      # metadata for upload to PyPI
      author="Ariel Burman",
      author_email="arielburman@gmail.com",
      description="Hardware emulation for maze application in raspberry pi",
      license="GPL",
      keywords="maze",
      )
