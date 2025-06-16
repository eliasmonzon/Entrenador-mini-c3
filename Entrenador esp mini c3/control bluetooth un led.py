# main.py

import bluetooth
from machine import Pin
import time
from bluetooth_ble import BLEUART

# Configura el LED en GPIO2
led = Pin(2, Pin.OUT)

# Inicializa BLE
ble = bluetooth.BLE()
uart = BLEUART(ble)

# Función que se llama cuando se recibe un mensaje
def on_rx():
    data = uart.read().decode().strip().lower()
    print("Recibido:", data)

    if data == "on":
        led.value(1)
        uart.write("LED encendido\n")
    elif data == "off":
        led.value(0)
        uart.write("LED apagado\n")
    else:
        uart.write("Comando no reconocido\n")

# Asigna la función
uart.irq(handler=on_rx)

# Bucle principal
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass

uart.close()


