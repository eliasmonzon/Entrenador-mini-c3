from machine import Pin, I2C
import ssd1306
import time

# OLED
i2c = I2C(0, scl=Pin(9), sda=Pin(8))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# LEDs
leds = [Pin(0, Pin.OUT), Pin(1, Pin.OUT), Pin(2, Pin.OUT),Pin(3, Pin.OUT)]
estados = [False, False, False,False]

# Botones: arriba, abajo, seleccionar
btn_up = Pin(5, Pin.IN, Pin.PULL_UP)
btn_down = Pin(6, Pin.IN, Pin.PULL_UP)
btn_select = Pin(7, Pin.IN, Pin.PULL_UP)

menu = ["Azul", "Verde", "Naranja", "Rojo",]
indice = 0

def mostrar_menu():
    oled.fill(0)
    oled.text("MENU", 20,0)
    for i in range(len(menu)):
        prefijo = "-> " if i == indice else "   "
        oled.text(prefijo + menu[i], 0, 10 + i * 10)

    oled.show()

# Estados anteriores para flanco
ultimo_up = 1
ultimo_down = 1
ultimo_sel = 1
mostrar_menu()  # Mostrar menú al iniciar
while True:
    
    act_up = btn_up.value()
    act_down = btn_down.value()
    act_sel = btn_select.value()

    if ultimo_up == 1 and act_up == 0:
        indice = (indice - 1) % len(menu)
        mostrar_menu()
   
        

    if ultimo_down == 1 and act_down == 0:
        indice = (indice + 1) % len(menu)
        mostrar_menu()

    if ultimo_sel == 1 and act_sel == 0:
        estados[indice] = not estados[indice]
        leds[indice].value(estados[indice])
        mostrar_menu()
        
    ultimo_up = act_up
    ultimo_down = act_down
    ultimo_sel = act_sel
    time.sleep(0.1)
