from operator import itemgetter

from .dates_conversion.instruct_and_date_conversion import *
from .mode_schema import Mode


class Mode6(Mode):
    def __init__(self, csv_handler):
        super().__init__(csv_handler)

    def __check_if_user_input_day_is_correct(self, user_input: str):
        while True:
            try:
                datetime.strptime(user_input, "%d/%m/%Y")
                break
            except ValueError:
                print("\nWprowadź datę w odpowiednim formacie.\n")
                user_input = input()

        return user_input

    def __option_6_user_input_day(self):
        print(
            f"\nPodaj dzień, który chcesz sprawdzić (format dd/mm/yyyy).\
            \nPrzykład: {current_date_str}.\n"
        )
        user_input = input()

        user_day = self.__check_if_user_input_day_is_correct(user_input)

        return user_day

    def __check_if_user_input_hours_is_correct(self, user_input: str):
        while True:
            try:
                hours_split = user_input.split(" - ")
                list(map(lambda hour: datetime.strptime(hour, "%H:%M"), hours_split))
                break
            except ValueError:
                print("\nWprowadź godziny w odpowiednim formacie.\n")
                user_input = input()

        return user_input

    def __option_6_user_input_hours(self):
        print(
            '\nPodaj przedział godzinowy (jeśli chcesz zobaczyć wolne sloty dla całego dnia, napisz "brak").\
                \nPrzykład: 12:30 - 16:00\n'
        )
        user_input = input()

        if user_input != "brak":
            user_hours = self.__check_if_user_input_hours_is_correct(user_input)
        else:
            user_hours = user_input

        return user_hours

    def __convert_user_hours_to_datetime(self, day: str, hours: str):
        user_hours_list = hours.split(" - ")

        for i in range(len(user_hours_list)):
            user_hours_list[i] = day + " " + user_hours_list[i]
            user_hours_list[i] = datetime.strptime(user_hours_list[i], "%d/%m/%Y %H:%M")

        return user_hours_list

    def __search_for_classes_between_specified_dates(self, dates: list):
        busy_time = []
        flag = 0

        for i in range(len(self.full_start)):
            for j in range(len(self.full_start[i])):
                if dates[0] - timedelta(hours=2, minutes=15) <= self.full_start[i][
                    j
                ] < dates[1] and dates[0] < self.full_end[i][j] <= dates[1] + timedelta(
                    hours=2, minutes=15
                ):
                    busy_time.append([])

                    busy_time[flag].append(self.full_start[i][j])
                    busy_time[flag].append(self.full_end[i][j])

                    flag += 1

        sorted_busy_time = sorted(busy_time, key=itemgetter(0))

        return sorted_busy_time

    def __search_for_empty_slots_if_hours_specified(self, dates: list, busy_time: list):
        busy_time_len = len(busy_time) - 1

        empty_slots = []
        flag = 0

        for i in range(len(busy_time)):
            if i == 0 and busy_time_len == i:
                if busy_time[i][0] > dates[0]:
                    empty_slots.append([])

                    empty_slots[flag].append(dates[0])
                    empty_slots[flag].append(busy_time[i][0])

                if busy_time[i][1] < dates[1]:
                    empty_slots.append([])

                    empty_slots[flag].append(busy_time[i][1])
                    empty_slots[flag].append(dates[1])

            else:
                if i == busy_time_len:
                    if busy_time[i][0] not in empty_slots[flag - 1]:
                        empty_slots.append([])

                        empty_slots[flag].append(busy_time[i - 1][1])
                        empty_slots[flag].append(busy_time[i][0])

                    if dates[1] >= busy_time[i][1]:
                        empty_slots.append([])

                        empty_slots[flag].append(busy_time[i][1])
                        empty_slots[flag].append(dates[1])

                elif busy_time[i][0] > dates[0] and i == 0:
                    empty_slots.append([])

                    empty_slots[flag].append(dates[0])
                    empty_slots[flag].append(busy_time[i][0])

                    flag += 1

                    empty_slots.append([])

                    empty_slots[flag].append(busy_time[i][1])
                    empty_slots[flag].append(busy_time[i + 1][0])

                else:
                    empty_slots.append([])

                    empty_slots[flag].append(busy_time[i][1])
                    empty_slots[flag].append(busy_time[i + 1][0])

                flag += 1

        sorted_empty_slots = sorted(empty_slots, key=itemgetter(0))

        if sorted_empty_slots[len(sorted_empty_slots) - 1][0] == sorted_empty_slots[len(sorted_empty_slots) - 1][1]:
            del sorted_empty_slots[len(sorted_empty_slots) - 1]

        return sorted_empty_slots

    def __convert_user_day_to_datetime(self, day: str):
        day = datetime.strptime(day, "%d/%m/%Y")

        return day

    def __search_for_classes_for_date(self, day: str):
        busy_time = []
        flag = 0

        for i in range(len(self.full_start)):
            for j in range(len(self.full_start[i])):
                if self.full_start[i][j].date() == day.date():
                    busy_time.append([])

                    busy_time[flag].append(self.full_start[i][j])
                    busy_time[flag].append(self.full_end[i][j])

                    flag += 1

        sorted_busy_time = sorted(busy_time, key=itemgetter(0))

        return sorted_busy_time

    def __search_for_empty_slots_if_hours_not_specified(
        self, day: datetime, busy_time: list
    ):
        busy_time_len = len(busy_time) - 1

        empty_slots = []
        flag = 0

        for i in range(len(busy_time)):
            if i == 0:
                empty_slots.append([])

                empty_slots[flag].append(day)
                empty_slots[flag].append(busy_time[i][0])

                if busy_time_len >= 1:
                    flag += 1

                    empty_slots.append([])

                    empty_slots[flag].append(busy_time[i][1])
                    empty_slots[flag].append(busy_time[i + 1][0])

            elif i == busy_time_len:
                empty_slots.append([])

                empty_slots[flag].append(busy_time[i][1])
                empty_slots[flag].append(day + timedelta(days=1))

            else:
                empty_slots.append([])

                empty_slots[flag].append(busy_time[i][1])
                empty_slots[flag].append(busy_time[i + 1][0])

            flag += 1

        sorted_empty_slots = sorted(empty_slots, key=itemgetter(0))

        return sorted_empty_slots

    def __user_chose_to_specify_hours(self, day: str, hours: str):
        dates_list = self.__convert_user_hours_to_datetime(day, hours)
        busy_time = self.__search_for_classes_between_specified_dates(dates_list)
        empty_slots = self.__search_for_empty_slots_if_hours_specified(
            dates_list, busy_time
        )

        return empty_slots

    def __user_chose_not_to_specify_hours(self, day: str):
        day_datetime = self.__convert_user_day_to_datetime(day)
        busy_time = self.__search_for_classes_for_date(day_datetime)
        empty_slots = self.__search_for_empty_slots_if_hours_not_specified(
            day_datetime, busy_time
        )

        return empty_slots

    def __print_empty_slots(self, empty_slots):
        for i in range(len(empty_slots)):
            for j in range(len(empty_slots[i])):
                empty_slots[i][j] = "{:d}:{:02d}".format(
                    empty_slots[i][j].hour, empty_slots[i][j].minute
                )

            print(f"{empty_slots[i][0]} - {empty_slots[i][1]}")

        print("\n")

    def run_mode(self):
        user_day = self.__option_6_user_input_day()
        user_hours = self.__option_6_user_input_hours()

        if user_hours != "brak":
            empty_slots = self.__user_chose_to_specify_hours(user_day, user_hours)

            print(f"\nWolne sloty na dzień {user_day} w godzinach {user_hours}:")
        else:
            empty_slots = self.__user_chose_not_to_specify_hours(user_day)

            print(f"\nWolne sloty na dzień {user_day}:")

        self.__print_empty_slots(empty_slots)
