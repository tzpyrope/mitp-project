import pandas as pd
from ..variables import *

from .mode_functions import *
from .mode_schema import Mode


class Mode7(Mode):
    def __init__(self, csv_handler):
        super().__init__(csv_handler)

    def __option_7_user_input(self):
        print(
            f"\nPodaj przedział czasowy, który chcesz sprawdzić (format dd/mm/yyyy).\
                \nJeśli interesuje cię konkretny dzień, wpisz jedną datę.\
                \nPrzykład: {current_date_str}\
                \nJeśli interesuje cię przedział pomiędzy dwoma datami, wpisz obie.\
                \nPrzykład: {current_date_str} - {tomorrow_time_str}\n"
        )

        user_input = input()

        return user_input

    def __check_if_7_input_is_correct_for_multiple_dates(self, user_input: str):
        while True:
            try:
                user_dates = user_input.split(" - ")
                user_dates = list(
                    map(lambda date: datetime.strptime(date, "%d/%m/%Y"), user_dates)
                )
                break
            except ValueError:
                print("\nWprowadź datę w odpowiednim formacie.\n")
                user_input = input()

        return user_dates

    def __check_if_7_input_is_correct_for_single_date(self, user_input: str):
        while True:
            try:
                user_date = datetime.strptime(user_input, "%d/%m/%Y")
                break
            except ValueError:
                print("\nWprowadź datę w odpowiednim formacie.\n")
                user_input = input()

        return user_date

    def __find_classes_for_multiple_dates(
        self, user_dates: list, classes: dict, class_types: dict, start_times: list, end_times: list
    ):
        for i in range(len(self.full_start)):
            for j in range(len(self.full_start[i])):
                if (
                    user_dates[1].date()
                    >= self.full_start[i][j].date()
                    >= user_dates[0].date()
                ):
                    classes.append(self.subject_list[i])
                    class_types.append(self.class_type_list[i])
                    start_times.append(self.full_start[i][j])
                    end_times.append(self.full_end[i][j])

    def __find_classes_for_one_date(
        self, user_date: list, classes: dict, class_types: dict, start_times: list, end_times: list
    ):
        for i in range(len(self.full_start)):
            for j in range(len(self.full_start[i])):
                if self.full_start[i][j].date() == user_date.date():
                    classes.append(self.subject_list[i])
                    class_types.append(self.class_type_list[i])
                    start_times.append(self.full_start[i][j])
                    end_times.append(self.full_end[i][j])

    def __get_class_info(self):
        user_date = self.__option_7_user_input()
        classes = []
        class_types = []
        start_times = []
        end_times = []

        if "-" in user_date:
            user_date = self.__check_if_7_input_is_correct_for_multiple_dates(user_date)
            self.__find_classes_for_multiple_dates(user_date, classes, class_types, start_times, end_times)
        else:
            user_date = self.__check_if_7_input_is_correct_for_single_date(user_date)
            self.__find_classes_for_one_date(user_date, classes, class_types, start_times, end_times)

        num_of_classes = len(classes)

        return classes, class_types, num_of_classes, start_times, end_times

    def __get_gramatically_correct_str(self, num: int):
        if num == 1:
            event_string = "wydarzenie"
            plan_string = "zaplanowane"
        elif num in range(2, 5):
            event_string = "wydarzenia"
            plan_string = "zaplanowane"
        else:
            event_string = "wydarzeń"
            plan_string = "zaplanowanych"

        return plan_string, event_string

    def run_mode(self):
        class_info = self.__get_class_info()
        (class_list, type_list, num_of_classes, start_times, end_times) = class_info
        strings = self.__get_gramatically_correct_str(num_of_classes)
        (plan, event) = strings

        start_times, end_times, class_list, type_list = zip(*sorted(zip(start_times, end_times, class_list, type_list)))

        start_dates = list(map(lambda date: datetime.strftime(date, "%d/%m/%Y"), start_times))

        start_hours = list(map(lambda date: datetime.strftime(date, "%H:%M"), start_times))
        end_hours = list(map(lambda date: datetime.strftime(date, "%H:%M"), end_times))

        print(f"\nW tym okresie masz {num_of_classes} {plan} {event}:\n")

        for i in range(len(class_list)):
            if pd.isna(type_list[i]):
                print(f"{class_list[i]} dnia {start_dates[i]} od {start_hours[i]} do {end_hours[i]}")
            else:
                print(f"{class_list[i]} ({type_list[i]}) dnia {start_dates[i]} od {start_hours[i]} do {end_hours[i]}")
        print("\n")
