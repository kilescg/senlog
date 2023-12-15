import smbus2
import time
import struct
from utils import *
from rich import print
from rich.pretty import pprint

model_require_data_dict = {
    '2': 2,
    '3': 1
}

model_name_dict = {
    '2': 'Panasonic SN-GCJA5',
    '3': 'Sensirion SCD4x'
}

class I2C_Trinity:
    def __init__(self, bus):
        self.bus = smbus2.SMBus(bus)

    def scan(self):
        devices = []
        for addr in range(0x03, 0x77 + 1):
            try:
                self.bus.read_byte(addr)
                devices.append(str(addr))
            except OSError as expt:
                if expt.errno == 16:
                    pass
        return  devices
    
    def read_sensor(self,address):
        # Interface with sensor
        msg = smbus2.i2c_msg.read(int(address), 27)
        self.bus.i2c_rdwr(msg)

        # data management
        data = bytes(msg)
        data_size = data[0]
        '''
        sensirion = Model 1
        Panasonic = Model 2
        '''
        model_id = (data[1] << 8) + data[2]
        error_status = (data[5] << 24) + (data[6] << 16) + (data[7] << 8) + data[8]
        float_data_1 = struct.unpack('!f', bytes(data[11:15]))[0]
        float_data_2 = struct.unpack('!f', bytes(data[17:21]))[0]
        float_data_3 = struct.unpack('!f', bytes(data[23:27]))[0]
        return data_size, model_id, error_status, [float_data_1, float_data_2, float_data_3]
       
    
    def start_test(self, round, interval):
        devices = {}
        addresses = self.scan()

        '''
        Classifiy Sensor Type
        '''
        for address in addresses:
            _, model_id, _, _ = self.read_sensor(address)
            model_id = str(model_id)
            if address not in devices:
                devices[address] = {}
                devices[address]['log'] = []
            devices[address]['model_id'] = model_id

        for cnt in range(round):
            print()
            print(f"[bold cyan] Round [/bold cyan] : [green]{cnt}[/green]")
            print(f'[green]{get_human_datetime()}[/green]')
            print()
            for address in addresses:
                try:
                    start_time = time.time()

                    _, model_id, _, packet_data = self.read_sensor(address)
                    model_id = str(model_id)
                    
                    targeted_data = packet_data[model_require_data_dict[model_id]]
                    devices[address]['log'].append({
                        'data' : targeted_data,
                        'datetime' : get_datetime()
                    })
                    print(f'[bold magenta]Address [/bold magenta] : [orchid]{address}[orchid], [bold light_coral]Type[/bold light_coral] : [salmon1]{model_name_dict[model_id]}[/salmon1], [bold cyan]Data[/bold cyan] : [blue]{targeted_data}[blue]')
                    # devices['datetime'].append(get_datetime())
                except Exception as error:
                    print(f"[red] Can't read data on address [/red] : [bold red]{address}[/bold red]")
                    print("An exception occurred:", error)

                time.sleep(0.1)
        
        while (time.time() - start_time < interval):
            if (cnt == (round-1)):
                break

        # pprint(devices)
        # while(1):
        #     pass
