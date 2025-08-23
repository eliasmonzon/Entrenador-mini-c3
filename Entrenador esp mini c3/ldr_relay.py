from machine import Pin, ADC
import time

# Relé en GPIO0
rele = Pin(0, Pin.OUT)

# LDR en GPIO1 (ADC)
ldr = ADC(Pin(1))
ldr.atten(ADC.ATTN_11DB)  # Permite medir hasta ~3.3V
ldr.width(ADC.WIDTH_12BIT)  # Resolución de 12 bits (0-4095)

# Umbral para oscuridad (ajústalo en pruebas)
UMBRAL_OSCURO = 1700  # Si el valor supera esto, consideramos oscuro

while True:
    valor = ldr.read()
    print("LDR:", valor)

    if valor > UMBRAL_OSCURO:
        rele.value(0)  # Apaga relé con luz
    else:
        rele.value(1) # Activa relé en oscuridad   

    time.sleep(0.5)
