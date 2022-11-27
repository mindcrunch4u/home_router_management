from scrape_analyze import analyze
from threading import Thread
import datetime

g_time_last_paint = None
g_file_save_path = "./dataexpo/images/"

def paint(file_path, str_time_start, str_time_end, out_file_name, forced=False):
    global g_file_save_path
    global g_time_last_paint
    now = datetime.datetime.now()
    if g_time_last_paint == None or forced or (now - g_time_last_paint).total_seconds()/60 > 2:
        g_time_last_paint = now
        try:
            thread = Thread(target=analyze, args=(file_path, str_time_start, str_time_end, "minute", "hour",
                    g_file_save_path + out_file_name))
            thread.start()
            thread.join()
        except Exception as e:
            print(e)
