
from machine import Pin, I2C
import network
import espnow
import ssd1306

# Configuración del OLED
WIDTH = 128
HEIGHT = 64
sda = Pin(8)
scl = Pin(9)
i2c = I2C(sda=sda, scl=scl, freq=400000)
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

oled.fill(0)
oled.text("Esperando msg...", 0, 0)
oled.show()

# Activar WiFi en modo estación
sta = network.WLAN(network.STA_IF)
sta.active(True)

# Inicializar ESP-NOW
esp = espnow.ESPNow()
esp.active(True)

while True:
    host, msg = esp.recv()
    if msg:
        mensaje = msg.decode()
        print("Recibido:", mensaje)
        oled.fill(0)
        oled.text("Recibido del esp", 0,0)
        oled.text("wroom:", 0, 20)
        oled.text(mensaje, 0, 40)
        oled.show()

