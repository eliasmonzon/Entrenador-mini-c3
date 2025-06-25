from imagenes import * #importa todo lo que hay en imagenes 
import framebuf

class ojos:
    def __init__(self, oled):
        self.oled = oled  # Instancia de la pantalla OLED

        # Datos de los ojos
        ojos_data = [ojos0,ojos1,ojos2,ojos3,ojos4,ojos5,ojos6,ojos7,ojos8,
                     ojos9,ojos10,ojos11,ojos12,ojos13,ojos14,ojos15,ojos16]
        
        # Cargar buffers de imágenes
        self.frames = []
        for ojos in ojos_data:
            buffer = bytearray(ojos)
            fb = framebuf.FrameBuffer(buffer, 128, 64, framebuf.MONO_HLSB)  # Tamaño ajustado a 115x55
            self.frames.append(fb)
    
    def mostrar_ojos(self, index):
        """Muestra un par de ojos en la pantalla OLED según el índice."""
        if 0 <= index < len(self.frames):
            self.oled.fill(0)  # Limpiar la pantalla
            self.oled.blit(self.frames[index], 0, 3)  # Dibujar el frame
            self.oled.show()
        else:
            print("Índice fuera de rango:", index)
