from machine import Pin, I2C, PWM
import ssd1306
import time
import random

# ------------------ Configuración de Hardware ------------------
# LEDs
leds = {
    0: Pin(0, Pin.OUT),   # Azul
    1: Pin(1, Pin.OUT),   # Verde
    2: Pin(2, Pin.OUT),   # Naranja
    3: Pin(3, Pin.OUT)    # Rojo
}

# Pulsadores (conectados a GND, pull-up interno)
botones = {
    0: Pin(5, Pin.IN, Pin.PULL_UP),   # Switch 1
    1: Pin(6, Pin.IN, Pin.PULL_UP),   # Switch 2
    2: Pin(7, Pin.IN, Pin.PULL_UP),   # Switch 3
    3: Pin(10, Pin.IN, Pin.PULL_UP)   # Switch 4
}

# Buzzer pasivo
buzzer = PWM(Pin(4))
buzzer.deinit()  # desactivar al inicio

# Pantalla OLED
i2c = I2C(0, scl=Pin(9), sda=Pin(8))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# ------------------ Funciones ------------------
def beep(frec=1000, duracion=200):
    buzzer.init(freq=frec, duty=512)
    time.sleep_ms(duracion)
    buzzer.deinit()

def mostrar(texto1, texto2=""):
    oled.fill(0)
    oled.text(texto1, 0, 20)
    oled.text(texto2, 0, 40)
    oled.show()

def prender_led(n, t=0.5):
    leds[n].on()
    beep(800 + n*200, 150)  # tono distinto por LED
    time.sleep(t)
    leds[n].off()

def esperar_boton(correcto):
    while True:
        for i in botones:
            if botones[i].value() == 0:  # presionado
                prender_led(i, 0.2)
                return i == correcto

# ------------------ Juego tipo Simon ------------------
secuencia = []
nivel = 1

mostrar("Juego LED Simon", "Presiona un btn")
time.sleep(2)

while True:
    # agregar un LED random a la secuencia
    secuencia.append(random.randint(0, 3))

    mostrar("Nivel {}".format(nivel))
    time.sleep(1)

    # mostrar la secuencia
    for paso in secuencia:
        prender_led(paso)
        time.sleep(0.2)

    # esperar la respuesta del jugador
    for paso in secuencia:
        if not esperar_boton(paso):
            mostrar("Perdiste!", "Nivel: {}".format(nivel))
            for i in range(3):
                beep(200, 300)
                time.sleep(0.2)
            secuencia = []
            nivel = 1
            time.sleep(2)
            mostrar("Reiniciando", "")
            time.sleep(2)
            break
    else:
        mostrar("¡Bien!", "Nivel {}".format(nivel))
        beep(1500, 300)
        nivel += 1
        time.sleep(1)
        continue
