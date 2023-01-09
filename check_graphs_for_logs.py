import glob
import os

in_log_folder="./"
out_image_folder="./dataexpo/images/"

def get_image_name(log_name):
    '''
        from: log_2022_12_3.txt
        to: 2022-12-3.png
    '''
    s = log_name.split('.txt')[0]
    s = s.split('_')
    return '-'.join( s[1:4] ) + ".png"


log_files = glob.glob(in_log_folder+"log_*.txt")
for item in log_files:
    exists = os.path.exists( out_image_folder + get_image_name(item) )
    print(item, " --> ", get_image_name(item), "exists:", exists)
