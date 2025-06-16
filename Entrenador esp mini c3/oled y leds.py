from machine import Pin, SoftI2C
import ssd1306
import time

# Configuración del OLED
sda = Pin(8)
scl = Pin(9)
i2c = SoftI2C(sda=sda, scl=scl, freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Configuración de los LEDs
led_azul = Pin(0, Pin.OUT)
led_verde = Pin(1, Pin.OUT)
led_amarillo = Pin(2, Pin.OUT)
led_rojo = Pin(3, Pin.OUT)

# Diccionario con los LEDs y sus nombres
leds = [
    (led_azul, "Azul"),
    (led_verde, "Verde"),
    (led_amarillo, "Amarillo"),
    (led_rojo, "Rojo")
]

# Función para mostrar texto en OLED
def mostrar_mensaje(texto):
    oled.fill(0)
    oled.text("Entrenador esp", 0, 0)
    oled.text("LED encendido:", 0, 20)
    oled.text(texto, 0, 35)
    oled.show()

# Secuencia de encendido de LEDs
while True:
    for led, nombre in leds:
        # Apaga todos
        for l, _ in leds:
            l.value(0)
        # Enciende el actual
        led.value(1)
        mostrar_mensaje(nombre)
        time.sleep(3)
