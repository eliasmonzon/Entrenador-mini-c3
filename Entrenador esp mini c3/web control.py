try:
    import usocket as socket
except:
    import socket

from machine import Pin
import network
import time
import gc

gc.collect()

ssid = 'E13'
password = 'elias1983'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass

print('Connection successful')
print(station.ifconfig())

# Definición de pines
relay = Pin(2, Pin.OUT)
boton = Pin(16, Pin.IN, Pin.PULL_DOWN)

def web_page():
    if relay.value() == 1:
        relay_state = ''
    else:
        relay_state = 'checked'
    
    # Empieza el HTML  
    html = """<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style> body{
  font-family: time roman; 
  text-align: center; 
  margin: 0px auto; 
  padding-top: 30px;
}
.switch{
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}
.switch input{
 display: none;
}
.slider{
  position: absolute;
  top: 1;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  border-radius: 40px;
}
.slider:before{
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
input:checked+.slider{
  background-color: #FF3333;
}
input:checked+.slider:before{
  transform: translateX(26px);
}
</style>
<script>
function toggleCheckbox(element) {
    var xhr = new XMLHttpRequest(); 
    if (element.checked) {
        xhr.open("GET", "/?relay=off", true);
    } else {
        xhr.open("GET", "/?relay=on", true);
    } 
    xhr.send();
}
</script>
</head>
<body>
<h1>Mi casa </h1>
<label class="switch">
<input type="checkbox" onchange="toggleCheckbox(this)" %s>
<span class="slider"></span>
</label>
<h3> OFF ON</h3>
</body></html>""" % (relay_state)
    
    return html

# Configuración del socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    try:
        if gc.mem_free() < 102000:
            gc.collect()
        
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print('Content = %s' % request)
        
        relay_on = request.find('/?relay=on')
        relay_off = request.find('/?relay=off')
        
        # Control del relé desde la web
        if relay_on != -1:
            print('RELAY ON desde web')
            relay.value(0)  # Encender el relé
        if relay_off != -1:
            print('RELAY OFF desde web')
            relay.value(1)  # Apagar el relé

        # Control del relé desde el pulsador
        if boton.value() == 1:  # Detectar pulsación del botón
            # Alternar el estado del relé
            if relay.value() == 1:  # Si el relé está apagado
                print('RELAY ON desde pulsador')
                relay.value(0)  # Encender el relé
            else:  # Si el relé está encendido
                print('RELAY OFF desde pulsador')
                relay.value(1)  # Apagar el relé
            
            # Esperar un momento para evitar rebotes
            time.sleep(0.3)  

        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
