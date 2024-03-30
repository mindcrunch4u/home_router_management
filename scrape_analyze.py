import datetime
import json
import sys
from enum import Enum
from dateutil.relativedelta import relativedelta
from configuration import default_config

global_y_axis = []
global_x_axis = []
global_search_name = default_config.plot_host_name

time_range = {
        "year"  : 1,
        "month" : 2,
        "day"   : 3,
        "hour"  : 4,
        "minute": 5,
        "second": 6,
        }

def info(string_content):
    print("[INFO] " + str(string_content), flush=True)

def date_to_list(string_date):
    # accepted format: 2022-11-09 23:45:31.340576
    section = string_date.split(" ")
    ret_list = []
    for rougher in section[0].split('-'):
        ret_list.append(rougher)
    for finer in section[1].split('.')[0].split(':'):
        ret_list.append(finer)
    return ret_list

def process_file(file_name):
    is_waiting_for_data = False
    last_key = None
    stored_dict = dict()
    try:
        f = open(file_name,"r")
    except:
        print("can\'t open file: " + file_name)
        return None
    for line in f:
        if is_waiting_for_data:
            stored_dict[last_key] = line
            is_waiting_for_data = False
        elif line.startswith("REC~"):
            date_list = date_to_list(line.split("~")[1])
            last_key = tuple(date_list)
            is_waiting_for_data = True
    return stored_dict

def is_key_exist(tuple_key, dict_data, match_range):
    range_index = time_range[match_range]
    for item in dict_data:
        if tuple_key[0:range_index] == item[0:range_index]:
            return True
    return False

def find_with_key(tuple_key, dict_data, match_range):
    ret_list = []
    range_index = time_range[match_range]
    for item in dict_data:
        if tuple_key[0:range_index] == item[0:range_index]:
            ret_list.append(item)
    return ret_list

def time_to_int(dateobj):
    total = int(dateobj.strftime('%S'))
    total += int(dateobj.strftime('%M')) * 60
    total += int(dateobj.strftime('%H')) * 60 * 60
    total += (int(dateobj.strftime('%j')) - 1) * 60 * 60 * 24
    total += (int(dateobj.strftime('%Y')) - 1970) * 60 * 60 * 24 * 365
    return total

def iterate_time_with_granularity(processor, data_dict, list_start_date, list_end_date, string_time_range, plot_granularity, inc=1):
    date_start = datetime.datetime(*list_start_date)
    date_end   = datetime.datetime(*list_end_date)
    dict_length = len(data_dict)
    dict_index = 0

    if date_start > date_end:
        info("end date can\'t be ealier than start date.")
        return
    
    date_diff = time_to_int(date_end) - time_to_int(date_start)

    while date_start < date_end:
        if string_time_range == "year":
            date_start += relativedelta(years=+inc)
        elif string_time_range == "month":
            date_start += relativedelta(months=+inc)
        elif string_time_range == "day":
            date_start += relativedelta(days=+inc)
        elif string_time_range == "hour":
            date_start += relativedelta(hours=+inc)
        elif string_time_range == "minute":
            date_start += relativedelta(minutes=+inc)
        elif string_time_range == "second":
            date_start += relativedelta(seconds=+inc)
        else:
            info("date incremental format not supported")
            break
        tmp_date_string = str(date_start)
        storage_key = tuple(date_to_list(tmp_date_string))
        list_in_time_range = find_with_key(storage_key, data_dict, string_time_range)
        processor(data_dict, storage_key, list_in_time_range, plot_granularity) # function pointer
        dict_index += 1
        print(
                "Progress: %.2f%%,  %s - %s"
                %
                (
                    (1 - ((time_to_int(date_end) - time_to_int(date_start))/date_diff))*100
                    , date_start
                    , date_end
                )
                , end='\r'
            )

'''
----------------------------------------------------------------------------------------------------
                        Non-Generic Functions Begin
----------------------------------------------------------------------------------------------------
'''
def get_int_usage_by_key(data_dict, tuple_key):
    string_json = data_dict[tuple_key]
    data_json = json.loads(string_json)
    for item in data_json["data"]:
        if item["name"] == global_search_name:
            return (int(item["up_speed"]) + int(item["down_speed"]))/8/1024/1024
    return 0

def jot_down_y_axis(data_dict, storage_key, list_in_time_range, granularity):
    # from "data_dict", using "storage_key", found "list_in_time_range"
    global global_y_axis
    global global_x_axis
    int_usage = 0
    # search through each storage_key, and sum up internet usage
    for item in list_in_time_range:
        int_usage += get_int_usage_by_key(data_dict, item)
    global_y_axis.append(int_usage)
    #global_x_axis.append("-".join(storage_key[time_range["hour"]-1:time_range[granularity]]))
    #global_x_axis.append(storage_key[time_range[granularity]-1])  # <-- this works
    global_x_axis.append("/".join(storage_key[0:time_range[granularity]]))

def plot_array(plot_granularity, save_as="plot.png"):
    global global_y_axis
    import numpy as np
    import matplotlib.pyplot as plt
    plt.rcParams["figure.figsize"] = [8, 3.50]
    plt.rcParams["figure.autolayout"] = True
    plt.rcParams.update({'font.size': 8})
    plt.title("Line graph")
    #plt.locator_params(nbins=4)

    fig, ax = plt.subplots()
    fig.autofmt_xdate()

    x = np.array(global_x_axis)
    y = np.array(global_y_axis)

    plt.xlabel("Time: " + plot_granularity)
    plt.ylabel("Megabytes(MB) In Total")

    plt.plot(x, y, color="red")
    plt.savefig(save_as)
    plt.close('all')

def arg_time_to_int_list(input_str):
    ret = []
    ret.append( int(input_str.split('.')[0] ))
    ret.append( int(input_str.split('.')[1] ))
    ret.append( int(input_str.split('.')[2] ))
    return ret
'''
----------------------------------------------------------------------------------------------------
                        Non-Generic Functions Ends
----------------------------------------------------------------------------------------------------
'''

def clear_globals():
    global global_y_axis
    global global_x_axis
    global_y_axis = []
    global_x_axis = []

def main():
    if len(sys.argv) < 5:
        print("prog <file> <start date> <end date> <output file>")
        print("example: prog 2022_11_20.txt 2022.11.20 2022.11.21 2022-11-20.png")
        return
    target_file = sys.argv[1]
    #target_file = "log_2022_11_20.txt"
    start   = arg_time_to_int_list( sys.argv[2] )
    end     = arg_time_to_int_list( sys.argv[3] )
    save_as = sys.argv[4]
    #start   = [2022,11,21]
    #end     = [2022,11,21]

    #default:
    collection_granularity = "minute"
    plot_granularity = "hour"

    #very fine:
    #collection_granularity = "second"
    #plot_granularity = "hour"

    # { (2022, 2, 22, h, m, s) : json_data }
    data_dict = process_file(target_file) 
    if data_dict == None:
        return
    # search dict with an increment, through start date and end date, call processor at each iteration
    iterate_time_with_granularity(jot_down_y_axis, data_dict, start, end, collection_granularity, plot_granularity) 
    plot_array(plot_granularity, save_as=save_as)

def analyze(file_path, str_time_start, str_time_end, collection_granularity, plot_granularity, output_path):
    start   = arg_time_to_int_list( str_time_start )
    end     = arg_time_to_int_list( str_time_end   )
    save_as = output_path

    data_dict = process_file(file_path) 
    if data_dict == None:
        return
    iterate_time_with_granularity(jot_down_y_axis, data_dict, start, end, collection_granularity, plot_granularity) 
    plot_array(plot_granularity, save_as=save_as)
    print("",flush=True)

if __name__ == "__main__":
    main()
