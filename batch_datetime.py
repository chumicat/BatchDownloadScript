from datetime import datetime, timedelta
from typing import Iterator, Union
from abc import abstractmethod
import json

DEFAULT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
CONFIG_FILENAME = "config.json"

class BatchDateTime:
    class_keys = []

    def get_dict(self):
        return {key.replace("_{}__".format(self.__class__.__name__), ""): value \
            for key, value in self.__dict__.items()
        }

    def set_dict(self, newdict):
        if not all(class_key in newdict for class_key in self.class_keys) \
            or len(self.class_keys) != len(newdict): raise ValueError("dict key mismatch")
        for class_key in self.__class__.class_keys:
            setattr(self, "_{}__{}".format(self.__class__.__name__, class_key), newdict[class_key])

    def __str__(self) -> str:
        return str(self.get_dict())

    @abstractmethod
    def get_members(self):
        pass

    @staticmethod
    def timedelta_float_selector(variable: Union[timedelta, float, int]) -> float:
        return variable.total_seconds() if isinstance(variable, timedelta) else float(variable)

    @staticmethod
    def datetime_string_selector(variable: Union[datetime, str]) -> str:
        return datetime.strftime(variable, DEFAULT_DATETIME_FORMAT) if isinstance(variable, datetime) else variable

class BatchDateTimeToPast(BatchDateTime):
    class_keys = ["format", "interval", "lookback_period"]

    def __init__(self, format: str = "", interval: Union[timedelta, float, int] = 0, \
            lookback_period: Union[timedelta, float, int] = 0) -> None:
        self.__format = format
        self.__interval = self.timedelta_float_selector(interval)
        self.__lookback_period = self.timedelta_float_selector(lookback_period)

    def get_members(self):
        cur_datetime = datetime.now()
        end_datetime = cur_datetime - timedelta(seconds=self.__lookback_period)
        interval = timedelta(seconds=self.__interval)
        while cur_datetime >= end_datetime:
            yield cur_datetime.strftime(self.__format)
            cur_datetime -= interval

class BatchDateTimeToFuture(BatchDateTime):
    class_keys = ["format", "interval", "lookforward_period"]

    def __init__(self, format: str = "", interval: Union[timedelta, float, int] = 0, \
            lookforward_period: Union[timedelta, float, int] = 0) -> None:
        self.__format = format
        self.__interval = self.timedelta_float_selector(interval)
        self.__lookforward_period = self.timedelta_float_selector(lookforward_period)

    def get_members(self):
        cur_datetime = datetime.now()
        end_datetime = cur_datetime + timedelta(seconds=self.__lookforward_period)
        interval = timedelta(seconds=self.__interval)
        while cur_datetime <= end_datetime:
            yield cur_datetime.strftime(self.__format)
            cur_datetime += interval

class BatchDateTimePeriod(BatchDateTime):
    class_keys = ["format", "interval", "begin_datetime", "end_datetime"]

    def __init__(self, format: str = "", interval: Union[timedelta, float, int] = 0, \
            begin_datetime: Union[datetime, str] = datetime.today(), \
            end_datetime: Union[datetime, str] = datetime.today()) -> None:
        self.__format = format
        self.__interval = self.timedelta_float_selector(interval)
        self.__begin_datetime = self.datetime_string_selector(begin_datetime)
        self.__end_datetime = self.datetime_string_selector(end_datetime)

    def get_members(self):
        cur_datetime = datetime.strptime(self.__begin_datetime, DEFAULT_DATETIME_FORMAT)
        end_datetime = datetime.strptime(self.__end_datetime, DEFAULT_DATETIME_FORMAT)
        interval = timedelta(seconds=self.__interval)
        while cur_datetime <= end_datetime:
            yield cur_datetime.strftime(self.__format)
            cur_datetime += interval

class BatchDateTimes:
    def __init__(self) -> None:
        self.__items = {}

    def __getitem__(self, key) -> BatchDateTime:
        return self.__items[key]

    def __setitem__(self, key, newvalue: BatchDateTime) -> None:
        self.__items[key] = newvalue

    def __get_dict(self) -> dict:
        data_dict = {}
        for key, value in self.__items.items():
            data_dict[key] = value.get_dict()
        return data_dict

    def __str__(self) -> str:
        return str(self.__get_dict())

    def next_idx(self) -> int:
        return max(self.__items.keys()) + 1 if self.__items else 0

    @staticmethod
    def batch_datetime_class_selector_with_dict(newdict: dict) -> BatchDateTime:
        if "lookback_period" in newdict:
            batch_datetime = BatchDateTimeToPast()
        elif "lookforward_period" in newdict:
            batch_datetime = BatchDateTimeToFuture()
        elif "begin_datetime" in newdict:
            batch_datetime = BatchDateTimePeriod()
        else:
            raise ValueError("dict mismatch to BatchDateTime descendant")

        batch_datetime.set_dict(newdict)
        return batch_datetime

    def export_json(self, filepath: str, encoding: str = "utf8") -> None:
        with open(filepath, "w", encoding=encoding) as file:
            json.dump(self.__get_dict(), file, indent=4, sort_keys=False)

    def import_json(self, filepath: str, encoding: str = "utf8") -> None:
        self.__items = {}
        with open(filepath, "r", encoding=encoding) as file:
            for key, value in json.load(file).items():
                self.__items[int(key)] = self.batch_datetime_class_selector_with_dict(value)

    def get_members(self, replace_table: dict = {}) -> Iterator[str]:
        for value in self.__items.values():
            for v in value.get_members():
                for src, dst in replace_table.items():
                    v = v.replace(src, dst)
                yield v
