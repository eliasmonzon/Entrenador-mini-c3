from machine import Pin, SoftI2C
import ssd1306
import time

# Configuración del OLED
sda = Pin(8)
scl = Pin(9)
i2c = SoftI2C(sda=sda, scl=scl, freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Configuración de los LEDs
led1 = Pin(1, Pin.OUT)
led2 = Pin(2, Pin.OUT)
led3 = Pin(3, Pin.OUT)
led4 = Pin(4, Pin.OUT)

# Configuración de los botones con pull-up interno
boton1 = Pin(21, Pin.IN, Pin.PULL_UP)
boton2 = Pin(20, Pin.IN, Pin.PULL_UP)
boton3 = Pin(10, Pin.IN, Pin.PULL_UP)
boton4 = Pin(5, Pin.IN, Pin.PULL_UP)

# Función para mostrar el encabezado fijo y el estado dinámico
def mostrar(mensaje):
    oled.fill(0)
    oled.text("Entrenador esp", 0, 0)  # Línea fija superior
    oled.text(mensaje, 0, 16)          # Mensaje dinámico debajo
    oled.show()

while True:
    mensaje = ""

    if not boton1.value():
        led1.on()
        mensaje = "LED 1 encendido"
    else:
        led1.off()

    if not boton2.value():
        led2.on()
        mensaje = "LED 2 encendido"
    else:
        led2.off()

    if not boton3.value():
        led3.on()
        mensaje = "LED 3 encendido"
    else:
        led3.off()

    if not boton4.value():
        led4.on()
        mensaje = "LED 4 encendido"
    else:
        led4.off()

    if mensaje:
        mostrar(mensaje)
    else:
        mostrar("Ningun LED activo")

    time.sleep(0.1)
