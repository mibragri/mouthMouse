from machine import SPI, Pin
from ST7735 import TFT 
from sysfont import sysfont

class DISPLAY:
    def __init__(self):
        # Setting up display
        self._spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), ) #miso=Pin(12))
        self._tft = TFT(self._spi,2,14,17)
        self._tft.initr()
        self._tft.rgb(True)
        self._tft.fill(TFT.BLACK)
        self._v = 0

    def write_display(self, message, color='white', pos=None):
        if color == 'red':
            color = TFT.RED
        elif color == 'blue':
            color = TFT.BLUE
        elif color == 'green':
            color = TFT.GREEN
        else:
            color = TFT.WHITE
        if self._v == 160:
            self._v = 72
        if not pos:
            pos = self._v 
        self._tft.fillrect((0, pos), (128, 160), TFT.BLACK)
        self._tft.text((0, pos), message, color, sysfont, 1, nowrap=True)
        self._v += 8 # sysfont["Height"]

def main():
    print('Instantiating display')
    display = DISPLAY()
    write_display('It works', 'red')
    write_display('It works in green', 'green')
    write_display('It works', 'white', 72)


if __name__ == "__main__":
    main()
