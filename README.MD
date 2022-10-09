## Batch Download Script Usage
### Introudction
batch_download_script is used to try to download a bunch of files from internet, which url have datetime as variable.
For Example: Try download file from url  "http://example.com/Log %Y-%m-%d.txt" from 2022/08/16 to 2022/08/21, which means:
- Try download from http://example.com/Log%202022-08-16.txt
- Try download from http://example.com/Log%202022-08-17.txt
- Try download from http://example.com/Log%202022-08-18.txt
- Try download from http://example.com/Log%202022-08-19.txt
- Try download from http://example.com/Log%202022-08-20.txt
- Try download from http://example.com/Log%202022-08-21.txt

### Usage - config.json
We will create config.json as script configuration, Refer to [FORMAT CODE REFERENCE](https://www.geeksforgeeks.org/python-datetime-strptime-function/) to plan your format string.

An Example config.json are as following, which means:
- index 0: Download target from now to one month ago
- index 1: Donwload target from now to one month later
- index 2: Download target from 2022/08/16 to 2022/06/21

```
{
    "0": {
        "format": "http://example.com/Log %Y-%m-%d.txt",
        "interval": 86400.0,
        "lookback_period": 2592000.0
    },
    "1": {
        "format": "http://example.com/Log %Y-%m-%d.txt",
        "interval": 86400.0,
        "lookforward_period": 2592000.0
    },
    "2": {
        "format": "http://example.com/Log %Y-%m-%d.txt",
        "interval": 86400.0,
        "begin_datetime": "2022-08-16 00:00:00.000000",
        "end_datetime": "2022-08-21 00:00:00.000000"
    },
}
```

You can also use follow command to set configuration file interactively:
```
python batch_download_script.py config list
python batch_download_script.py config add
python batch_download_script.py config remove
```

### Usage - Run Script
Run the python script directly to download with config.json
```
python batch_download_script.py
```

## Batch DateTime Usage
### Introduction
batch_datetime module is used to get a period of string that have datetime as variable.
For Example: Get string of "%Y-%m-%d.txt" from 2022/08/16 to 2022/08/21, which means:
- 2022-08-16.txt
- 2022-08-17.txt
- 2022-08-18.txt
- 2022-08-19.txt
- 2022-08-20.txt
- 2022-08-21.txt

### Main Module
batch_datetime module have three main type of class
- BatchDateTimeToPast(format, interval, lookback_period) is used to get datetime from current time to past
- BatchDateTimeToFuture(format, interval, lookforward_period) is used to get datetime from current time to future
- BatchDateTimeToFuture(format, interval, begin_datetime, end_datettime) is used to get datetime from current time to future
All these three class are descendants of BatchDateTime class.

Variable meaning are as following:
- format is format of output string, [FORMAT CODE REFERENCE](https://www.geeksforgeeks.org/python-datetime-strptime-function/)
- interval is time (in second) that between two printed datetime. For Example, 86400 means printed string will have 1 day-long blank
- lookback_period is farest time (in second) that we will trace in past. For Example, 604800 means we will keep print string until 1 week-long in past.
- lookforward_period is farest time (in second) that we will trace to future. For Example, 604800 means we will keep print string until 1 week-long in future.
- begin_datetime is the start time of period datetime. begin_datetime should always before end_datetime
- end_datetime is the end time of period datetime

### Usage
batch_datetime module use class BatchDateTimes as a easy way to access and control a bunch of BatchDateTime
Run example_01.py and check example_01.py to check how configuration consist

```python
# example_0.py
from batch_datetime import BatchDateTimeToPast, BatchDateTimeToFuture, BatchDateTimePeriod, BatchDateTimes
from datetime import datetime, timedelta

# Several ways to add BatchDateTime member to BatchDateTimes
batch_datetimes = BatchDateTimes()
batch_datetimes[0] = BatchDateTimeToPast("%Y-%m-%d", 86400, 2592000)
batch_datetimes[1] = BatchDateTimeToPast("%Y-%m-%d", timedelta(days=1), timedelta(days=30))
batch_datetimes.add_config_with_dict({"format": "%Y-%m-%d", "interval": 86400, "lookback_period": 2592000})
batch_datetimes[3] = BatchDateTimeToFuture("%Y-%m-%d", 86400, 2592000)
batch_datetimes[4] = BatchDateTimeToFuture("%Y-%m-%d", timedelta(days=1), timedelta(days=30))
batch_datetimes.add_config_with_dict({"format": "%Y-%m-%d", "interval": 86400, "lookforward_period": 2592000})
batch_datetimes[6] = BatchDateTimePeriod("%Y-%m-%d", 86400, "2022-10-09 14:23:50.523000", "2022-10-16 14:23:50.523000")
batch_datetimes[7] = BatchDateTimePeriod("%Y-%m-%d", timedelta(days=1), datetime.strptime("2022-10-09", "%Y-%m-%d"), datetime.strptime("2022-10-09", "%Y-%m-%d"))
batch_datetimes.add_config_with_dict({"format": "%Y-%m-%d", "interval": 86400, "begin_datetime": "2022-10-09 14:23:50.523000", "end_datetime": "2022-10-16 14:23:50.523000"})

# Showing configuration
batch_datetimes.list_config()
print(list(batch_datetimes.get_members()))

# Export and import Configuration
batch_datetimes.export_json("a.json")
batch_datetimes.import_json("a.json")

# Showing configuration again
batch_datetimes.list_config()
print(list(batch_datetimes.get_members()))
```


