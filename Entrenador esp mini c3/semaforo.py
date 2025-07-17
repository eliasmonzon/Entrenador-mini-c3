from machine import Pin, I2C
import ssd1306
import time

# --- OLED ---
i2c = I2C(0, scl=Pin(9), sda=Pin(8))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# --- LEDs ---
led_rojo = Pin(3, Pin.OUT)
led_naranja = Pin(2, Pin.OUT)
led_verde = Pin(1, Pin.OUT)

# --- Función para mostrar números grandes ---
def mostrar_numero_grande(num):
    oled.fill(0)
    # Cada número ocupa 3 filas x 3 columnas de píxeles (bloques), tamaño aproximado.
    numeros = {
        0: [" ### ",
            "#   #",
            "#   #",
            "#   #",
            "#   #",
            "#   #",
            " ### "],
        1: ["  #  ",
            " ##  ",
            "# #  ",
            "  #  ",
            "  #  ",
            "  #  ",
            "#####"],
        2: [" ### ",
            "#   #",
            "    #",
            "   # ",
            "  #  ",
            " #   ",
            "#####"],
        3: [" ### ",
            "#   #",
            "    #",
            " ### ",
            "    #",
            "#   #",
            " ### "],
        4: ["   # ",
            "  ## ",
            " # # ",
            "#  # ",
            "#####",
            "   # ",
            "   # "],
        5: ["#####",
            "#    ",
            "#    ",
            "#### ",
            "    #",
            "#   #",
            " ### "],
        6: [" ### ",
            "#   #",
            "#    ",
            "#### ",
            "#   #",
            "#   #",
            " ### "],
        7: ["#####",
            "    #",
            "   # ",
            "  #  ",
            " #   ",
            " #   ",
            " #   "],
        8: [" ### ",
            "#   #",
            "#   #",
            " ### ",
            "#   #",
            "#   #",
            " ### "],
        9: [" ### ",
            "#   #",
            "#   #",
            " ####",
            "    #",
            "#   #",
            " ### "]
    }
    dig = numeros[num]
    for i, fila in enumerate(dig):
        oled.text(fila, 20, i * 8)
    oled.show()

# --- Función para mostrar mensaje ---
def mostrar_mensaje(msg):
    oled.fill(0)
    oled.text(msg, 10, 25)
    oled.show()

# --- Bucle principal del semáforo ---
while True:
    # --- Luz verde: cruzar ---
    led_rojo.off()
    led_naranja.off()
    led_verde.on()
    for t in range(5, 0, -1):  # Cuenta regresiva de 5 a 1
        mostrar_numero_grande(t)
        time.sleep(1)

    # --- Luz naranja: advertencia ---
    led_verde.off()
    led_naranja.on()
    mostrar_mensaje("¡ATENCION!")
    time.sleep(2)

    # --- Luz roja: no cruzar ---
    led_naranja.off()
    led_rojo.on()
    mostrar_mensaje("ESPERA...")
    time.sleep(5)
 # --- Luz naranja: advertencia ---
    led_verde.off()
    led_naranja.on()
    mostrar_mensaje("¡ATENCION!")
    time.sleep(2)
