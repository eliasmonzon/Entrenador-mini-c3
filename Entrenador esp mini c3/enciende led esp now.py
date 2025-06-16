
import network
import espnow
from machine import Pin

# Configuración del LED
led = Pin(2, Pin.OUT)
estado_led = False  # Estado actual del LED (apagado al inicio)

# Activar WiFi en modo estación
sta = network.WLAN(network.STA_IF)
sta.active(True)

# Inicializar ESP-NOW
esp = espnow.ESPNow()
esp.active(True)

print("Esperando mensajes...")

while True:
    host, msg = esp.recv()
    if msg:
        print("Recibido:", msg)
        comando = msg.decode('utf-8').strip().lower()
        if comando == 'on':
            estado_led = not estado_led  # Cambia el estado
            led.value(estado_led)        # Actualiza el LED

