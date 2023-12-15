#!/usr/bin/env python3
import pandas as pd
import smbus2
import struct
import time
import datetime
import csv
import os
import math
from smbus2 import SMBus, i2c_msg
from openpyxl.chart import (
    LineChart,
    Reference,
)

TIME_DELAY = 60
TOTAL_ROUND = 60
ACCESS_TOKEN = "sl.Bp81JXGMMHaWruKbEQzpeeuzf9IaRI4tq4Pe3iak9uY8fzCp6zjD1yNW9F1uj-eOj556HPfpQqc-UYVv0A8iCbXMQ-48cerH5KVoWfbauI1H17UYvlZL_gr4QS7Dsd0J-ESDfn6MOi2Q"
EXCEL_FILE_PATH = "/home/trinity/sensor_checker/sensor_db.xlsx"
DROPBOX_PATH = "/sensor_db.xlsx"

excel_file = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'sensor_db.xlsx')

bus = smbus2.SMBus(1)


def get_datetime():
    return time.strftime('%Y-%m-%d %H:%M:%S')

def get_sheet_datetime():
    return time.strftime('%Y-%m-%d %H_%M_%S')


def add_data_to_csv(file_path, fieldnames, data_list):
    if not os.path.exists(file_path):
        with open(file_path, 'x', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(fieldnames)
    with open(file_path, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(data_list)

def create_excel(data_dict):
    sheet_name = get_sheet_datetime()
    df = pd.DataFrame(data_dict)
    if os.path.exists(excel_file):
        writer = pd.ExcelWriter(excel_file, engine='openpyxl', mode='a')
    else:
        writer = pd.ExcelWriter(excel_file, engine='openpyxl')
    df.to_excel(writer, sheet_name=sheet_name)

    workbook  = writer.book
    worksheet = writer.sheets[sheet_name]

    chart_cnt = math.ceil(len(data_dict) / 10)

    for chart_num in range(chart_cnt):
        if (chart_num == chart_cnt - 1) and (len(data_dict) % 10 != 0):
            data_point = len(data_dict) % 10 - 1
        else:
            data_point = 10

        # Create a chart
        if data_point <= 0:
            continue

        chart = LineChart()
        chart.title = f"Panasonic SN-GCJA5 Test Sample {chart_num}"
        chart.x_axis.title = "Test number"
        chart.y_axis.title = "PM 2.5 (µg/m³)"
        chart.style = 10

        for data_num in range(data_point):
            series = Reference(
                worksheet,
                min_col=(chart_num * 10) + data_num + 3,
                min_row=1,
                # max_col=(chart_num * 10) + data_num + 3,
                max_row=TOTAL_ROUND + 1,
            )
            chart.add_data(series, titles_from_data=True)
            # chart.set_categories(series)

        chart_location = f"{number_to_letters((chart_num * 10) + 1)}{TOTAL_ROUND + 3}"
        worksheet.add_chart(chart, chart_location)

        # Save the workbook to a file
        workbook.save(excel_file)

    writer.close()


if __name__ == '__main__':
    for cnt in range(TOTAL_ROUND):
        print(f'Round : {cnt}')
        start_time = time.time()
        for address in addresses:
            msg = i2c_msg.read(address, 27)
            bus.i2c_rdwr(msg)
            data = bytes(msg)
            sensor_model = (data[1] << 8) + data[2]
            if sensor_model != 0:
                pm2_5 = struct.unpack('!f', bytes(data[17:21]))[0]
                print(f'address : {address}')
                print(f'pm2.5 : {pm2_5}')
        time.sleep(1)
