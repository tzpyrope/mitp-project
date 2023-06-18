from datetime import datetime, timedelta

import pandas as pd

from .instruct_and_date_conversion import *


class ReadCsvData:
    def __init__(self, file_path):
        self.__file_path = file_path

    @property
    def file_path(self):
        return self.__file_path

    def read_schedule_csv(self):
        df = pd.read_csv(
            r"%s" % self.__file_path,
            delimiter=",",
            usecols=[
                "Typ",
                "Tytuł",
                "Uwaga",
                "Pierwszy dzień",
                "Ostatni dzień",
                "Ogłoszony początek",
                "Ogłoszony koniec",
                "Miejsce",
            ],
            dtype=None,
        )

        return df


class CsvConversion(ReadCsvData):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.__class_type_list = None
        self.__subject_list = None
        self.__start_days = None
        self.__end_days = None
        self.__start_time = None
        self.__end_time = None
        self.__location = None

    @property
    def class_type_list(self):
        return self.__class_type_list

    @property
    def subject_list(self):
        return self.__subject_list

    @property
    def start_days(self):
        return self.__start_days

    @property
    def end_days(self):
        return self.__end_days

    @property
    def start_time(self):
        return self.__start_time

    @property
    def end_time(self):
        return self.__end_time

    @property
    def location(self):
        return self.__location

    def convert_class_data(self):
        df = self.read_schedule_csv()

        self.__class_type_list = df["Typ"].values.tolist()
        self.__subject_list = df["Tytuł"].values.tolist()
        self.__start_days = df["Pierwszy dzień"].values.tolist()
        self.__end_days = df["Ostatni dzień"].values.tolist()
        self.__start_time = df["Ogłoszony początek"].values.tolist()
        self.__end_time = df["Ogłoszony koniec"].values.tolist()
        self.__location = df["Miejsce"].values.tolist()

    def __account_for_single_day_events(
        self, start_time_end_day: list, end_time_end_day: list, weeks: list
    ):
        start_time_end_day.append("N/A")
        end_time_end_day.append("N/A")
        weeks.append(0)

    def __end_days_datetime_list_conversion(self):
        start_time_end_days = []
        end_time_end_days = []

        weeks = []

        for i in range(len(self.__end_days)):
            if (
                pd.isna(self.__end_days[i])
                or self.__end_days[i] == self.__start_days[i]
            ):
                self.__account_for_single_day_events(
                    start_time_end_days, end_time_end_days, weeks
                )
            else:
                end_day = datetime.strptime(self.__end_days[i], "%d.%m.%Y")
                start_day = datetime.strptime(self.__start_days[i], "%d.%m.%Y")
                week_count = (abs(end_day - start_day).days) // 7
                weeks.append(week_count)

                start_time_end_days.append([])
                end_time_end_days.append([])

                for number in range(0, (week_count + 1)):
                    date = start_day + timedelta(weeks=number)
                    date = datetime.strftime(date, "%d.%m.%Y")
                    date_begin = date + " " + self.__start_time[i]
                    date_end = date + " " + self.__end_time[i]
                    date_begin = datetime.strptime(date_begin, "%d.%m.%Y %H:%M")
                    date_end = datetime.strptime(date_end, "%d.%m.%Y %H:%M")
                    start_time_end_days[i].append(date_begin)
                    end_time_end_days[i].append(date_end)

        return start_time_end_days, end_time_end_days

    def __start_days_datetime_list_conversion(self):
        start_time_start_days = []
        end_time_start_days = []

        append_hour(self.__start_days, self.__start_time, start_time_start_days)
        append_hour(self.__start_days, self.__end_time, end_time_start_days)

        datetime_list_conversion(start_time_start_days)
        datetime_list_conversion(end_time_start_days)

        return start_time_start_days, end_time_start_days

    def __final_start_times_list_conversion(self):
        self.convert_class_data()

        full_start = []

        start_days_list = self.__start_days_datetime_list_conversion()
        (start_time_start_days, end_time_start_days) = start_days_list
        end_days_list = self.__end_days_datetime_list_conversion()
        (start_time_end_days, end_time_end_days) = end_days_list

        for i in range(len(end_time_start_days)):
            if end_time_end_days[i] == "N/A":
                full_start.append([start_time_start_days[i]])
            else:
                full_start.append(start_time_end_days[i])

        return full_start

    def __final_end_times_list_conversion(self):
        self.convert_class_data()

        full_end = []

        start_days_list = self.__start_days_datetime_list_conversion()
        (start_time_start_days, end_time_start_days) = start_days_list
        end_days_list = self.__end_days_datetime_list_conversion()
        (start_time_end_days, end_time_end_days) = end_days_list

        for i in range(len(end_time_start_days)):
            if end_time_end_days[i] == "N/A":
                full_end.append([end_time_start_days[i]])
            else:
                full_end.append(end_time_end_days[i])

        return full_end

    def get_class_start_times(self) -> list:
        full_start = self.__final_start_times_list_conversion()
        return full_start

    def get_class_end_times(self) -> list:
        full_end = self.__final_end_times_list_conversion()
        return full_end
