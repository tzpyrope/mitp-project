from .instruct_and_data_conversion import *


def get_title_input():
    title = input("\nŻeby dodać nowe wydarzenie, najpierw wpisz tytuł wydarzenia: ")

    return title

def get_type_input():
    user_type = input("\nWpisz typ wydarzenia (jeśli dodajesz przedmiot do planu zajęć, wpisujesz nazwę formy zajęć - np. CWA).\
                    \nJeśli chcesz, żeby to pole pozostało puste, wpisz \"brak\": ")

    return user_type

def check_if_day_in_correct_format(day):
    while True:
        try:
            datetime.strptime(day, "%d/%m/%Y")
            break
        except ValueError:
            print("\nWprowadź datę w odpowiednim formacie.\n")
            day = input()

    return day

def get_start_day_input():
    start_day = input("\nWpisz dzień, w którym wydarzenie się rozpoczyna (format dd/mm/yyyy): ")
    start_day = check_if_day_in_correct_format(start_day)
    start_day = start_day.replace("/", ".")

    return start_day

def get_end_day_input():
    end_day = input("\nJeśli wydarzenie się powtarza co tydzień o tej samej godzinie, wpisz dzień, w którym się kończy (format dd/mm/yyyy).\
                        \nJeśli wydarzenie trwa tylko jeden dzień, wpisz \"brak\": ")
    if end_day != "brak":
        end_day = check_if_day_in_correct_format(end_day)
        end_day = end_day.replace("/", ".")

    return end_day

def check_if_hours_in_correct_format(hours: str):
    while True:
        try:
            hours_list = hours.split(" - ")
            list(map(lambda hour: datetime.strptime(hour, "%H:%M"), hours_list))
            break
        except ValueError:
            print("\nWprowadź godziny w odpowiednim formacie.\n")
            hours = input()
    
    return hours_list


def get_hours_input():
    hours = input("\nWpisz godziny, w których trwa wydarzenie (przykład: 8:00 - 12:30): ")
    hours = check_if_hours_in_correct_format(hours)
    
    return hours

def get_location_input():
    user_location = input("\nWpisz miejsce, w którym wydarzenie ma mieć miejsce.\
                        \nJeśli chcesz, żeby to pole pozostało puste, wpisz \"brak\": ")

    return user_location

def count_weeks_between_dates(start_day: str, end_day: str):
    end_day = datetime.strptime(end_day, "%d.%m.%Y")
    start_day = datetime.strptime(start_day, "%d.%m.%Y")
    week_count = (abs(end_day - start_day).days) // 7

    return week_count

def create_lists_of_dates(start_day, end_day, start_hour, end_hour):
    start_dates_list = []
    end_dates_list = []
    
    start_day_time = datetime.strptime(start_day + " " + start_hour, "%d.%m.%Y %H:%M")
    end_day_time = datetime.strptime(start_day + " " + end_hour, "%d.%m.%Y %H:%M")

    if end_day != "brak":
        week_count = count_weeks_between_dates(start_day, end_day)

        for i in range(0, week_count + 1):
            start_dates_list.append(start_day_time + timedelta(weeks=i))
            end_dates_list.append(end_day_time + timedelta(weeks=i))

    return start_dates_list, end_dates_list


def check_if_events_overlap(start_day, end_day, start_hour, end_hour):
    lists = create_lists_of_dates(start_day, end_day, start_hour, end_hour)
    (start_list, end_list) = lists

    overlaps = []
    flag = 0

    for i in range(len(start_list)):
        for j in range(len(full_start)):
            for k in range(len(full_start[j])):
                if (full_start[j][k] > start_list[i] and full_start[j][k] < end_list[i]) or \
                (full_end[j][k] > start_list[i] and full_end[j][k] < end_list[i]):
                    overlaps.append([])

                    overlaps[flag].append(subject_list[j])
                    overlaps[flag].append(full_start[j][k])
                    overlaps[flag].append(full_end[j][k])

                    flag += 1

    overlaps_sorted = sorted(overlaps, key=itemgetter(1))

    return overlaps_sorted

def make_inputs_into_dict():
    title = get_title_input()
    event_type = get_type_input()
    start_day = get_start_day_input()
    end_day = get_end_day_input()
    hours = get_hours_input()
    start_hour = hours[0]
    end_hour = hours[1]
    place = get_location_input()

    overlap = check_if_events_overlap(start_day, end_day, start_hour, end_hour)

    dict = {
        "Nazwa": "brak",
        "Grupa": "brak",
        "Typ": event_type,
        "Tytuł": title,
        "Uwaga": "brak",
        "Dzień tygodnia": "brak",
        "Pierwszy dzień": start_day, 
        "Ostatni dzień": end_day, 
        "Ogłoszony początek": start_hour, 
        "Ogłoszony koniec": end_hour, 
        "Miejsce": place,
        "Pojemność": "brak",
        "Prowadzący / Odpowiedzialny": "brak",
        "E-mail": "brak",
        "Żądane usługi": "brak",
        "Zatwierdzony": "brak"
    }

    return dict, overlap

def confirm_the_change(inputs: dict):
    print(f"\nTwoje wydarzenie:\
          \nTyp: {inputs['Typ']}\
          \nTytuł: {inputs['Tytuł']}\
          \nPierwszy dzień: {inputs['Pierwszy dzień']}\
          \nOstatni dzień: {inputs['Ostatni dzień']}\
          \nGodzina rozpoczęcia: {inputs['Ogłoszony początek']}\
          \nGodzina zakończenia: {inputs['Ogłoszony koniec']}\
          \nMiejsce: {inputs['Miejsce']}")
    choice = input("Czy chcesz dodać to wydarzenie? (y/n): ")

    return choice

def add_new_event(input_dict: dict):
    choice = confirm_the_change(input_dict)

    if choice == "y":
        column_names = list(input_dict.keys())
        with open("events.csv", "a", encoding = "utf8", newline="") as csvfile:
            dictwriter_object = csv.DictWriter(csvfile, fieldnames = column_names)

            dictwriter_object.writerow(input_dict)
            csvfile.close()

        print("\nWydarzenie zostało dodane. Zrestartuj program, żeby zostało wczytane do pozostałych opcji.\n")
    else:
        print("\nWydarzenie nie zostało dodane.\n")


def user_chose_option_4():
    inputs = make_inputs_into_dict()
    (input_dict, overlap) = inputs

    if len(overlap) == 0:
        add_new_event(input_dict)
    else:
        print("\n\nTwoje wydarzenie pokrywa się czasowo z innymi zaplanowanymi już wydarzeniami, na przykład:")

        for i in range(len(overlap)):
            if i < 3:
                date_start = datetime.strftime(overlap[i][1], "%d/%m/%Y %H:%M")
                date_end = datetime.strftime(overlap[i][2], "%d/%m/%Y %H:%M")

                print(f"{overlap[i][0]}: {date_start} - {date_end}")
        
        print("\nJeśli w ciągu wcześniej zaplanowanego wydarzenia dzieje się coś, co chcesz mieć w planie, możesz usunąć kolidujące wydarzenie.\n")
