from machine import Pin
import time

# Configurar los pines de los LEDs
led_rojo = Pin(4, Pin.OUT)
led_naranja = Pin(3, Pin.OUT)
led_verde = Pin(2, Pin.OUT)

# Transistores de control para los dos dígitos
digit_ctrl = [
    Pin(1, Pin.OUT),  # Decenas
    Pin(0, Pin.OUT)   # Unidades
]

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

# Función para encender los segmentos de un dígito
def set_segments(num):
    for seg, pin in segment_pins.items():
        pin.value(digits[num][seg])

# Mostrar número de dos dígitos con multiplexado
def show_number(num, tiempo=0.2):
    decenas = num // 10
    unidades = num % 10
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < int(tiempo*1000):
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

# Función para apagar todos los LEDs
def apagar_todos_leds():
    led_rojo.value(0)
    led_naranja.value(0)
    led_verde.value(0)

# Programa principal
while True:
    # Primera fase: LED rojo durante 15 segundos
    print("Encendiendo LED rojo - Contando 15 segundos")
    led_rojo.value(1)
    for i in range(15, 0, -1):
        show_number(i, tiempo=1)  # Mostrar el contador en el display
    
    # Segunda fase: LED rojo + naranja durante 5 segundos
    print("Encendiendo LED naranja - Contando 5 segundos")
    led_naranja.value(1)
    for i in range(5, 0, -1):
        show_number(i, tiempo=1)  # Mostrar el contador en el display
    
    # Tercera fase: Apagar rojo y naranja, encender verde durante 15 segundos
    print("Apagando rojo y naranja, encendiendo verde - Contando 15 segundos")
    apagar_todos_leds()
    led_verde.value(1)
    for i in range(15, 0, -1):
        show_number(i, tiempo=1)  # Mostrar el contador en el display
    
    # Cuarta fase: Apagar verde, encender naranja durante 5 segundos
    print("Apagando verde, encendiendo naranja - Contando 5 segundos")
    led_verde.value(0)
    led_naranja.value(1)
    for i in range(5, 0, -1):
        show_number(i, tiempo=1)  # Mostrar el contador en el display
    
    # Apagar naranja para comenzar de nuevo
    led_naranja.value(0)
    print("Ciclo completado. Reiniciando...\n")