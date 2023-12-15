if __name__ == '__main__':
    # scan available address
    addresses = scan(force=True)
    print(f"addresses : {addresses}")
    data_dict = {}
    data_dict['datetime'] = []
    for address in addresses:
        data_dict[str(address)] = []

    for cnt in range(TOTAL_ROUND):
        print(f'Round : {cnt}')
        start_time = time.time()
        data_dict['datetime'].append(get_datetime())
        for address in addresses:
            try:
                data = bus.read_i2c_block_data(address, 0, 27)
                sensor_model = (data[1] << 8) + data[2]
                if sensor_model != 0:
                    co2 = struct.unpack('!f', bytes(data[11:15]))[0]
                    dt_data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f'address : {address}')
                    print(f'co2 : {co2}')
                    print(f'date time : {dt_data}')
                    data_dict[str(address)].append(co2)
                else:
                    data_dict[str(address)].append(0)
                time.sleep(1)
            except:
                print(f"can't read {address}")
                data_dict[str(address)].append(0)
                time.sleep(1)

        while (time.time() - start_time < TIME_DELAY):
            pass

    create_excel(data_dict)
    upload_to_dropbox(ACCESS_TOKEN, EXCEL_FILE_PATH, DROPBOX_PATH)

    {
        '1',[1,2,3],
        '2',[4,5,6],
        '3',[7,8,9],
        'datetime' : ['1', '2','3']
    }
