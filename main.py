from machine import Pin, ADC, SoftI2C, SPI
import bluetooth
import utime
from BLEHKBMouse import BLEHKBMouse
from display import DISPLAY
from wlan import WLAN
from joystick import JOYSTICK

# Setting up display
display = DISPLAY()
if display: display.write_display('Booting...', 'blue')

# Configuring WLAN
wlan = WLAN(display=display)

# BLE required before joystick to use ble in joystick class
print('Configuring BLE')
if display: display.write_display('- c bluetooth')
ble = bluetooth.BLE()
ble_mouse = BLEHKBMouse(ble, 'MB-Mouse')

# Configuring Joystick
joystick = JOYSTICK(ble_hid=ble_mouse, display=display)

# Define joystick range of center, else false movements
range1 = 52
range2 = 62

print('Starting loop')
if display: display.write_display('... startup completed', 'blue')

connect_informed = False
while True:
    while not ble_mouse.is_connected():
        utime.sleep_ms(2425) # needs 25ms, since clock tick of 240Hz (24ms)
        print('** ble disconnected')
        if display: display.write_display('** ble disconnected', 'red', 64)
        connect_informed = False
    while ble_mouse.is_connected():
        if not connect_informed:
            print('** ble connected')
            if display: display.write_display('** ble connected', 'green', 64)
            connect_informed = True
        utime.sleep_ms(100)
        x = joystick.joystick('x')
        y = joystick.joystick('y')
        try:
            if not x in range(range1,range2) and x > range2:
                ble_mouse.send_motion(10, 0)
                print('%.2f\t%.2f' % (x,y))
            if not x in range(range1,range2) and x < range1:
                ble_mouse.send_motion(-10, 0)
                print('%.2f\t%.2f' % (x,y))
            if not y in range(range1,range2) and y > range2:
                ble_mouse.send_motion(0, 10)
                print('%.2f\t%.2f' % (x,y))
            if not y in range(range1,range2) and y < range1:
                ble_mouse.send_motion(0, -10)
                print('%.2f\t%.2f' % (x,y))
            utime.sleep_ms(25)
        except Exception as e:
            print('*** Error: '+str(e), 'red')
            if display: display.write_display('* ERROR:', 'red')
            if display: display.write_display('** '+str(e), 'red')
