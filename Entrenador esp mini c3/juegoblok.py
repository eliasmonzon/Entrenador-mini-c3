from machine import Pin, I2C, PWM
import ssd1306
import time
import random

# --- Configuración OLED ---
i2c = I2C(0, scl=Pin(9), sda=Pin(8))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# --- Controles ---
btn_left = Pin(5, Pin.IN, Pin.PULL_UP)
btn_right = Pin(6, Pin.IN, Pin.PULL_UP)

# --- Buzzer ---
buzzer = PWM(Pin(21))
buzzer.duty(0)

def beep(freq=1000, t=50):
    buzzer.freq(freq)
    buzzer.duty(512)
    time.sleep_ms(t)
    buzzer.duty(0)

# --- Función principal del juego ---
def jugar():
    # Variables iniciales
    paddle_x = 50
    paddle_w = 20
    paddle_h = 3
    paddle_y = 60

    ball_x = 64
    ball_y = 40
    ball_dx = 1
    ball_dy = -1
    ball_r = 2

    # Bloques
    blocks = []
    cols = 8
    rows = 5
    block_w = 14
    block_h = 6
    for r in range(rows):
        for c in range(cols):
            blocks.append([c*block_w+2, r*block_h+10, True])  # x, y, visible

    vidas = 3
    puntos = 0

    # --- Función para dibujar ---
    def draw_game():
        oled.fill(0)
        # Mostrar puntos y vidas
        oled.text("P:"+str(puntos), 0, 0)
        oled.text("V:"+str(vidas), 100, 0)

        # Bloques
        for b in blocks:
            if b[2]:
                oled.fill_rect(b[0], b[1], block_w-2, block_h-2, 1)

        # Paleta
        oled.fill_rect(paddle_x, paddle_y, paddle_w, paddle_h, 1)

        # Bola
        oled.fill_rect(int(ball_x), int(ball_y), ball_r, ball_r, 1)

        oled.show()

    # --- Bucle de juego ---
    while True:
        # Movimiento de paleta
        if not btn_left.value() and paddle_x > 0:
            paddle_x -= 2
        if not btn_right.value() and paddle_x < 128-paddle_w:
            paddle_x += 2

        # Movimiento bola
        ball_x += ball_dx
        ball_y += ball_dy

        # Rebote bordes
        if ball_x <= 0 or ball_x >= 128-ball_r:
            ball_dx = -ball_dx
            beep(800, 30)
        if ball_y <= 8:  # debajo del marcador
            ball_dy = -ball_dy
            beep(800, 30)

        # Rebote con paleta
        if (paddle_y-2 <= ball_y <= paddle_y and
            paddle_x <= ball_x <= paddle_x+paddle_w):
            ball_dy = -ball_dy
            beep(1200, 50)

        # Choque con bloques
        for b in blocks:
            if b[2]:
                if (b[0] <= ball_x <= b[0]+block_w and
                    b[1] <= ball_y <= b[1]+block_h):
                    b[2] = False
                    ball_dy = -ball_dy
                    puntos += 10
                    beep(1500, 60)
                    break

        # Bola perdida
        if ball_y > 64:
            vidas -= 1
            beep(400, 300)
            if vidas == 0:
                oled.fill(0)
                oled.text("GAME OVER", 30, 30)
                oled.show()
                time.sleep(2)
                return  # terminar juego
            else:
                # Reiniciar bola
                ball_x = 64
                ball_y = 40
                ball_dx = random.choice([-1, 1])
                ball_dy = -1
                time.sleep(1)

        # Ganaste si todos los bloques se borraron
        if all(not b[2] for b in blocks):
            oled.fill(0)
            oled.text("GANASTE!", 30, 30)
            oled.show()
            beep(2000, 300)
            time.sleep(2)
            return

        draw_game()
        time.sleep(0.02)

# --- Bucle principal del sistema ---
while True:
    jugar()  # jugar una partida
    # pantalla de reinicio
    oled.fill(0)
    oled.text("Pulsa derecha", 10, 20)
    oled.text("para reiniciar", 10, 40)
    oled.show()
    # esperar botón
    while btn_right.value():
        time.sleep(0.1)
