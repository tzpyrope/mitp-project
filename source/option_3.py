from instruct_and_data_conversion import *

def check_if_3_input_is_correct(user_input: str):
    while True:
        try:
            if user_input != "jutro" and user_input != "dzisiaj":
                datetime.strptime(user_input, "%d/%m/%Y")
            break
        except ValueError:
            print("\nWprowadź datę w odpowiednim formacie.\n")
            user_input = input()

    return user_input

def option_3_user_input():
    user_input = input(f"\nPodaj datę (format: dd/mm/yyyy).\
                  \nPrzykład: {current_date_str}\
                  \nLub wpisz \"dzisiaj\" albo \"jutro\".\n\n")

    user_date = check_if_3_input_is_correct(user_input)

    return user_date

def user_date_adjustment(user_date: datetime):
    # jeśli użytkownik chce bazować na obecnej/jutrzejszej dacie
    if user_date == "jutro":
        user_date = current_time + timedelta(days = 1)
    elif user_date == "dzisiaj":
        user_date = current_time
    else:
        user_date = datetime.strptime(user_date, "%d/%m/%Y")

    return user_date

def group_class__found_for_specified_day():
    user_date = user_date_adjustment(option_3_user_input())
    
    # inicjalizacja potrzebnych list
    class_all = []
    class_type = []
    classes_start = []
    classes_end = []
    subject_name = []
    location_name = []
    busy = False

    # szukanie dat/godzin zajęć dla sprecyzowanego dnia
    for i in range(len(subject_list)):
        for j in range(len(full_start[i])):
            if user_date.date() == full_start[i][j].date():
                busy = True # w podanym dniu są zajęcia

                # tworzenie wielowymiarowej listy i list z informacjami o zajęciach
                class_all.append([])
                subject_name.append(subject_list[i])

                if pd.isna(class_type_list[i]):
                    class_type.append("")
                else:
                    class_type.append(class_type_list[i])

                if pd.isna(location[i]):
                    location_name.append("")
                else:
                    location_name.append(location[i])
    
                classes_start.append(full_start[i][j])
                classes_end.append(full_end[i][j])

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

def format_datetime_to_string_for_hours(class_list: list):
    # konwersja datetime na str by pokazywał tylko godziny i minuty
    for i in range(len(class_list)):
        class_list[i][3] = "{:d}:{:02d}".format(class_list[i][3].hour, class_list[i][3].minute)
        class_list[i][4] = "{:d}:{:02d}".format(class_list[i][4].hour, class_list[i][4].minute)

def make_a_schedule_table_for_given_day(class_list: list):
    table = [["Przedmiot", "Forma zajęć", "Miejsce", "Godzina rozpoczęcia", "Godzina zakończenia"]]

    for i in range(len(class_list)):
        table.append(class_list[i])

    print("")
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
    print("\n\n")

def user_chose_option_3():
    class_busy = group_class__found_for_specified_day()
    (class_list, busy) = class_busy

    if busy: # jeśli są zajęcia, tworzymy tabelkę
        format_datetime_to_string_for_hours(class_list)
        make_a_schedule_table_for_given_day(class_list)
    else:
        print("\nNie masz wtedy zajęć.\n")