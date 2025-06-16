from machine import Pin, SoftI2C
from IR_remote import ir_receptor
import ssd1306
import time

# Inicializar receptor IR en el pin 4
Receptor_pin = ir_receptor(4)

# Configuración del OLED
sda = Pin(8)
scl = Pin(9)
i2c = SoftI2C(sda=sda, scl=scl, freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# LEDs
Led1 = Pin(0, Pin.OUT)
Led2 = Pin(1, Pin.OUT)
Led3 = Pin(2, Pin.OUT)
Led4 = Pin(3, Pin.OUT)

# Estados de los LEDs
led1_state = False
led2_state = False
led3_state = False
led4_state = False

# Función para mostrar el encabezado fijo y estados de LEDs
def mostrar_estados():
    oled.fill(0)
    oled.text("Entrenador esp", 0, 0)
    oled.text("LED1: {}".format("ON" if led1_state else "OFF"), 0, 16)
    oled.text("LED2: {}".format("ON" if led2_state else "OFF"), 0, 26)
    oled.text("LED3: {}".format("ON" if led3_state else "OFF"), 0, 36)
    oled.text("LED4: {}".format("ON" if led4_state else "OFF"), 0, 46)
    oled.show()

# Mostrar al inicio
mostrar_estados()

# Bucle principal
while True:
    irValue = Receptor_pin.ir_read()
    
    if irValue == '0x807f728d':  # Botón azul
        led1_state = not led1_state
        Led1.value(led1_state)
        mostrar_estados()
        
    elif irValue == '0x807fb04f':  # Otro botón
        led2_state = not led2_state
        Led2.value(led2_state)
        mostrar_estados()
        
    elif irValue == '0x807f30cf':
        led3_state = not led3_state
        Led3.value(led3_state)
        mostrar_estados()
        
    elif irValue == '0x807f52ad':
        led4_state = not led4_state
        Led4.value(led4_state)
        mostrar_estados()
        
    time.sleep(0.1)  # Para evitar rebotes o lecturas múltiples muy rápidas
