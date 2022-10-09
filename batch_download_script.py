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

if __name__ == "__main__":
    batch_datetimes = BatchDateTimes()
    if path.exists(CONFIG_FILENAME):
        batch_datetimes.import_json(CONFIG_FILENAME)
    else:
        print("Config not exist, Please add a new one")
        batch_datetimes.add_config_interactive()
        batch_datetimes.export_json(CONFIG_FILENAME)

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
        batch_datetimes.add_config_interactive()
        batch_datetimes.export_json(CONFIG_FILENAME)
    elif sys.argv[1] == "config" and sys.argv[2] == "list":
        batch_datetimes.list_config()
    elif sys.argv[1] == "config" and sys.argv[2] == "remove":
        batch_datetimes.remove_config_interactive()
        batch_datetimes.export_json(CONFIG_FILENAME)
    else:
        print("`batch_download_script.py` to downlaod with config")
        print("`batch_download_script.py config list`   to list item")
        print("`batch_download_script.py config add`    to add new item")
        print("`batch_download_script.py config remove` to remove item")