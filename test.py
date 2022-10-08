from datetime import datetime, timedelta
from batch_datetime import BatchDateTimeToPast, BatchDateTimeToFuture, BatchDateTimePeriod
from batch_datetime import BatchDateTimes
import batch_datetime
import json


if __name__ == "__main__":
    items = BatchDateTimes()
    items[0] = BatchDateTimeToPast("%Y-%b-%d.gif", timedelta(days=1), timedelta(weeks=2))
    items[1] = BatchDateTimeToFuture("%Y-%b-%d.gif", timedelta(days=5), timedelta(days=100))
    items[2] = BatchDateTimePeriod("%Y-%b-%d.gif", timedelta(days=1).total_seconds(), \
                                   datetime.strptime("2022-08-25", "%Y-%m-%d"), \
                                   datetime.strptime("2022-10-07", "%Y-%m-%d"))
    items.export_json(batch_datetime.CONFIG_FILENAME)
    print(items[0], items[1], items[2])
    print(type(items), type(items[0]), type(items[1]), type(items[2]))
    print(items)
    print("")

    items = BatchDateTimes()
    items.import_json(batch_datetime.CONFIG_FILENAME)
    print(items[0], items[1], items[2])
    print(type(items), type(items[0]), type(items[1]), type(items[2]))
    print(items)
    print("")

    print([x for x in items.get_members()])

    dd = datetime.strptime("2022-10-07", "%Y-%m-%d")
    print(dd)
    print(type(dd))
    ds = datetime.strftime(dd, batch_datetime.DEFAULT_DATETIME_FORMAT)
    print(ds)
