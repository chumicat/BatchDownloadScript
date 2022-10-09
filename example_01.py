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