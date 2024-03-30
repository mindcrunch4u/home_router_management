import glob
import os
import sys
import datetime

# Description Use this script to regenerate plots using log*.txt from the current folder.


def usage():
    print("python3 regenerate.py <input logs folder> <output images folder> [overwrite]")
    print("\tExample: python3 regenerate.py ./ ./newimgs/")
    print('\tIf the keyword "overwrite" is added to the end of the command, then the script overwrites the images regardless if they already exist or not.')


def get_image_name(log_name):
    '''
        from: log_2022_12_3.txt
        to: 2022-12-3.png
    '''
    s = log_name.split('.txt')[0]
    s = s.split('_')
    return '-'.join( s[1:4] ) + ".png"


def file_name_to_date(file_name):
    file_name = file_name.split('.')[0]
    datetime_object = datetime.datetime.strptime(file_name, '%Y-%m-%d')
    return datetime_object


def main(in_log_folder, out_image_folder, force_reload=False):
    log_files = glob.glob(in_log_folder+"log_*.txt")
    for item in log_files:
        file_name = get_image_name(item)
        out_path  = out_image_folder + file_name
        from_date = file_name_to_date(file_name)
        to_date   = file_name_to_date(file_name) + datetime.timedelta(days=1)

        exists = os.path.exists( out_path )
        if exists and not force_reload:
            print(item, " --> ", out_image_folder + file_name, "exists:", exists)
        else:
            cmd = "/usr/bin/python3.9  scrape_analyze_fine.py" + " " + item + " " + from_date.strftime("%Y.%m.%d") + " " + to_date.strftime("%Y.%m.%d") + " " + out_path
            print("[Gen] " + cmd)
            os.system(cmd)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(sys.argv)
        usage()
        sys.exit(1)
    else:
        in_log_folder = sys.argv[1]
        out_image_folder= sys.argv[2]
        force_reload = False
        if len(sys.argv) == 4:
            if sys.argv[-1] == "overwrite":
                force_reload = True
            else:
                force_reload = False
        main(in_log_folder, out_image_folder, force_reload)
