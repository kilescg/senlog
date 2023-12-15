import smbus2

class I2C_Trinity:
    def __init__(self, bus):
        self.bus = smbus2.SMBus(bus)

    def scan(self):
        devices = []
        for addr in range(0x03, 0x77 + 1):
            try:
                data = self.bus.read_byte(addr)
                devices.append(addr)
            except OSError as expt:
                if expt.errno == 16:
                    pass
        return  devices
