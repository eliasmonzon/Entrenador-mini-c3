import time
from machine import Pin, I2C, ADC
import ssd1306
from ojos_oled import ojos  # Importar la biblioteca de ojos

WIDTH  = 128         # oled display width
HEIGHT = 64          # oled display height

sda = Pin(8)   # Data pin
scl = Pin(9)   # Clock pin
i2c = I2C(sda=sda, scl=scl, freq=400000)  # ✅ Correcto para ESP32-C3

oled = ssd1306.SSD1306_I2C(128, 64, i2c)  # Initialise ssd1306 display



# Crear instancia de la clase Ojos
Cara = ojos(oled)

# Lista de índices de ojos que quieres mostrar
indices_deseados = [ 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

# Mostrar diferentes pares de ojos en un bucle
while True:
    for index in indices_deseados:
        Cara.mostrar_ojos(index)  # Mostrar el par de ojos correspondiente
        time.sleep_ms(100)  # Esperar 1 segundo antes de mostrar el siguiente
