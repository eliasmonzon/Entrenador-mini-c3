from machine import Pin
from IR_remote import ir_receptor
import utime

Receptor_pin = ir_receptor(4)  # Receptor IR en GPIO 4
Led1 = Pin(0, Pin.OUT)         # LED controlado por el botón (GPIO 0)
Led_parpadeo = Pin(8, Pin.OUT) # LED que parpadea al asignar nuevo botón

codigo_actual = None
led_encendido = False

codigo_repetido = "0xffffffff"  # Código repetido que debemos ignorar

def parpadear_led(pin_led, veces=3, tiempo_ms=200):
    for _ in range(veces):
        pin_led.value(0)
        utime.sleep_ms(tiempo_ms)
        pin_led.value(1)
        utime.sleep_ms(tiempo_ms)

print("Pulsa cualquier botón del control para asignarlo al LED.")

while True:
    codigo = Receptor_pin.ir_read()
    if codigo and codigo != codigo_repetido:
        print("Código recibido:", codigo)

        if codigo_actual is None:
            codigo_actual = codigo
            print("Código asignado:", codigo_actual)
            parpadear_led(Led_parpadeo)  # Parpadea LED al asignar por primera vez
        elif codigo == codigo_actual:
            led_encendido = not led_encendido
            Led1.value(1 if led_encendido else 0)
            print("LED", "encendido" if led_encendido else "apagado")
        else:
            codigo_actual = codigo
            print("Nuevo código asignado:", codigo_actual)
            parpadear_led(Led_parpadeo)  # Parpadea LED al cambiar de botón

    utime.sleep_ms(100)

