from flask import Flask
from flask import render_template
import glob
import os
import time
import base64

app = Flask(__name__)
log_file_path = "../log*.txt"
img_file_path = "./images/"

def get_b64_image_from(path):
    b64str = None
    try:
        with open(path, "rb") as img_file:
            b64str = base64.b64encode(img_file.read())
            b64str = b64str.decode()
    except:
        return None
    return b64str

def get_b64_image_name(log_path):
    log_path = os.path.basename(log_path)
    img_path = None
    try:
        img_path = "-".join([log_path.split("_")[1], log_path.split("_")[2], log_path.split("_")[3]]) + ".png"
        img_path = img_path.replace(".txt", "")
    except:
        print("faulty log path: ", log_path)
        return None
    return img_path

def get_items_from(path):
    ret = list()
    files = glob.glob(path)
    files = sorted(files, key = lambda x: os.path.getmtime(os.path.abspath(x)), reverse=True)
    for item in files:
        tmp_dict = dict()
        log_path = os.path.abspath(item) #log file
        img_path = get_b64_image_name(log_path) #img name
        img_path = img_file_path + str(img_path)

        tmp_dict["name"]  = os.path.basename(log_path)
        tmp_dict["image"] = get_b64_image_from(img_path)
        ret.append(tmp_dict)
    return ret

@app.route('/')
def hello_world():
    items = get_items_from(log_file_path)
    return render_template(
            "home.html",
            title="Graph Viewer",
            description="select a date",
            articles= items
            )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)
