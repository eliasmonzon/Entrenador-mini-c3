import network
import espnow
import time

# Activar WiFi en modo estación
sta = network.WLAN(network.STA_IF)
sta.active(True)

# Inicializar ESP-NOW
esp = espnow.ESPNow()
esp.active(True)

# Dirección MAC del receptor (ajusta esto con la dirección real del receptor)
peer_mac = b'\x18\x8b\x0e\x1b\xbe\x8c'  # <- remplaza por la MAC real
esp.add_peer(peer_mac)

while True:
    mensaje = "Hola"
    esp.send(peer_mac, mensaje)
    print("Enviado:", mensaje)
    time.sleep(2)


