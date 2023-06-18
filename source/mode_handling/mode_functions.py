from datetime import datetime


def get_main_part_instructions():
    instructions = {
        "1": "podaje jakie masz zajęcia w podanym dniu o danej godzinie\
        \njeśli nie masz wtedy zajęć, podaje kiedy masz następne zajęcia tego samego dnia",
        "2": "podaje kiedy masz najbliższe zajęcia z danego przedmiotu (w oparciu o obecną datę lub sprecyzowaną)",
        "3": "podaje twój plan zajęć na dany dzień",
        "4": "dodaje wydarzenie",
        "5": "usuwa wydarzenie",
        "6": "wyszukaj wolne sloty w podanym terminie",
        "7": "podaje ile w danym okresie czasowym masz zaplanowanych wydarzeń",
        "help": "pokazuje ponownie listę opcji",
        "exit": "zakończ program",
    }

    return instructions


def make_main_part_instructions_str():
    instructions = get_main_part_instructions()

    instructions_str = ""

    instructions_str += "\nWybierz jedną z poniższych opcji:"
    for key, value in instructions.items():
        instructions_str += f"\n{key} - {value}"
    instructions_str += "\n"

    return instructions_str


def append_hour(date_list: list, hour_list: list, ending_list: list):
    for i in range(len(date_list)):
        list_object = date_list[i] + " " + hour_list[i]
        ending_list.append(list_object)


def datetime_list_conversion(beginning_list: list):
    for i in range(len(beginning_list)):
        list_object_datetime = datetime.strptime(beginning_list[i], "%d.%m.%Y %H:%M")
        beginning_list[i] = list_object_datetime


def datediff_to_h_min(end_date: datetime, start_date: datetime):
    h_min = end_date - start_date
    h_min = str(h_min).replace(":", " ")
    if ("00 00") in h_min:
        h_min = h_min.replace(" 00 00", "h")
    else:
        h_min = h_min.replace(" 00", "")
        h_min = h_min.replace(" ", "h ") + "min"
    return h_min


def list_to_set_specified(
    list_from_set: list, new_set: set, specified_list: list, specified_variable
):
    for i in range(len(specified_list)):
        if specified_list[i] == specified_variable:
            new_set.add(list_from_set[i])



def generate_subject_options(subject_list):
    subject_set = set(subject_list)
    subject_pool_dict = {}
    number_subject = 0

    for subject in subject_set:
        number_subject += 1
        number_str = str(number_subject)
        subject_pool_dict[number_str] = subject

    return subject_pool_dict


def check_if_user_input_is_in_dict_keys(user_input: str, options: dict):
    while user_input not in list(options.keys()):
        print("\nWpisz poprawnie wybraną opcję.\n")
        user_input = input()

    return user_input


def get_user_input_subject(subject_list):
    possible_subjects = generate_subject_options(subject_list)

    print("\nWybierz przedmiot, który cię interesuje:")

    for key in possible_subjects:
        print(f"{key} - {possible_subjects[key]}")

    user_input = input("\n")

    subject_input = check_if_user_input_is_in_dict_keys(user_input, possible_subjects)

    return subject_input


def search_for_subject_corresponding_to_user_choice(subject_list):
    possible_subjects = generate_subject_options(subject_list)
    subject = get_user_input_subject(subject_list)

    for key in possible_subjects:
        if key == subject:
            subject_name = possible_subjects[key]
            return subject_name


def search_for_number_of_different_class_types(class_type_set: set):
    if len(class_type_set) <= 1:
        type_choice = 0
    else:
        type_choice = 1

    return type_choice


def create_class_type_dict_for_classes_with_more_than_one_type(
    class_type_set: set, class_type_dict: dict
):
    number_type = 0

    for class_type in class_type_set:
        number_type += 1
        number_str = str(number_type)
        class_type_dict[number_str] = class_type

    return class_type_dict


def get_user_input_class_type(class_type_dict: dict):
    print("\nWybierz formę zajęć, która cię interesuje:")

    for key in class_type_dict:
        print(f"{key} - {class_type_dict[key]}")

    user_input = input("\n")

    class_type_input = check_if_user_input_is_in_dict_keys(user_input, class_type_dict)

    return class_type_input


def search_for_class_type_corresponding_to_user_choice(class_type_dict: dict):
    class_type = get_user_input_class_type(class_type_dict)

    for key in class_type_dict:
        if key == class_type:
            class_type_name = class_type_dict[key]
            return class_type_name
