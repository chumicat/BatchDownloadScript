import urllib.request
import threading
from batch_datetime import BatchDateTimePeriod, BatchDateTimeToFuture, BatchDateTimeToPast, BatchDateTimes
import platform
import re
import sys
from os import path

CONFIG_FILENAME = "config.json"

def download_file(url, file):
    try:
        print("Try Url: {}".format(url))
        urllib.request.urlretrieve(url, file)
        print("File {} Found and Download".format(file))
    except:
        pass

def set_config_as_json(batch_datetimes: BatchDateTimes):
    # Step 1: Select Type
    print("Add new BatchDateTime - Step 1: Select Type")
    print("  (1) Now to Past")
    print("  (2) Now to Future")
    print("  (3) Now to Period")
    ans = input("> ")
    if "1" in ans:
        command = [1, 2, 3]
        batch_datetime_class = BatchDateTimeToPast
    elif "2" in ans:
        command = [1, 2, 4]
        batch_datetime_class = BatchDateTimeToFuture
    elif "3" in ans:
        command = [1, 2, 5, 6]
        batch_datetime_class = BatchDateTimePeriod
    else:
        print("No Select")
        return

    print("Add new BatchDateTime - Step 2: Set Config")
    # Step 2: Set Config
    config_dict = {}
    if 1 in command:
        config_dict["format"] = input("Format: ").replace("%20", " ")
    if 2 in command:
        config_dict["interval"] = float(input("Interval (s): "))
    if 3 in command:
        config_dict["lookback_period"] = float(input("lookback_period (s): "))
    if 4 in command:
        config_dict["lookforward_period"] = float(input("lookforward_period (s): "))
    if 5 in command:
        config_dict["begin_datetime"] = input("begin_datetime (%Y-%m-%d %H:%M:%S.%f): ")
    if 6 in command:
        config_dict["end_datetime"] = input("end_datetime: (%Y-%m-%d %H:%M:%S.%f): ")

    # Step 3: export
    idx = batch_datetimes.next_idx()
    batch_datetimes[idx] = batch_datetime_class()
    batch_datetimes[idx].set_dict(config_dict)
    batch_datetimes.export_json(CONFIG_FILENAME)

if __name__ == "__main__":
    batch_datetimes = BatchDateTimes()
    if path.exists(CONFIG_FILENAME):
        batch_datetimes.import_json(CONFIG_FILENAME)
    else:
        print("Config not exist, Please add a new one")
        set_config_as_json(batch_datetimes)
    
    if len(sys.argv) < 2:
        threads, member_count = [], 0
        replace_dict = {" ": "%20"}
        if platform.system() == "Windows":
            replace_dict["%-d"] = "%#d"
        elif platform.system() == "Linux":
            replace_dict["%#d"] = "%-d"

        for idx, url in enumerate(batch_datetimes.get_members(replace_dict)):
            filename = re.findall(".*/(.*)", url)[0]
            threads.append(threading.Thread(target = download_file, args = (url, filename)))
            threads[idx].start()
            member_count += 1
            
        for idx in range(member_count):
            threads[idx].join()
    elif sys.argv[1] == "config" and sys.argv[2] == "add":
        while(input("Add new config? [n/y]") == "y"):
            set_config_as_json(batch_datetimes)
    elif sys.argv[1] == "config" and sys.argv[2] == "list":
        print(str(batch_datetimes))