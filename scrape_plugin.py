from scrape_analyze import analyze, clear_globals
from threading import Thread
import datetime

g_time_last_paint = None
g_file_save_path = "/root/scripts/dataexpo/images/"

def paint(file_path, str_time_start, str_time_end, out_file_name, forced=False):
    global g_file_save_path
    global g_time_last_paint
    clear_globals()
    now = datetime.datetime.now()
    # paint every 30 minutes
    if g_time_last_paint == None or forced or (now - g_time_last_paint).total_seconds()/60 > 30:
        print("From: " + str_time_start + ", To: " + str_time_end + ", Forced: " + str(forced))
        g_time_last_paint = now
        try:
            thread = Thread(target=analyze, args=(file_path, str_time_start, str_time_end, "minute", "hour",
                    g_file_save_path + out_file_name))
            thread.start()
            thread.join()
        except Exception as e:
            print(e)
