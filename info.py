import requests
import scrape_headers
import json
import datetime
import os
from time import sleep
from scrape_crypto import to_crypto_string
from scrape_plugin import paint

delay=10
time_info_start = {
        "year" :str(datetime.datetime.today().year),
        "month":str(datetime.datetime.today().month),
        "day":str(datetime.datetime.today().day),
        }
output_name = "log_" + time_info_start["year"] + "_" + time_info_start["month"] + "_" + time_info_start["day"] + ".txt"
g_session = requests.Session()
g_cookie = None
g_token_id = None
g_header_get_data = scrape_headers.h_360_get_data

def info(str_content):
    time = datetime.datetime.now()
    now = str(time)
    print("[INFO] [" + now + "]: " + str_content, flush=True)

def rotate_file():
    global output_name
    global time_info_start

    time_info_before_rotation = time_info_start
    today = datetime.datetime.today()
    time_info_now = {
            "year" :str(today.year),
            "month":str(today.month),
            "day":str(today.day),
    }
    if time_info_start == time_info_now:
        paint_forced = False
    else:
        output_name = "log_" + time_info_now["year"] + "_" + time_info_now["month"] + "_" + time_info_now["day"] + ".txt"
        time_info_start = time_info_now
        info("file rotated to: " + output_name)
        paint_forced = True

    tmp_file_name = time_info_before_rotation["year"] + \
            "-" + time_info_before_rotation["month"] + \
            "-" + time_info_before_rotation["day"] + ".png"
    tmp_time_start = time_info_before_rotation["year"] + \
            "." + time_info_before_rotation["month"] + \
            "." + time_info_before_rotation["day"]
    tmp_time_end = None
    if not paint_forced:
        tmp_tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        tmp_time_info_tomorrow = {
                "year" :str(tmp_tomorrow.year),
                "month":str(tmp_tomorrow.month),
                "day":str(tmp_tomorrow.day),
        }
        tmp_time_end = tmp_time_info_tomorrow["year"] + "." + tmp_time_info_tomorrow["month"] + "." + tmp_time_info_tomorrow["day"]
    else:
        tmp_time_end = time_info_now["year"] + "." + time_info_now["month"] + "." + time_info_now["day"]
    paint(output_name, tmp_time_start, tmp_time_end, tmp_file_name, paint_forced)
    return

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

def calculate_crypt_string():
    endpoint = "http://192.168.0.1/router/get_rand_key.cgi?noneed=noneed"
    response_json = requests.get(endpoint, data={}, headers={}, timeout=4, verify=False).json()
    part_head = response_json['rand_key'][0:32]
    part_tail = response_json['rand_key'][32:]
    ivstring = "360luyou@install"
    password = "abcd6666"

    crypt_tail = to_crypto_string(part_tail, ivstring, password)
    print(part_head, part_tail)
    return part_head + crypt_tail

def refresh_header():
    global g_session
    global g_cookie
    global g_token_id
    global g_header_get_data
    endpoint = "http://192.168.0.1/router/web_login.cgi"
    string = calculate_crypt_string()
    info("crypt string: " + string + ", len: " + str(len(string)))
    data = {"user":"admin", "pass":str(string), "from": "1"}
    g_session = requests.Session()
    res = g_session.post(endpoint, data=data, headers=scrape_headers.h_360_get_token, timeout=4, verify=False).json()
    g_cookie = res["cookie"]
    g_token_id = res["token_id"]

def cleanup_procedure():
    global g_cookie
    global g_token_id
    global g_header_get_data
    g_header_get_data["Cookie"] = "Qihoo_360_login=" + g_cookie
    g_header_get_data["Referer"] = "http://192.168.0.1/new_index.htm?token_id=" + g_token_id
    g_header_get_data["token_id"] = g_token_id

def main():
    global g_header_get_data
    endpoint = "http://192.168.0.1/app/devices/webs/getdeviceslist.cgi"
    data = {}
    while True:
        try:
            rotate_file()
            response_json = requests.post(endpoint, data=data, headers=g_header_get_data, timeout=4, verify=False).json()
            to_file(json.dumps(response_json, indent=None))
            print(".", end="",flush=True)
        except Exception as e:
            info("request failure")
            print(e)
            try:
                refresh_header()
                cleanup_procedure()
            except Exception as es2:
                info("failed to refresh session")
        sleep(delay)

if __name__ == '__main__':
    info("program starts")
    refresh_header()
    cleanup_procedure()
    main()
