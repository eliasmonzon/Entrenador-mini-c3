from machine import Pin, ADC
import time

# Pines de segmentos (a-g) - Ajusta según tu conexión real
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
    Pin(1, Pin.OUT),  # Decenas
    Pin(0, Pin.OUT)   # Unidades
]

# Configurar LDR en GPIO4 (ADC)
ldr = ADC(Pin(4))
ldr.atten(ADC.ATTN_11DB)  # Rango completo 0-3.3V
UMBRAL_OSCURO = 2000      # Ajusta este valor según pruebas (0-4095)

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

# -------- PROGRAMA PRINCIPAL -----------
contador = 0
estado_prev = False  # Estado anterior del LDR (True = oscuro, False = claro)

while True:
    # Leer valor del LDR (0-4095)
    ldr_valor = ldr.read()
    
    # Determinar si está oscuro (por encima del umbral)
    # Nota: En esta configuración, más luz = menor resistencia = mayor voltaje
    oscuro_actual = ldr_valor > UMBRAL_OSCURO
    
    # Detectar transición de claro a oscuro (flanco ascendente de oscuridad)
    if oscuro_actual and not estado_prev:
        contador += 1
        if contador > 99:
            contador = 0
        print(f"Contador: {contador}, Valor LDR: {ldr_valor}")
        time.sleep_ms(300)  # Pequeña pausa para evitar detecciones múltiples

    # Actualizar estado anterior
    estado_prev = oscuro_actual

    # Mostrar número actual
    show_number(contador, tiempo=0.1)