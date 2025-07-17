try:
    import usocket as socket
except:
    import socket

from machine import Pin
import network
import time
import gc

gc.collect()

# Conexión WiFi
ssid = 'E13'
password = 'elias1983'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    pass

print('Conexión exitosa')
print(station.ifconfig())

# Pines
relay = Pin(3, Pin.OUT)  # Usamos GPIO10 en vez de GPIO2
boton = Pin(5, Pin.IN, Pin.PULL_DOWN)
estado_anterior = 0  # Para detectar flanco del botón

# Página web con AJAX para actualizar estado del relé
def web_page():
    if relay.value() == 1:
        relay_state = ''
    else:
        relay_state = 'checked'
    
    html = """<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {
  font-family: Times New Roman;
  text-align: center;
  margin: 0px auto;
  padding-top: 30px;
}
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}
.switch input {
  display: none;
}
.slider {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  border-radius: 40px;
}
.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: #fff;
  transition: .4s;
  border-radius: 24px;
}
input:checked + .slider {
  background-color: #FF3333;
}
input:checked + .slider:before {
  transform: translateX(26px);
}
</style>

<script>
// Envía ON/OFF según el cambio del checkbox
function toggleCheckbox(element) {
    var xhr = new XMLHttpRequest(); 
    if (element.checked) {
        xhr.open("GET", "/?relay=off", true);
    } else {
        xhr.open("GET", "/?relay=on", true);
    } 
    xhr.send();
}

// Sincroniza el checkbox con el estado del relé cada 1 segundo
setInterval(function() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            var estado = xhr.responseText.trim();
            var checkbox = document.getElementById("relaySwitch");
            if (estado === "ON") {
                checkbox.checked = false;
            } else {
                checkbox.checked = true;
            }
        }
    }
    xhr.open("GET", "/estado", true);
    xhr.send();
}, 1000);
</script>
</head>
<body>
<h1>Mi casa</h1>
<label class="switch">
<input type="checkbox" id="relaySwitch" onchange="toggleCheckbox(this)" %s>
<span class="slider"></span>
</label>
<h3> OFF ON</h3>
</body>
</html>""" % (relay_state)

    return html

# Configuración del servidor web
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
s.settimeout(0.1)  # No bloquear, así se puede leer el botón

# Bucle principal
while True:
    try:
        # === Leer botón físico ===
        estado_actual = boton.value()
        if estado_actual == 1 and estado_anterior == 0:
            print('Botón presionado')
            if relay.value() == 1:
                relay.value(0)
                print('Relé encendido')
            else:
                relay.value(1)
                print('Relé apagado')
            time.sleep(0.3)  # Antirebote

        estado_anterior = estado_actual

        # === Atender conexiones web ===
        try:
            conn, addr = s.accept()
            conn.settimeout(3.0)
            print('Conexión de %s' % str(addr))
            request = conn.recv(1024)
            conn.settimeout(None)
            request = str(request)
            print('Petición:', request)

            # Cambios por web
            if '/?relay=on' in request:
                relay.value(0)
                print('Relé ON desde web')
            elif '/?relay=off' in request:
                relay.value(1)
                print('Relé OFF desde web')
            elif '/estado' in request:
                estado = 'ON' if relay.value() == 0 else 'OFF'
                conn.send('HTTP/1.1 200 OK\n')
                conn.send('Content-Type: text/plain\n')
                conn.send('Connection: close\n\n')
                conn.sendall(estado)
                conn.close()
                continue  # Ya respondimos

            # Página principal
            response = web_page()
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()

        except OSError:
            pass  # No hubo conexión, seguir

    except Exception as e:
        print('Error general:', e)
        time.sleep(1)
