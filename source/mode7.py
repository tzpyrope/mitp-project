from .instruct_and_date_conversion import *


def option_7_user_input():
    print(
        f"\nPodaj przedział czasowy, który chcesz sprawdzić (format dd/mm/yyyy).\
              \nJeśli interesuje cię konkretny dzień, wpisz jedną datę.\
              \nPrzykład: {current_date_str}\
              \nJeśli interesuje cię przedział pomiędzy dwoma datami, wpisz obie.\
              \nPrzykład: {current_date_str} - {tommorow_time_str}\n"
    )

    user_input = input()

    return user_input


def check_if_7_input_is_correct_for_multiple_dates(user_input: str):
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


def check_if_7_input_is_correct_for_single_date(user_input: str):
    while True:
        try:
            user_date = datetime.strptime(user_input, "%d/%m/%Y")
            break
        except ValueError:
            print("\nWprowadź datę w odpowiednim formacie.\n")
            user_input = input()

    return user_date


def find_classes_for_multiple_dates(user_dates: list, classes: dict, class_types: dict):
    for i in range(len(full_start)):
        for j in range(len(full_start[i])):
            if (
                full_start[i][j].date() <= user_dates[1].date()
                and full_start[i][j].date() >= user_dates[0].date()
            ):
                classes.append(subject_list[i])
                class_types.append(class_type_list[i])


def find_classes_for_one_date(user_date: list, classes: dict, class_types: dict):
    for i in range(len(full_start)):
        for j in range(len(full_start[i])):
            if full_start[i][j].date() == user_date.date():
                classes.append(subject_list[i])
                class_types.append(class_type_list[i])


def get_class_info():
    user_date = option_7_user_input()
    classes = []
    class_types = []

    if "-" in user_date:
        user_date = check_if_7_input_is_correct_for_multiple_dates(user_date)
        find_classes_for_multiple_dates(user_date, classes, class_types)
    else:
        user_date = check_if_7_input_is_correct_for_single_date(user_date)
        find_classes_for_one_date(user_date, classes, class_types)

    num_of_classes = len(classes)

    return classes, class_types, num_of_classes


def get_gramatically_correct_str(num: int):
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


def user_chose_option_7():
    class_info = get_class_info()
    (class_list, type_list, num_of_classes) = class_info
    strings = get_gramatically_correct_str(num_of_classes)
    (plan, event) = strings

    print(f"\nW tym okresie masz {num_of_classes} {plan} {event}:\n")
    for i in range(len(class_list)):
        if pd.isna(type_list[i]):
            print(class_list[i])
        else:
            print(f"{class_list[i]}, {type_list[i]}")
    print("\n")
