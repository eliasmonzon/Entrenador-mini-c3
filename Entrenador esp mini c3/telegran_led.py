import network
import urequests as requests
import time
from machine import Pin

# Configuración WiFi
SSID = "TCL"
PASSWORD = "elias1983"

# Token del bot
BOT_TOKEN = "5553671950:AAEKsh4xEjhHoZ-w8LaBOjHCv2vv3MFV5vI"

# Control del LED
led = Pin(0, Pin.OUT)

# Conexión a WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    print("Conectando a WiFi...")
    time.sleep(1)

print("Conectado! IP:", wlan.ifconfig()[0])

# Estado del último mensaje procesado
last_update_id = 0

while True:
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_update_id + 1}"
        r = requests.get(url)
        data = r.json()
        for result in data["result"]:
            update_id = result["update_id"]
            message = result["message"]["text"]
            chat_id = result["message"]["chat"]["id"]

            print("Mensaje recibido:", message)

            if message == "On":
                led.value(1)
            elif message == "Off":
                led.value(0)

            last_update_id = update_id

        r.close()
    except Exception as e:
        print("Error:", e)

    time.sleep(5)
