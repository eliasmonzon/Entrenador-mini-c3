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

# Configurar 4 relés y 4 botones físicos
reles = [Pin(pin, Pin.OUT) for pin in [3, 2, 1, 0]]
botones = [Pin(pin, Pin.IN, Pin.PULL_DOWN) for pin in [5, 6, 7, 10]]

# Inicializar relés apagados (rele.value(0) = apagado)
for rele in reles:
    rele.value(0)

estado_anterior = [0, 0, 0, 0]

# Página web con AJAX sincronizado
def web_page():
    checks = ['checked' if rele.value() == 1 else '' for rele in reles]

    html = """<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {
  font-family: Arial;
  text-align: center;
  padding-top: 30px;
  background-color: #f0f0f0;
}
.grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 30px;
  justify-items: center;
  max-width: 500px;
  margin: 0 auto;
}
.switch {
  position: relative;
  display: inline-block;
  width: 120px;
  height: 70px;
}
.switch input { display: none; }
.slider {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: #2196F3;
  border-radius: 40px;
  transition: background-color 0.4s;
}
.slider:before {
  position: absolute;
  content: "";
  height: 50px;
  width: 50px;
  left: 10px;
  bottom: 10px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}
input:checked + .slider {
  background-color: red;
}
input:checked + .slider:before {
  transform: translateX(50px);
}
.estado {
  font-size: 20px;
  margin-top: 10px;
}
</style>

<script>
function toggleCheckbox(idx, element) {
    var xhr = new XMLHttpRequest();
    var estado = element.checked ? "on" : "off";
    xhr.open("GET", "/?rele=" + idx + "&estado=" + estado, true);
    xhr.send();
}

setInterval(function() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            var estados = xhr.responseText.trim().split(",");
            for (let i = 0; i < 4; i++) {
                var checkbox = document.getElementById("rele" + i);
                checkbox.checked = (estados[i] === "1");
                document.getElementById("estado" + i).innerText = checkbox.checked ? "Encendido" : "Apagado";
            }
        }
    }
    xhr.open("GET", "/estados", true);
    xhr.send();
}, 1000);
</script>
</head>
<body>
<h1>Control de 4 Relés</h1>
<div class="grid">
""" + "".join(f"""
  <div>
    <label class="switch">
      <input type="checkbox" id="rele{i}" onchange="toggleCheckbox({i}, this)" {checks[i]}>
      <span class="slider"></span>
    </label>
    <div class="estado" id="estado{i}">{'Encendido' if checks[i] else 'Apagado'}</div>
    <div>Relé {i+1}</div>
  </div>
""" for i in range(4)) + """
</div>
</body>
</html>
"""
    return html

# Servidor web
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
s.settimeout(0.1)

while True:
    try:
        for i in range(4):
            actual = botones[i].value()
            if actual == 1 and estado_anterior[i] == 0:
                print(f"Pulsador {i+1} presionado")
                reles[i].value(0 if reles[i].value() == 1 else 1)
                time.sleep(0.2)
            estado_anterior[i] = actual

        try:
            conn, addr = s.accept()
            conn.settimeout(3.0)
            print('Conexión de', addr)
            request = conn.recv(1024)
            conn.settimeout(None)
            request = str(request)
            print('Petición:', request)

            if '/?rele=' in request:
                try:
                    idx = int(request.split("rele=")[1].split("&")[0])
                    estado = request.split("estado=")[1].split(" ")[0]
                    if 0 <= idx < 4:
                        reles[idx].value(1 if estado == "on" else 0)
                        print(f"Relé {idx+1} desde web: {estado}")
                except:
                    pass

            if '/estados' in request:
                estados = [str(rele.value()) for rele in reles]
                conn.send('HTTP/1.1 200 OK\n')
                conn.send('Content-Type: text/plain; charset=utf-8\n')
                conn.send('Connection: close\n\n')
                conn.sendall(",".join(estados))
                conn.close()
                continue

            response = web_page()
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html; charset=utf-8\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()

        except OSError:
            pass

    except Exception as e:
        print("Error general:", e)
        time.sleep(1)
