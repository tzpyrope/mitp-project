import csv
from datetime import datetime, timedelta
from operator import itemgetter

from .mode_schema import Mode


class Mode4(Mode):
    def __init__(self, csv_handler):
        super().__init__(csv_handler)
        self.file_path = csv_handler.file_path

    def __get_title_input(self):
        title = input("\nŻeby dodać nowe wydarzenie, najpierw wpisz tytuł wydarzenia: ")

        return title

    def __get_type_input(self):
        user_type = input(
            '\nWpisz typ wydarzenia (jeśli dodajesz przedmiot do planu zajęć, wpisujesz nazwę formy zajęć - np. CWA).\
                        \nJeśli chcesz, żeby to pole pozostało puste, wpisz "brak": '
        )

        if user_type == "brak":
            user_type = ""

        return user_type

    def __check_if_day_in_correct_format(self, day: str):
        while True:
            try:
                datetime.strptime(day, "%d/%m/%Y")
                break
            except ValueError:
                print("\nWprowadź datę w odpowiednim formacie.\n")
                day = input()

        return day

    def __get_start_day_input(self):
        start_day = input(
            "\nWpisz dzień, w którym wydarzenie się rozpoczyna (format dd/mm/yyyy): "
        )
        start_day = self.__check_if_day_in_correct_format(start_day)
        start_day = start_day.replace("/", ".")

        return start_day

    def __get_end_day_input(self):
        end_day = input(
            '\nJeśli wydarzenie się powtarza co tydzień o tej samej godzinie, wpisz dzień, w którym się kończy (format dd/mm/yyyy).\
                            \nJeśli wydarzenie trwa tylko jeden dzień, wpisz "brak": '
        )
        if end_day != "brak":
            end_day = self.__check_if_day_in_correct_format(end_day)
            end_day = end_day.replace("/", ".")
        else:
            end_day = ""

        return end_day

    def __check_if_hours_in_correct_format(self, hours: str):
        while True:
            try:
                hours_list = hours.split(" - ")
                list(map(lambda hour: datetime.strptime(hour, "%H:%M"), hours_list))
                break
            except ValueError:
                print("\nWprowadź godziny w odpowiednim formacie.\n")
                hours = input()

        return hours_list

    def __get_hours_input(self):
        hours = input(
            "\nWpisz godziny, w których trwa wydarzenie (przykład: 8:00 - 12:30): "
        )
        hours = self.__check_if_hours_in_correct_format(hours)

        return hours

    def __get_location_input(self):
        user_location = input(
            '\nWpisz miejsce, w którym wydarzenie ma mieć miejsce.\
                            \nJeśli chcesz, żeby to pole pozostało puste, wpisz "brak": '
        )

        if user_location == "brak":
            user_location = ""

        return user_location

    def __count_weeks_between_dates(self, start_day: str, end_day: str):
        end_day = datetime.strptime(end_day, "%d.%m.%Y")
        start_day = datetime.strptime(start_day, "%d.%m.%Y")
        week_count = abs(end_day - start_day).days // 7

        return week_count

    def __create_lists_of_dates(self, start_day: str, end_day: str, start_hour: str, end_hour: str):
        start_dates_list = []
        end_dates_list = []

        start_day_time = datetime.strptime(
            start_day + " " + start_hour, "%d.%m.%Y %H:%M"
        )
        end_day_time = datetime.strptime(start_day + " " + end_hour, "%d.%m.%Y %H:%M")

        if end_day == "":
            start_dates_list.append(start_day_time)
            end_dates_list.append(end_day_time)
        else:
            week_count = self.__count_weeks_between_dates(start_day, end_day)

            for i in range(0, week_count + 1):
                start_dates_list.append(start_day_time + timedelta(weeks=i))
                end_dates_list.append(end_day_time + timedelta(weeks=i))

        return start_dates_list, end_dates_list

    def __check_if_events_overlap(self, start_day: str, end_day: str, start_hour: str, end_hour: str):
        lists = self.__create_lists_of_dates(start_day, end_day, start_hour, end_hour)
        (start_list, end_list) = lists

        overlaps = []
        flag = 0

        for i in range(len(start_list)):
            for j in range(len(self.full_start)):
                for k in range(len(self.full_start[j])):
                    if (
                        self.full_start[j][k] > start_list[i]
                        and self.full_start[j][k] < end_list[i]
                    ) or (
                        self.full_end[j][k] > start_list[i]
                        and self.full_end[j][k] < end_list[i]
                    ):
                        overlaps.append([])

                        overlaps[flag].append(self.subject_list[j])
                        overlaps[flag].append(self.full_start[j][k])
                        overlaps[flag].append(self.full_end[j][k])

                        flag += 1

        overlaps_sorted = sorted(overlaps, key=itemgetter(1))

        return overlaps_sorted

    def __make_inputs_into_dict(self):
        title = self.__get_title_input()
        event_type = self.__get_type_input()
        start_day = self.__get_start_day_input()
        end_day = self.__get_end_day_input()
        hours = self.__get_hours_input()
        start_hour = hours[0]
        end_hour = hours[1]
        place = self.__get_location_input()

        overlap = self.__check_if_events_overlap(
            start_day, end_day, start_hour, end_hour
        )

        csv_input_dict = {
            "Nazwa": "",
            "Grupa": "",
            "Typ": f"{event_type}",
            "Tytuł": f"{title}",
            "Uwaga": "",
            "Dzień tygodnia": "",
            "Pierwszy dzień": f"{start_day}",
            "Ostatni dzień": f"{end_day}",
            "Ogłoszony początek": f"{start_hour}",
            "Ogłoszony koniec": f"{end_hour}",
            "Miejsce": f"{place}",
            "Pojemność": "",
            "Prowadzący / Odpowiedzialny": "",
            "E-mail": "",
            "Żądane usługi": "",
            "Zatwierdzony": "",
        }

        return csv_input_dict, overlap

    def __confirm_the_change(self, inputs: dict):
        print(
            f"\nTwoje wydarzenie:\
            \nTyp: {inputs['Typ']}\
            \nTytuł: {inputs['Tytuł']}\
            \nPierwszy dzień: {inputs['Pierwszy dzień']}\
            \nOstatni dzień: {inputs['Ostatni dzień']}\
            \nGodzina rozpoczęcia: {inputs['Ogłoszony początek']}\
            \nGodzina zakończenia: {inputs['Ogłoszony koniec']}\
            \nMiejsce: {inputs['Miejsce']}"
        )
        choice = input("Czy chcesz dodać to wydarzenie? (y/n): ")

        return choice

    def __add_new_event(self, input_dict: dict, file_path: str):
        choice = self.__confirm_the_change(input_dict)

        if choice == "y":
            column_names = list(input_dict.keys())
            with open(f"{file_path}", "a", encoding="utf8", newline="") as csvfile:
                dictwriter_object = csv.DictWriter(csvfile, fieldnames=column_names)

                dictwriter_object.writerow(input_dict)
                csvfile.close()

            print(
                "\nWydarzenie zostało dodane. Zrestartuj program, żeby zostało wczytane do pozostałych opcji.\n\n"
            )
        else:
            print("\nWydarzenie nie zostało dodane.\n\n")

    def run_mode(self):
        inputs = self.__make_inputs_into_dict()
        (input_dict, overlap) = inputs

        if len(overlap) == 0:
            self.__add_new_event(input_dict, self.file_path)
        else:
            print(
                "\n\nTwoje wydarzenie pokrywa się czasowo z innymi zaplanowanymi już wydarzeniami, na przykład:"
            )

            for i in range(len(overlap)):
                date_start = datetime.strftime(overlap[i][1], "%d/%m/%Y %H:%M")
                date_end = datetime.strftime(overlap[i][2], "%d/%m/%Y %H:%M")

                print(f"{overlap[i][0]}: {date_start} - {date_end}")

                if i == 3:
                    break

            print(
                "\nJeśli w ciągu wcześniej zaplanowanego wydarzenia dzieje się coś, co chcesz mieć w planie, "
                "możesz usunąć kolidujące wydarzenie.\n\n"
            )
