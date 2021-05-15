from machine import Pin
import time

rele = Pin(16, Pin.OUT)

wile True:
  rele.on()
  time.sleep(1)
  rele.off()
  time.sleep(1)
  print('Version 2 installed using USB') 
