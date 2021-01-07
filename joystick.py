from machine import Pin, ADC
import utime

_PINX = 33   # needs to be a pin that supports ADC
_PINY = 35   # needs to be a pin that supports ADC
_PINSW = 21
_PINAIR = 32

class JOYSTICK:
    def __init__(self, ble_hid, display=None):
        self._display = display
        self._ble_hid = ble_hid

        print('Configuring joystick')
        if self._display: self._display.write_display('- c joystick')
        
        self._adcx = ADC(Pin(_PINX))
        self._adcx.atten(ADC.ATTN_11DB)
        self._adcy = ADC(Pin(_PINY))
        self._adcy.atten(ADC.ATTN_11DB)
        self._sw = Pin(_PINSW, Pin.IN, Pin.PULL_UP)
        self._air = Pin(_PINAIR, Pin.IN, Pin.PULL_UP)
        
        self._click_count = 0
        self._dragging = False
        self._drag_mode = False
        
        self._next_call_button = utime.ticks_ms()
        self._next_call_air = utime.ticks_ms()

        self._sw.irq(handler=self.button_pressed, trigger=Pin.IRQ_FALLING)
        self._air.irq(handler=self.air_flow, trigger=Pin.IRQ_RISING)

    def button_pressed(self, p):
        # enable and disable drap and drop mode
        if utime.ticks_ms() > self._next_call_button: # Debouncing, else every turning of wheel will cause a click
            print('Joystick Click')
            if self._ble_hid.is_connected():
                if self._drag_mode:
                    print('- disabling dragging and drop mode')
                    if self._display: self._display.write_display('- D drag-n-drop')
                    self._drag_mode = False
                else:
                    print('- enabling dragging and drop mode')
                    if self._display: self._display.write_display('- E drag-n-drop')
                    self._drag_mode = True
        self._next_call_button = utime.ticks_ms() + 200

    def air_flow(self, p):
        if utime.ticks_ms() > self._next_call_air: # Debouncing, else every turning of wheel will cause a click
            self._click_count += 1
            print('Air Flow', self._click_count)
            if self._ble_hid.is_connected():
                if not self._drag_mode:
                    print('- clicking')
                    if self._display: self._display.write_display('- clicked: '+str(self._click_count))
                    self._ble_hid.send_click(0)
                elif self._dragging:
                    print('- dropping')
                    if self._display: self._display.write_display('- dropping')
                    self._ble_hid.send_drag_release(0)
                    self._dragging = False
                else:
                    print('- dragging')
                    if self._display: self._display.write_display('- dragging')
                    self._ble_hid.send_drag(0)
                    self._dragging = True
        self._next_call_air = utime.ticks_ms() + 500

    def joystick(self, adc):
        if adc == 'x':
            return max(6, min(120, int(self._adcx.read()/32)))
        elif adc == 'y':
            return max(6, min(120, int(self._adcy.read()/32)))
        else:
            return None
