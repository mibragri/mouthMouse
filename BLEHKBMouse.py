import bluetooth, struct
from micropython import const


_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
_IRQ_GATTS_READ_REQUEST = const(4)
_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_SERVICE_RESULT = const(9)
_IRQ_GATTC_SERVICE_DONE = const(10)
_IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
_IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
_IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
_IRQ_GATTC_DESCRIPTOR_DONE = const(14)
_IRQ_GATTC_READ_RESULT = const(15)
_IRQ_GATTC_READ_DONE = const(16)
_IRQ_GATTC_WRITE_DONE = const(17)
_IRQ_GATTC_NOTIFY = const(18)
_IRQ_GATTC_INDICATE = const(19)
_IRQ_GATTS_INDICATE_DONE = const(20)
_IRQ_MTU_EXCHANGED = const(21)
_IRQ_L2CAP_ACCEPT = const(22)
_IRQ_L2CAP_CONNECT = const(23)
_IRQ_L2CAP_DISCONNECT = const(24)
_IRQ_L2CAP_RECV = const(25)
_IRQ_L2CAP_SEND_READY = const(26)
_IRQ_CONNECTION_UPDATE = const(27)
_IRQ_ENCRYPTION_UPDATE = const(28)
_IRQ_GET_SECRET = const(29)
_IRQ_SET_SECRET = const(30)

_F_READ = bluetooth.FLAG_READ
_F_WRITE = bluetooth.FLAG_WRITE
_F_READ_WRITE = bluetooth.FLAG_READ | bluetooth.FLAG_WRITE
_F_READ_NOTIFY = bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY

_ATT_F_READ = 0x01
_ATT_F_WRITE = 0x02

_UUID = bluetooth.UUID

_HID_SERVICE = (
    _UUID(0x1812),  # Human Interface Device
    (
        (_UUID(0x2A4A), _F_READ),  # HID information
        (_UUID(0x2A4B), _F_READ),  # HID report map
        (_UUID(0x2A4C), _F_WRITE),  # HID control point
        (_UUID(0x2A4D), _F_READ_NOTIFY, ((_UUID(0x2908), _ATT_F_READ),)),  # HID report / reference
        (_UUID(0x2A4E), _F_READ_WRITE),  # HID protocol mode
    ),
)

# fmt: off
_HID_REPORT_MAP = bytes([
    0x05, 0x01,     # Usage Page (Generic Desktop)
    0x09, 0x02,     # Usage (Mouse)
    0xA1, 0x01,     # Collection (Application)
    0x09, 0x01,     #     Usage (Pointer)
    0xA1, 0x00,     #     Collection (Physical)
    0x85, 0x01,     #         Report ID (1)
    0x95, 0x03,     #         Report Count (3)
    0x75, 0x01,     #         Report Size (1)
    0x05, 0x09,     #         Usage Page (Buttons)
    0x19, 0x01,     #         Usage Minimum (1)
    0x29, 0x03,     #         Usage Maximum (3)
    0x15, 0x00,     #         Logical Minimum (0)
    0x25, 0x01,     #         Logical Maximum (1)
    0x81, 0x02,     #         Input(Data, Variable, Absolute); 3 button bits
    0x95, 0x01,     #         Report Count(1)
    0x75, 0x05,     #         Report Size(5)
    0x81, 0x01,     #         Input(Constant);                 5 bit padding
    0x75, 0x08,     #         Report Size (8)
    0x95, 0x02,     #         Report Count (3)
    0x05, 0x01,     #         Usage Page (Generic Desktop)
    0x09, 0x30,     #         Usage (X)
    0x09, 0x31,     #         Usage (Y)
    0x09, 0x38,     #         Usage (Wheel)
    0x15, 0x81,     #         Logical Minimum (-127)
    0x25, 0x7F,     #         Logical Maximum (127)
    0x81, 0x06,     #         Input(Data, Variable, Relative); 3 position bytes (X,Y,Wheel)
    0xC0,           #     End Collection
    0xC0,           # End Collection
])
# fmt: on

# register services
#handles = ble.gatts_register_services((hid_service,))

class BLEHKBMouse:
    def __init__(self, ble, name="MP-Mouse"):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        print('- handles, register hid service')
        ((self._h_info, self._h_hid, self._, self._h_rep, self._h_d1, self._h_proto),) = self._ble.gatts_register_services((_HID_SERVICE,))
        #_h_info, _h_hid, _, _h_rep, _h_d1, _h_proto = handles[0]
        print('- setting initial hid data')
        self._ble.gatts_write(self._h_info, b"\x01\x01\x00\x02")  # HID info: ver=1.1, country=0, flags=normal
        self._ble.gatts_write(self._h_hid, _HID_REPORT_MAP)  # HID report map
        self._ble.gatts_write(self._h_d1, struct.pack("<BB", 1, 1))  # report: id=1, type=input
        self._ble.gatts_write(self._h_proto, b"\x01")  # protocol mode: report
        self._connections = set()
        self._write_callback = None
        self._secrets = {}
        self._payload = (
            b"\x02\x01\x06"
            b"\x03\x03\x12\x18"  # complete list of 16-bit service UUIDs: 0x1812
            b"\x03\x19\xc2\x03"  # appearance: mouse
            b"\x09\x09"+name  # complete local name
        )
        self._advertise()

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            _conn_handle, _, _ = data
            self._connections.add(_conn_handle)
            print("BLE connect: ", event, data)
            #save_secrets()
        elif event == _IRQ_CENTRAL_DISCONNECT:
            _conn_handle, _, _ = data
            self._connections.remove(_conn_handle)
            print("BLE disconnect", event, data)
            self._advertise()
        elif event == _IRQ_SET_SECRET:
            sec_type, key, value = data
            key = sec_type, bytes(key)
            value = bytes(value) if value else None
            print("- set secret:", key, value)
            if value is None:
                if key in _secrets:
                    del _secrets[key]
                    return True
                else:
                    return False
            else:
                _secrets[key] = value
            return True
        elif event == _IRQ_GET_SECRET:
            sec_type, index, key = data
            print("- get secret:", sec_type, index, bytes(key) if key else None)
            if key is None:
                i = 0
                for (t, _key), value in _secrets.items():
                    if t == sec_type:
                        if i == index:
                            return value
                        i += 1
                return None
            else:
                key = sec_type, bytes(key)
                return _secrets.get(key, None)
        elif event == _IRQ_MTU_EXCHANGED:
            print('- MTU exchanged')
        else:
            print("other events:", event, data)
            _conn_handle = data[0]

    def is_connected(self):
        return len(self._connections) > 0

    def _advertise(self):
        #print('- loading secrets')
        #load_secrets()
        print('Advertising BLE device')
        self._ble.gap_advertise(100_000, adv_data=self._payload)

    def send_mouse(self, button_mask, x, y, wheel):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._h_rep, struct.pack("4B", button_mask, x, y, wheel))

    def send_drag_release(self, button):
        self.send_mouse(0, 0, 0, 0) # required to release mouse click, else it would drag

    def send_drag(self, button):
        self.send_mouse(1 << button, 0, 0, 0)

    def send_click(self, button):
        self.send_mouse(1 << button, 0, 0, 0)
        self.send_mouse(0, 0, 0, 0) # required to release mouse click, else it would drag

    def send_motion(self, x, y):
        self.send_mouse(0, int(x), int(y), 0)

    def load_secrets(self):
        try:
            with open("secrets.json", "r") as f:
                entries = json.load(f)
                for sec_type, key, value in entries:
                    _secrets[sec_type, binascii.a2b_base64(key)] = binascii.a2b_base64(value)
        except:
            print("*** no secrets available")

    def save_secrets(self):
        try:
            with open("secrets.json", "w") as f:
                json_secrets = [
                    (sec_type, binascii.b2a_base64(key), binascii.b2a_base64(value))
                    for (sec_type, key), value in _secrets.items()
                ]
                json.dump(json_secrets, f)
        except:
            print("*** failed to save secrets")

def main():
    print('Initiating BLE')
    ble = bluetooth.BLE()
    m = BLEHKBMouse(ble)
    #print('- enabling BLE security')
    #try:
        #ble.config(le_secure=True)
    #except Exception as e:
        #print('*** could not enable security')
        #print('*** Error:', str(e))
    #print('- enabling BLE bonding')
    #try:
        #ble.config(bond=True)
    #except Exception as e:
        #print('*** could not enable bonding')
        #print('*** Error:', str(e))
    #print('- configuring BLE irq')
    #ble.irq(ble_irq)
    while True:
        time.sleep(0.500)
        if m.is_connected():
            print('Mouse connected')
        else:
            print('Mouse not connected')


if __name__ == "__main__":
    main()


