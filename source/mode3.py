from operator import itemgetter

import pandas as pd
from tabulate import tabulate

from .dates_conversion.instruct_and_date_conversion import *
from .mode_schema import Mode


class Mode3(Mode):
    def __init__(self, csv_handler):
        super().__init__(csv_handler)

    def __check_if_3_input_is_correct(self, user_input: str):
        while True:
            try:
                if user_input != "jutro" and user_input != "dzisiaj":
                    datetime.strptime(user_input, "%d/%m/%Y")
                break
            except ValueError:
                print("\nWprowadź datę w odpowiednim formacie.\n")
                user_input = input()

        return user_input

    def __option_3_user_input(self):
        user_input = input(
            f'\nPodaj datę (format: dd/mm/yyyy).\
                    \nPrzykład: {current_date_str}\
                    \nLub wpisz "dzisiaj" albo "jutro".\n\n'
        )

        user_date = self.__check_if_3_input_is_correct(user_input)

        return user_date

    def __user_date_adjustment(self, user_date: str):
        # jeśli użytkownik chce bazować na obecnej/jutrzejszej dacie
        if user_date == "jutro":
            user_date = current_time + timedelta(days=1)
        elif user_date == "dzisiaj":
            user_date = current_time
        else:
            user_date = datetime.strptime(user_date, "%d/%m/%Y")

        return user_date

    def __group_class_found_for_specified_day(self):
        user_date = self.__user_date_adjustment(self.__option_3_user_input())

        # inicjalizacja potrzebnych list
        class_all = []
        class_type = []
        classes_start = []
        classes_end = []
        subject_name = []
        location_name = []
        busy = False

        # szukanie dat/godzin zajęć dla sprecyzowanego dnia
        for i in range(len(self.subject_list)):
            for j in range(len(self.full_start[i])):
                if user_date.date() == self.full_start[i][j].date():
                    busy = True  # w podanym dniu są zajęcia

                    # tworzenie wielowymiarowej listy i list z informacjami o zajęciach
                    class_all.append([])
                    subject_name.append(self.subject_list[i])

                    if pd.isna(self.class_type_list[i]):
                        class_type.append("")
                    else:
                        class_type.append(self.class_type_list[i])

                    if pd.isna(self.location[i]):
                        location_name.append("")
                    else:
                        location_name.append(self.location[i])

                    classes_start.append(self.full_start[i][j])
                    classes_end.append(self.full_end[i][j])

        # dodawanie informacji o poszczególnych zajęciach do wewnętrznych list
        # w formacie [nazwa przedmiotu, forma zajęć etc] żeby łatwo zrobić z całości tabelkę
        for i in range(len(class_all)):
            class_all[i].append(subject_name[i])
            class_all[i].append(class_type[i])
            class_all[i].append(location_name[i])
            class_all[i].append(classes_start[i])
            class_all[i].append(classes_end[i])

        sorted_class_all = sorted(class_all, key=itemgetter(3))

        return sorted_class_all, busy

    def __format_datetime_to_string_for_hours(self, class_list: list):
        # konwersja datetime na str by pokazywał tylko godziny i minuty
        for i in range(len(class_list)):
            class_list[i][3] = "{:d}:{:02d}".format(
                class_list[i][3].hour, class_list[i][3].minute
            )
            class_list[i][4] = "{:d}:{:02d}".format(
                class_list[i][4].hour, class_list[i][4].minute
            )

    def __make_a_schedule_table_for_given_day(self, class_list: list):
        table = [
            [
                "Przedmiot",
                "Forma zajęć",
                "Miejsce",
                "Godzina rozpoczęcia",
                "Godzina zakończenia",
            ]
        ]

        for i in range(len(class_list)):
            table.append(class_list[i])

        print("")
        print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))
        print("\n")

    def run_mode(self):
        class_busy = self.__group_class_found_for_specified_day()
        (class_list, busy) = class_busy

        if busy:  # jeśli są zajęcia, tworzymy tabelkę
            self.__format_datetime_to_string_for_hours(class_list)
            self.__make_a_schedule_table_for_given_day(class_list)
        else:
            print("\nNie masz wtedy zajęć.\n\n")
