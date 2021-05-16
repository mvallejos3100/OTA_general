from machine import Pin
import time

rele = Pin(16, Pin.OUT)

while True:
  rele.on()
  time.sleep(1)
  rele.off()
  time.sleep(1)
  print('Versión actualizada por medio de OTA\n') 
