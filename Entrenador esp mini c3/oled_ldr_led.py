from machine import Pin, SoftI2C, ADC
import ssd1306
import time

# Configuración I2C para la OLED
sda = Pin(8)
scl = Pin(9)
i2c = SoftI2C(sda=sda, scl=scl, freq=400000)

# Pantalla OLED 128x64
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Configuración del LDR en GPIO0
ldr = ADC(Pin(0))
ldr.atten(ADC.ATTN_11DB)   # Lectura hasta 3.3V
ldr.width(ADC.WIDTH_12BIT) # Resolución de 12 bits (0-4095)

# LED indicador en GPIO1
led = Pin(2, Pin.OUT)

while True:
    # Leer valor del LDR
    valor = ldr.read()
    voltaje = valor * (3.3 / 4095)  # Convertir a voltaje
    luz = int((valor / 4095) * 100)  # Escalar a 0-100%

    # Encender LED si la luz es <= 30%
    if luz <= 20:
        led.value(1)
        estado_led = "Encendido"
    else:
        led.value(0)
        estado_led = "Apagado"

    # Mostrar en consola
    print("LDR:", valor, " | Voltaje:", round(voltaje, 2), "V | Luz:", luz, "% | LED:", estado_led)

    # Mostrar en OLED
    oled.fill(0)  # Limpiar pantalla
    oled.text("Sensor LDR", 0, 0)
    oled.text("Valor: {}".format(valor), 0, 12)
    oled.text("Volt: {:.2f}V".format(voltaje), 0, 24)
    oled.text("Luz: {}%".format(luz), 0, 36)
    oled.text("LED: {}".format(estado_led), 0, 48)
    oled.show()

    time.sleep(0.5)
