import network
import espnow
from machine import Pin
import time

# Configuración del botón
boton = Pin(32, Pin.IN, Pin.PULL_DOWN)  # Asegúrate que tu botón está en este pin

# Activar WiFi en modo estación
sta = network.WLAN(network.STA_IF)
sta.active(True)

# Inicializar ESP-NOW
esp = espnow.ESPNow()
esp.active(True)

# Dirección MAC del receptor (cámbiala por la real del receptor)
peer_mac = b'\x18\x8b\x0e\x1b\xbe\x8c' # <- reemplaza por la MAC del receptor
esp.add_peer(peer_mac)

estado_anterior = 0

while True:
    estado_actual = boton.value()
    if estado_actual == 1 and estado_anterior == 0:
        esp.send(peer_mac, b'ON')
        print("Enviado: ON")
        time.sleep(0.3)
    


