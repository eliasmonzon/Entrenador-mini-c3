from machine import Pin, ADC
import time

# Configuración del LDR en GPIO4
ldr = ADC(Pin(4))
ldr.atten(ADC.ATTN_11DB)    # Rango 0 - 3.3V
ldr.width(ADC.WIDTH_12BIT) # Resolución de 12 bits (0-4095)

# LED en GPIO0
led = Pin(0, Pin.OUT)

# Umbral de luz (ajustalo haciendo pruebas)
umbral = 1000   

while True:
    valor = ldr.read()
    print("LDR:", valor)

    if valor > umbral:   # Valor alto = sombra
        led.value(0)     # LED apagado
        print("LED APAGADO")
    else:
        led.value(1)    # LED encendido 
        print("LED ENCENDIDO ")

    time.sleep(0.2)
