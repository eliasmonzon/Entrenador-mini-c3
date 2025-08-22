from machine import Pin, PWM
import time

# Pines de segmentos (a-g)
segment_pins = {
    "a": Pin(5, Pin.OUT),
    "b": Pin(6, Pin.OUT),
    "c": Pin(7, Pin.OUT),
    "d": Pin(8, Pin.OUT),
    "e": Pin(9, Pin.OUT),
    "f": Pin(10, Pin.OUT),
    "g": Pin(20, Pin.OUT)
}

# Transistores de control para los dos dígitos
digit_ctrl = [
    Pin(4, Pin.OUT), # Dígito de las unidades 
    Pin(21, Pin.OUT)# Dígito de las decenas
]

# Relé en GPIO1
rele = Pin(1, Pin.OUT)

# Buzzer pasivo en GPIO2 (PWM)
buzzer = PWM(Pin(2))
buzzer.deinit()  # apagado inicial

# Mapas de segmentos (ánodo común)
digits = {
    0: {"a":0,"b":0,"c":0,"d":0,"e":0,"f":0,"g":1},
    1: {"a":1,"b":0,"c":0,"d":1,"e":1,"f":1,"g":1},
    2: {"a":0,"b":0,"c":1,"d":0,"e":0,"f":1,"g":0},
    3: {"a":0,"b":0,"c":0,"d":0,"e":1,"f":1,"g":0},
    4: {"a":1,"b":0,"c":0,"d":1,"e":1,"f":0,"g":0},
    5: {"a":0,"b":1,"c":0,"d":0,"e":1,"f":0,"g":0},
    6: {"a":0,"b":1,"c":0,"d":0,"e":0,"f":0,"g":0},
    7: {"a":0,"b":0,"c":0,"d":1,"e":1,"f":1,"g":1},
    8: {"a":0,"b":0,"c":0,"d":0,"e":0,"f":0,"g":0},
    9: {"a":0,"b":0,"c":0,"d":0,"e":1,"f":0,"g":0}
}

# Función para escribir un número en los segmentos
def set_segments(num):
    for seg, pin in segment_pins.items():
        pin.value(digits[num][seg])

# Mostrar un número de dos dígitos con multiplexado
def show_number(num, tiempo=1):
    decenas = num // 10
    unidades = num % 10
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < tiempo * 1000:
        # Mostrar decenas
        set_segments(decenas)
        digit_ctrl[0].value(1)
        time.sleep_ms(5)
        digit_ctrl[0].value(0)

        # Mostrar unidades
        set_segments(unidades)
        digit_ctrl[1].value(1)
        time.sleep_ms(5)
        digit_ctrl[1].value(0)

# Apagar display
def clear_display():
    for pin in segment_pins.values():
        pin.value(1)
    for ctrl in digit_ctrl:
        ctrl.value(0)

# Función para activar relé + buzzer pasivo
def alarma(duracion=2, freq=1000):
    rele.value(1)
    buzzer.init(freq=freq, duty=512)  # iniciar buzzer a freq Hz
    time.sleep(duracion)
    buzzer.deinit()   # apagar buzzer
    rele.value(0)

# Programa principal: contar de 00 a 99
while True:
    for n in range(100):
        show_number(n, tiempo=1)
        if n == 99:
            alarma(duracion=2, freq=1000)  # sonar buzzer pasivo a 1kHz
    clear_display()
    time.sleep(1)
