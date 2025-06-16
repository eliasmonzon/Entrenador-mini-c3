from machine import Pin
import time

# LED en GPIO 1
led1 = Pin(1, Pin.OUT)
led2 = Pin(2, Pin.OUT)
led3 = Pin(3, Pin.OUT)
led4 = Pin(4, Pin.OUT)
# Botón en GPIO 21, con resistencia pull-up interna
boton1 = Pin(21, Pin.IN, Pin.PULL_UP)
boton2 = Pin(20, Pin.IN, Pin.PULL_UP)
boton3 = Pin(10, Pin.IN, Pin.PULL_UP)
boton4 = Pin(9, Pin.IN, Pin.PULL_UP)
while True:
    if not boton1.value():  # Si el botón está presionado (valor bajo)
        led1.on()
    else:
        led1.off()
    if not boton2.value():  # Si el botón está presionado (valor bajo)
        led2.on()
    else:
        led2.off()
    if not boton3.value():  # Si el botón está presionado (valor bajo)
        led3.on()
    else:
        led3.off()
    if not boton4.value():  # Si el botón está presionado (valor bajo)
        led4.on()
    else:
        led4.off()    
    time.sleep(0.05)  # Pequeña pausa para estabilidad
