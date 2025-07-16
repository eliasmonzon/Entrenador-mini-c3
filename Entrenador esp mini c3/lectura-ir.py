from machine import Pin
from IR_remote import ir_receptor
import utime

# Usar tu clase con el pin donde conectaste el receptor
Receptor_pin = ir_receptor(4)

print("Esperando señales del control remoto...")

while True:
    codigo = Receptor_pin.ir_read()
    if codigo:
        print("Código recibido:", codigo)
    utime.sleep_ms(100)
