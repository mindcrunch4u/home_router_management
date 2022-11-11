import time
import os
import sys
import subprocess
from pythonping import ping

gSleepTime = 2 # 30 -- wlan0, 2 -- eth0
gSleepLong = 120
gSleepShort = 2
gSleepImmediate = 0

gPingTimeout = 1

gCableName = "eth0"
gWirelessName = "CMCC-Oxj9"
gMainInterface = gCableName

def is_cable_plugged_in():
    status_check = subprocess.check_output(['ip','a'])
    status_check = status_check.decode().split(os.linesep)
    lineIndex = 0
    for line in status_check:
        if gCableName in line:
            if 'inet' in status_check[lineIndex+1] or 'inet' in status_check[lineIndex+2]:
                return True
        lineIndex += 1
    return False

def reload_interfaces():
    subprocess.run(['nmcli','c','down', gCableName])
    subprocess.run(['nmcli','c','down', gWirelessName])
    subprocess.run(['nmcli','c','up', gCableName])
    subprocess.run(['nmcli','c','up', gWirelessName])
    subprocess.run(['systemctl','restart','wg-quick@wg0'])

def eth0_flows_up(this_sleep_time = 2):
    global gMainInterface
    global gSleepTime
    gSleepTime = this_sleep_time
    gMainInterface = gCableName
    status_check = subprocess.check_output(['nmcli','c'])
    status_check = status_check.decode()
    if status_check.split(os.linesep)[1].split(' ')[0] == gCableName:
        print(".", end='', flush=True)
        return
    else:
        print("[+] execute switch: " + gCableName, flush=True)
    os.system("nmcli con modify eth0 ipv4.route-metric 10")
    os.system("nmcli con modify CMCC-Oxj9 ipv4.route-metric 600")
    reload_interfaces()
 
def wlan0_flows_up(this_sleep_time = 2):
    global gMainInterface
    global gSleepTime
    gSleepTime = this_sleep_time
    gMainInterface = gWirelessName
    status_check = subprocess.check_output(['nmcli','c'])
    status_check = status_check.decode()
    if status_check.split(os.linesep)[1].split(' ')[0] == gWirelessName:
        print(".", end='', flush=True)
        return
    else:
        print("[+] execute switch: " + gWirelessName, flush=True)
    os.system("nmcli con modify eth0 ipv4.route-metric 600")
    os.system("nmcli con modify CMCC-Oxj9 ipv4.route-metric 10")
    reload_interfaces()

def ping_public_net():
    try:
        for item in ping("baidu.com", count=1, timeout=gPingTimeout):
            if item.success == False:
                return 1
        return 0 #ok
    except:
        return 1 #error
 
def main():
    global gSleepTime
    global gMainInterface
    global gCableName
    global gWirelessName

    countTestCable = 15
    while True:
        ping_result = ping_public_net()
        if ping_result != 0:
            if gMainInterface == gCableName or (not is_cable_plugged_in()):
                print("reason 1, cable plugged: " + str(is_cable_plugged_in()), flush=True)
                wlan0_flows_up()
            else:
                print("reason 2", flush=True)
                eth0_flows_up()
        else:
            if gMainInterface == gCableName:
                print("reason 3", flush=True)
                eth0_flows_up()
            else:
                if is_cable_plugged_in():
                    countTestCable = countTestCable -1
                    if countTestCable <= 0:
                        # every 15 times using wlan0, check if cable is connected
                        # i.e. favour cable over wlan0
                        print("[~] attempting to favour: " + gCableName, flush=True)
                        gMainInterface = gCableName
                        countTestCable = 15
                        continue
                print("reason 4", flush=True)
                wlan0_flows_up(this_sleep_time=gSleepLong)
        time.sleep(gSleepTime)

if __name__ == '__main__':
    main()
