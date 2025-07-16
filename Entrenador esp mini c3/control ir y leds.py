from machine import Pin
from IR_remote import ir_receptor
Receptor_pin = ir_receptor(4)
Led1 = Pin(0, Pin.OUT)
Led2 = Pin(1,Pin.OUT)
Led3 = Pin(2,Pin.OUT)
Led4 = Pin(3,Pin.OUT)
led1_state = False
led2_state = False
led3_state = False
led4_state = False
while True:
    irValue = Receptor_pin.ir_read()
    if irValue == '0xf720df':
      led1_state = not led1_state  # Cambiar el estado del LED
      Led1.value(led1_state)  # Encender o apagar el LED según el estado
    elif irValue == '0xf7a05f':
      led2_state = not led2_state  # Cambiar el estado del LED
      Led2.value(led2_state)  # Encender o apagar el LED según el estado
    elif irValue == '0xf7609f':
      led3_state = not led3_state  # Cambiar el estado del LED
      Led3.value(led3_state)  # Encender o apagar el LED según el estado
    elif irValue == '0xf7e01f':
      led4_state = not led4_state  # Cambiar el estado del LED
      Led4.value(led4_state)  # Encender o apagar el LED según el estado
      
 