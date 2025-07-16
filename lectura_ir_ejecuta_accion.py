from machine import Pin
from IR_remote import ir_receptor
import utime

Receptor_pin = ir_receptor(4)  # Receptor IR en GPIO 4
Led1 = Pin(0, Pin.OUT)         # LED en GPIO 0

codigo_actual = None
led_encendido = False

# Algunos controles mandan esto al mantener presionado un botón
codigo_repetido = "0xffffffff"

print("Pulsa cualquier botón del control para asignarlo al LED.")

while True:
    codigo = Receptor_pin.ir_read()
    if codigo and codigo != codigo_repetido:
        print("Código recibido:", codigo)

        if codigo_actual is None:
            codigo_actual = codigo
            print("Código asignado:", codigo_actual)
        elif codigo == codigo_actual:
            # Encender o apagar el LED si es el código actual
            led_encendido = not led_encendido
            Led1.value(1 if led_encendido else 0)
            print("LED", "encendido" if led_encendido else "apagado")
        else:
            # Si se recibe un nuevo botón, se actualiza
            codigo_actual = codigo
            print("Nuevo código asignado:", codigo_actual)

    utime.sleep_ms(100)
