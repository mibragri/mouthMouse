import network
import utime

class WLAN:
    def __init__(self, display=None):
        self._display = display
        if self._display: self._display.write_display('- AP started')
        self._ap = network.WLAN(network.AP_IF)
        self._ap.active(True)
        self._ap_ip = self._ap.ifconfig()
        print('AP config:', self._ap_ip)

        self._wlan = network.WLAN(network.STA_IF)
        if not self._wlan.isconnected():
            self._wlan.active(True)
            while not self._wlan.active():
                print('Waiting for WLAN to become active')
                utime.sleep_ms(200)
                pass
            print('Scanning for WLANs')
            self._ssids = self._wlan.scan()
            for tupl in self._ssids:
                if b'mibra' in tupl:
                    print('- found SSID mibra, connecting...')
                    if self._display: self._display.write_display('- wlan mibra')
                    self._wlan.connect('mibra', 'mile2017')
                    while not self._wlan.isconnected():
                        pass
                    self._ip = self._wlan.ifconfig()
                    print('- IP: '+str(self._ip[0]))
                    print('- network config:', self._wlan.ifconfig())
                    if self._display: self._display.write_display('- IP: '+str(self._ip[0]))
                    print('- disabling AP mode')
                    self._ap.active(False)
                    if self._display: self._display.write_display('- AP stopped')
                    break
                else:
                    print('- found no suitable SSID')
                    if self._display: self._display.write_display('- wlan not found')
                    self._wlan.active(False)

        if self._wlan.isconnected():
            print('Starting webrepl, since WLAN is connected')
            import webrepl
            webrepl.start()

def main():
    wlan = WLAN()
    print('Is WLAN connected?')
    print(wlan._wlan.isconnected())

if __name__ == "__main__":
    main()
