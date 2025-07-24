import network
import requests as requests
import time
import json
from machine import Pin

# --- Configuración WiFi y Bot ---
SSID = "TCL"
PASSWORD = "elias1983"
BOT_TOKEN = "5553671950:AAEKsh4xEjhHoZ-w8LaBOjHCv2vv3MFV5vI"
AUTHORIZED_CHAT_ID = 1543365473  # ← Tu ID real obtenido de @userinfobot

# --- Pines ---
LED_WIFI = 0        # GPIO0: LED de estado WiFi
LED_TELEGRAM = 1    # GPIO1: LED controlado
ENTRADA_PIN = 21    # GPIO21: Entrada desde TTP223

# --- Inicialización de pines ---
led_wifi = Pin(LED_WIFI, Pin.OUT)
led_telegram = Pin(LED_TELEGRAM, Pin.OUT)
entrada = Pin(ENTRADA_PIN, Pin.IN, Pin.PULL_DOWN)

led_wifi.value(0)
led_telegram.value(0)

# Variable global para detectar flanco
estado_anterior = 0

# --- Función para conectar WiFi ---
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Conectando a la red WiFi '{ssid}'...")
        wlan.connect(ssid, password)
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
        if wlan.isconnected():
            print("¡Conectado! IP:", wlan.ifconfig()[0])
            led_wifi.value(1)
        else:
            print("No se pudo conectar.")
            led_wifi.value(0)
            return False
    else:
        led_wifi.value(1)
    return True

# --- Enviar mensajes a Telegram ---
def send_telegram_message(chat_id, message, reply_markup=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message}
    if reply_markup:
        payload['reply_markup'] = json.dumps(reply_markup)
    try:
        response = requests.post(url, json=payload)
        response.close()
    except Exception as e:
        print(f"Error al enviar mensaje a Telegram: {e}")

# --- Teclado en Telegram ---
main_keyboard = {
    "keyboard": [
        [{"text": "Encender LUZ"}, {"text": "Apagar LUZ"}],
        [{"text": "Estado de la LUZ"}]
    ],
    "resize_keyboard": True,
    "one_time_keyboard": False
}

# --- Bucle principal ---
def main():
    global estado_anterior  # Para flanco

    if not connect_wifi(SSID, PASSWORD):
        print("Fallo WiFi. Reintentando en 30s...")
        time.sleep(30)
        return

    last_update_id = 0
    print("Bot de Telegram iniciado. Esperando comandos...")

    while True:
        try:
            # --- Lectura de Telegram ---
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_update_id + 1}"
            r = requests.get(url)
            data = r.json()
            r.close()

            if "result" in data:
                for result in data["result"]:
                    update_id = result["update_id"]
                    if 'message' in result and 'text' in result['message']:
                        message_text = result["message"]["text"].lower()
                        chat_id = result["message"]["chat"]["id"]

                        print(f"Mensaje recibido: '{message_text}' de ID: {chat_id}")

                        if AUTHORIZED_CHAT_ID and str(chat_id) != str(AUTHORIZED_CHAT_ID):
                            send_telegram_message(chat_id, "No estás autorizado.")
                            continue

                        if message_text == "/start":
                            send_telegram_message(chat_id, "Selecciona una opción para controlar la LUZ:", reply_markup=main_keyboard)

                        elif "encender luz" in message_text:
                            led_telegram.value(1)
                            send_telegram_message(chat_id, "LUZ encendida 💡", reply_markup=main_keyboard)

                        elif "apagar luz" in message_text:
                            led_telegram.value(0)
                            send_telegram_message(chat_id, "LUZ apagada 🌑", reply_markup=main_keyboard)

                        elif "estado de la luz" in message_text:
                            estado = "encendida" if led_telegram.value() else "apagada"
                            send_telegram_message(chat_id, f"La LUZ está: {estado}", reply_markup=main_keyboard)

                        else:
                            send_telegram_message(chat_id, "Comando no reconocido. Usá los botones.", reply_markup=main_keyboard)

                        last_update_id = update_id

            # --- Revisión de GPIO21 (TTP223) ---
            estado_actual = entrada.value()
            if estado_actual == 1 and estado_anterior == 0:
                # Flanco de subida → alternar LED
                nuevo_estado = 0 if led_telegram.value() else 1
                led_telegram.value(nuevo_estado)
                print("TTP223 tocado → LED Telegram:", "Encendido" if nuevo_estado else "Apagado")

                # Notificación garantizada
                send_telegram_message(
                    AUTHORIZED_CHAT_ID,
                    f"LUZ cambiada por sensor: {'encendida 💡' if nuevo_estado else 'apagada 🌑'}",
                    reply_markup=main_keyboard
                )

            estado_anterior = estado_actual

        except OSError as e:
            print(f"Error de red: {e}")
            if not connect_wifi(SSID, PASSWORD):
                print("Reintento fallido. Esperando 30s...")
                time.sleep(30)
        except Exception as e:
            print(f"Error inesperado: {e}")

        time.sleep(0.2)

# --- Ejecutar ---
if __name__ == "__main__":
    while True:
        main()
        time.sleep(1)
