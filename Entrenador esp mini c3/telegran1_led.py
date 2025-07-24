import network
import urequests as requests
import time
import ujson # Importar ujson para trabajar con JSON
from machine import Pin

# --- Configuración ---
SSID = "TCL"
PASSWORD = "elias1983"

BOT_TOKEN = "5553671950:AAEKsh4xEjhHoZ-w8LaBOjHCv2vv3MFV5vI"

# ID de chat autorizado (REEMPLAZA con tu ID de chat si quieres seguridad)
AUTHORIZED_CHAT_ID = 1543365473  # Ejemplo: "123456789" (asegúrate que sea un string)

LED_PIN = 0 # Pin GPIO al que está conectado el LED (puede ser distinto según tu ESP)

# --- Inicialización del LED ---
led = Pin(LED_PIN, Pin.OUT)
led.value(0) # Asegurarse de que el LED esté apagado al inicio

# --- Conexión WiFi ---
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Conectando a la red WiFi '{ssid}'...")
        wlan.connect(ssid, password)
        timeout = 10 # Segundos
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
        if wlan.isconnected():
            print("Conectado! IP:", wlan.ifconfig()[0])
        else:
            print("No se pudo conectar a la red WiFi.")
            return False
    return True

# --- Función para enviar mensajes con o sin teclado a Telegram ---
def send_telegram_message(chat_id, message, reply_markup=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message}
    if reply_markup:
        payload['reply_markup'] = ujson.dumps(reply_markup) # Convertir el diccionario a string JSON
    
    try:
        response = requests.post(url, json=payload)
        response.close()
    except Exception as e:
        print(f"Error al enviar mensaje a Telegram: {e}")

# --- Definición del teclado personalizado ---
# Los textos de los botones deben coincidir EXACTAMENTE con los comandos que esperas
main_keyboard = {
    "keyboard": [
        [{"text": "Encender LUZ"}, {"text": "Apagar LUZ"}],
        [{"text": "Estado de la LUZ"}] # Cambiado a "Estado de la LUZ"
    ],
    "resize_keyboard": True, # Hace el teclado más compacto
    "one_time_keyboard": False # El teclado permanece visible
}

# --- Bucle principal del bot ---
def main():
    if not connect_wifi(SSID, PASSWORD):
        print("Fallo en la conexión WiFi. Reintentando en 30 segundos...")
        time.sleep(30)
        return

    last_update_id = 0
    print("Bot de Telegram iniciado. Esperando comandos...")

    while True:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_update_id + 1}"
            r = requests.get(url)
            data = r.json()
            r.close()

            if "result" in data:
                for result in data["result"]:
                    update_id = result["update_id"]
                    if 'message' in result and 'text' in result['message']:
                        # Convertimos a minúsculas para hacer la comparación insensible a mayúsculas/minúsculas
                        message_text = result["message"]["text"].lower()
                        chat_id = result["message"]["chat"]["id"]

                        print(f"Mensaje recibido: '{message_text}' del chat ID: {chat_id}")

                        # Validar el chat_id si AUTHORIZED_CHAT_ID está configurado
                        if AUTHORIZED_CHAT_ID is not None and str(chat_id) != str(AUTHORIZED_CHAT_ID):
                            print(f"Mensaje ignorado de chat ID no autorizado: {chat_id}")
                            send_telegram_message(chat_id, "Lo siento, no estás autorizado para controlar este bot.")
                            continue

                        # Aquí es donde enviamos el teclado si el mensaje inicial es "/start"
                        if message_text == "/start":
                            send_telegram_message(chat_id, "Selecciona una opción para controlar la LUZ:", reply_markup=main_keyboard)
                        
                        # --- C O N D I C I O N E S   A C T U A L I Z A D A S ---
                        elif "encender luz" in message_text: # Ajustado para "encender luz"
                            led.value(1)
                            send_telegram_message(chat_id, "LUZ encendida 💡", reply_markup=main_keyboard)
                            print("LUZ encendida")
                        elif "apagar luz" in message_text: # Ajustado para "apagar luz"
                            led.value(0)
                            send_telegram_message(chat_id, "LUZ apagada 🌑", reply_markup=main_keyboard)
                            print("LUZ apagada")
                        elif "estado de la luz" in message_text: # Ajustado para "estado de la luz"
                            estado = "encendida" if led.value() == 1 else "apagada"
                            send_telegram_message(chat_id, f"La LUZ está: {estado}", reply_markup=main_keyboard)
                            print(f"Estado de la LUZ solicitado: {estado}")
                        else:
                            # Mensaje de error actualizado para reflejar los nuevos comandos/botones
                            send_telegram_message(chat_id, "Comando no reconocido. Por favor, usa los botones o envía 'Encender LUZ', 'Apagar LUZ' o 'Estado de la LUZ'.", reply_markup=main_keyboard)

                        last_update_id = update_id
            else:
                # No hay actualizaciones nuevas, no es necesario imprimir nada si no hay errores
                pass

        except OSError as e:
            print(f"Error de red (OSError): {e}. Reconectando a WiFi...")
            if not connect_wifi(SSID, PASSWORD):
                print("Fallo en la reconexión WiFi. Esperando 30 segundos...")
                time.sleep(30)
        except Exception as e:
            print(f"Error inesperado: {e}")

        time.sleep(10)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(1)