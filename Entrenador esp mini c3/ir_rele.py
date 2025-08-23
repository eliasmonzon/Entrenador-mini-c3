from machine import Pin
from IR_remote import ir_receptor
Receptor_pin = ir_receptor(1)
Rele = Pin(0, Pin.OUT)
Rele_state = False
while True:
    irValue = Receptor_pin.ir_read()
    if irValue == '0xf7c03f':
      Rele_state = not Rele_state  # Cambiar el estado del Rele
      Rele.value(Rele_state) 
   