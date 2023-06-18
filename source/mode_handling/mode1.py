import pandas as pd
from ..variables import *

from .mode_functions import *
from .mode_schema import Mode


class Mode1(Mode):
    def __init__(self, csv_handler):
        super().__init__(csv_handler)

    def __check_if_user_input_is_correct_format(self, user_input: str):
        while True:
            try:
                if user_input != "teraz":
                    datetime.strptime(user_input, "%d/%m/%Y %H:%M")
                break
            except ValueError:
                print("\nWprowadź datę w odpowiednim formacie.\n")
                user_input = input()

        return user_input

    def __option_1_user_input(self):
        user_input = input(
            f'\nPodaj datę i godzinę w następującym formacie:\ndd/mm/yyyy hours:minutes\nPrzykład: {current_time_str}\
                                        \nLub wpisz "teraz", jeśli interesuje cię obecna data.\n\n'
        )

        user_date = self.__check_if_user_input_is_correct_format(user_input)

        return user_date

    def __check_if_during_datetime_there_is_event(self, datetime_date: datetime):
        busy = 0

        for i in range(len(self.start_days)):
            for j in range(len(self.full_start[i])):
                if (datetime_date <= self.full_end[i][j]) and (
                    datetime_date >= self.full_start[i][j]
                ):
                    busy = 1

                    subject_name = self.subject_list[i]

                    if pd.isna(self.location[i]):
                        location_name = ""
                    else:
                        location_name = f" w {self.location[i]}"

                    if pd.isna(self.class_type_list[i]):
                        class_type_name = ""
                    else:
                        class_type_name = f", {self.class_type_list[i]}"

                    hours_left = datediff_to_h_min(self.full_end[i][j], datetime_date)

        if busy:
            return [subject_name, class_type_name, location_name, hours_left]
        else:
            return []

    def __search_through_rest_of_day(self, datetime_date: datetime):
        possible_next_class = []
        for i in range(1, 21):
            time_diff = datetime_date + timedelta(hours=i)
            possible_next_class.append(time_diff)
            if time_diff > datetime_date.replace(hour=20):
                break

        return possible_next_class

    def __if_next_class_found(self, busy: bool, next_class, datetime_date: datetime):
        if busy:
            hours_until = datediff_to_h_min(next_class, datetime_date)
            next_class_hour = "{:d}:{:02d}".format(next_class.hour, next_class.minute)
            next_class_str = f"Następne najbliższe wydarzenie tego dnia jest o godzinie {next_class_hour}, {hours_until} od podanej godziny."
        else:
            next_class_str = (
                "Po podanej godzinie nie masz żadnych zaplanowanych wydarzeń tego dnia."
            )

        return next_class_str

    def __find_next_class_if_no_class_when_specified(self, datetime_date: datetime):
        busy = False  # inicjalizacja zmiennej, która określa czy osoba będzie miała zajęcia po danej godzinie w określonym dniu
        next_class = ""

        possible_next_class = self.__search_through_rest_of_day(datetime_date)

        for date in possible_next_class:
            for i in range(len(self.start_days)):
                for j in range(len(self.full_start[i])):
                    if (date <= self.full_end[i][j]) and (
                        date >= self.full_start[i][j]
                    ):
                        busy = True  # znaleziono zajęcia
                        next_class = self.full_start[i][j]
                        break
                if busy:  # przerwanie pętli, bo znaleziono najbliższe zajęcia
                    break
            if busy:
                break

        return self.__if_next_class_found(busy, next_class, datetime_date)

    def __instructions_whether_class_was_found(
        self, list_to_check: list, datetime_date: datetime
    ):
        if list_to_check:
            # sprecyzowanie formy zajęć, jeśli dany przedmiot ma tylko jedną formę, str class_type_name jest pusty
            class_type_set = set()
            list_to_set_specified(
                self.class_type_list,
                class_type_set,
                self.subject_list,
                list_to_check[1],
            )

            if len(class_type_set) == 1:
                list_to_check[1] = ""

            print(
                f'\nW tym czasie masz zajęcia "{list_to_check[0]}{list_to_check[1]}"{list_to_check[2]}.\
                \nTo wydarzenie skończy się w {list_to_check[3]} od sprecyzowanego czasu.\n\n'
            )
        else:
            result = self.__find_next_class_if_no_class_when_specified(datetime_date)

            print(f"\nNie masz wtedy zajęć.\n{result}\n\n")

    def run_mode(self):
        user_given_date = self.__option_1_user_input()

        # jeśli użytkownik chce bazować na obecnej dacie i godzinie
        if user_given_date == "teraz":
            user_given_date = current_time_str

        user_given_date += ":00"
        user_given_date = datetime.strptime(user_given_date, "%d/%m/%Y %H:%M:%S")

        event_list = self.__check_if_during_datetime_there_is_event(user_given_date)

        self.__instructions_whether_class_was_found(event_list, user_given_date)
