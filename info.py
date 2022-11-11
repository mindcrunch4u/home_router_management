import requests
import scrape_headers
import json
import datetime
import os
from time import sleep

delay=10
time_info_start = {
        "year" :str(datetime.datetime.today().year),
        "month":str(datetime.datetime.today().month),
        "day":str(datetime.datetime.today().day),
        }
output_name = "log_" + time_info_start["year"] + "_" + time_info_start["month"] + "_" + time_info_start["day"] + ".txt"

def info(str_content):
    time = datetime.datetime.now()
    now = str(time)
    print("[INFO] [" + now + "]: " + str_content, flush=True)

def rotate_file():
    global output_name
    global time_info_start

    today = datetime.datetime.today()
    time_info_now = {
            "year" :str(today.year),
            "month":str(today.month),
            "day":str(today.day),
    }
    if time_info_start == time_info_now:
        return
    output_name = "log_" + time_info_now["year"] + "_" + time_info_now["month"] + "_" + time_info_now["day"] + ".txt"
    time_info_start = time_info_now
    info("file rotated to: " + output_name)

def to_file(str_content):
    global output_name
    time = datetime.datetime.now()
    now = str(time)
    try:
        output = open(output_name, "a");
        output.write("REC~" + now + os.linesep)
        output.write(str_content + os.linesep)
        output.close()
    except:
        info("write failure")

info("program starts")
endpoint = "http://192.168.0.1/app/devices/webs/getdeviceslist.cgi"
headers = scrape_headers.h_360_get_data
data = {"Qihoo_360_login":"7792650288e777f04d7e2b81b48c9fd6"}
while True:
    try:
        rotate_file()
        response_json = requests.post(endpoint, data=data, headers=headers, verify=False).json()
        to_file(json.dumps(response_json, indent=None))
        print(".", end="",flush=True)
    except:
        info("request failure")
    sleep(delay)
