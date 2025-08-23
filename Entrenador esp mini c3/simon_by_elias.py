from machine import Pin, I2C, PWM
import ssd1306
import time
import random

# ------------------ Pines según tu pedido ------------------
# LED azul GPIO0, verde GPIO1, naranja GPIO2, rojo GPIO3
led_pins = [0, 1, 2, 3]
leds = [Pin(p, Pin.OUT) for p in led_pins]

# Botones a GND con pull-up: sw1 GPIO5, sw2 GPIO6, sw3 GPIO7, sw4 GPIO10
btn_pins = [10, 7, 6, 5]
botones = [Pin(p, Pin.IN, Pin.PULL_UP) for p in btn_pins]

# Buzzer pasivo en GPIO4
buzzer = PWM(Pin(4))
buzzer.freq(1200)
# Apagar buzzer
try:
    buzzer.duty(0)
except AttributeError:
    buzzer.duty_u16(0)

# OLED SSD1306 en I2C0: scl=9, sda=8
i2c = I2C(0, scl=Pin(9), sda=Pin(8))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# ------------------ Utilidades ------------------
def beep(freq=1000, ms=150, vol=0.5):
    """Bip compatible ESP32/ESP32-C3 (duty o duty_u16)."""
    buzzer.freq(freq)
    try:
        buzzer.duty(int(1023 * max(0, min(1, vol))))
    except AttributeError:
        buzzer.duty_u16(int(65535 * max(0, min(1, vol))))
    time.sleep_ms(ms)
    try:
        buzzer.duty(0)
    except AttributeError:
        buzzer.duty_u16(0)

def mostrar(t1="", t2=""):
    oled.fill(0)
    if t1: oled.text(t1, 0, 18)
    if t2: oled.text(t2, 0, 36)
    oled.show()

def prender_led(i, t=0.45):
    """Enciende LED i con tono único y lo apaga."""
    leds[i].on()
    beep(800 + i*220, 140)   # tonos distintos por LED
    time.sleep(t)
    leds[i].off()

def esperar_boton(correcto):
    """Espera botón, enciende su LED, hace debouncing y devuelve si fue el correcto."""
    while True:
        for i, btn in enumerate(botones):
            if btn.value() == 0:        # presionado (a GND)
                prender_led(i, 0.18)
                # esperar a que suelte (debounce)
                while btn.value() == 0:
                    time.sleep_ms(10)
                return i == correcto
        time.sleep_ms(1)

# ------------------ Efectos ------------------
def efecto_inicio():
    """Pantalla + barrido de luces con arpegio."""
    mostrar("SIMON", "by Elias")
    time.sleep(0.4)
    # Barrido hacia adelante
    for i in range(4):
        leds[i].on(); beep(500 + i*250, 120, 0.6); time.sleep(0.05); leds[i].off()
    # Barrido hacia atrás
    for i in reversed(range(4)):
        leds[i].on(); beep(700 + i*200, 100, 0.6); time.sleep(0.05); leds[i].off()
    time.sleep(0.4)

def efecto_error():
    """Todos los LEDs parpadean con tonos graves descendentes."""
    mostrar("Perdiste!", "")
    for f in (400, 320, 240):
        for _ in range(2):
            for L in leds: L.on()
            beep(f, 160, 0.7)
            for L in leds: L.off()
            time.sleep(0.12)

# ------------------ Juego tipo Simon ------------------
random.seed()     # usa ruido interno para variar la secuencia
secuencia = []
nivel = 1

efecto_inicio()
mostrar("Juego LED Simon", "Presiona un btn")
time.sleep(1200/1000)

while True:
    # Agregar un paso aleatorio (0..3) y mostrar nivel
    secuencia.append(random.randint(0, 3))
    mostrar("Nivel {}".format(nivel), "Observa la secuencia")
    time.sleep(600/1000)

    # Mostrar la secuencia
    for paso in secuencia:
        prender_led(paso, 0.35)
        time.sleep(0.18)

    # Repetir la secuencia con botones
    mostrar("Repite", "Nivel {}".format(nivel))
    correcto = True
    for paso in secuencia:
        if not esperar_boton(paso):
            correcto = False
            break

    if correcto:
        mostrar("¡Bien!", "Nivel {}".format(nivel))
        beep(1600, 220, 0.7)  # tono de acierto
        nivel += 1
        time.sleep(0.6)
    else:
        efecto_error()
        # Reinicio
        secuencia = []
        nivel = 1
        time.sleep(0.8)
        efecto_inicio()
        mostrar("Juego LED Simon", "Presiona un btn")
        time.sleep(0.8)

