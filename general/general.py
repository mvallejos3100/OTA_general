from machine import Pin
import time

rele = Pin(16, Pin.OUT)

while True:
  rele.on()
  time.sleep(.5)
  rele.off()
  time.sleep(.5)
  print('Versión actualizada por medio de OTA\n') 
