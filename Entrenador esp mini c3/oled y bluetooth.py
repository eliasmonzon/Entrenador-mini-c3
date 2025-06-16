import bluetooth
from machine import Pin, SoftI2C
import ssd1306
import time
from bluetooth_ble import BLEUART

# Configurar I2C y OLED
sda = Pin(8)
scl = Pin(9)
i2c = SoftI2C(sda=sda, scl=scl, freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Inicializar Bluetooth BLE UART
ble = bluetooth.BLE()
uart = BLEUART(ble)

# Mostrar mensaje inicial
oled.fill(0)
oled.text("Esperando datos", 0, 0)
oled.show()

# Función para manejar datos recibidos
def on_rx():
    data = uart.read().decode().strip()
    print("Recibido:", data)

    # Mostrar en la pantalla OLED
    oled.fill(0)
    oled.text("Bluetooth:", 0, 0)
    oled.text(data[:21], 0, 16)  # Máx 21 caracteres por línea
    oled.text(data[21:42], 0, 32)
    oled.text(data[42:63], 0, 48)
    oled.show()

# Asociar función al evento de recepción
uart.irq(handler=on_rx)

# Bucle principal (puede estar vacío)
while True:
    time.sleep(1)
