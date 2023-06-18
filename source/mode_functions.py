def generate_subject_options(subject_list):
    subject_set = set(subject_list)
    subject_pool_dict = {}
    # żeby móc dopasować wybrany numer do odpowiedniego przedmiotu
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
    # jeśli dane zajęcia mają tylko jeden typ nie ma sensu dawać użytkownikowi wybór

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
    # opcja wybrania wykładu/ćwiczeń/warsztatu/etc dla przedmiotu
    print("\nWybierz formę zajęć, która cię interesuje:")

    for key in class_type_dict:
        print(f"{key} - {class_type_dict[key]}")

    user_input = input("\n")

    class_type_input = check_if_user_input_is_in_dict_keys(user_input, class_type_dict)

    return class_type_input


def search_for_class_type_corresponding_to_user_choice(class_type_dict: dict):
    class_type = get_user_input_class_type(class_type_dict)

    # szukanie typu odpowiadającemu wybranemu numerowi
    for key in class_type_dict:
        if key == class_type:
            class_type_name = class_type_dict[key]
            return class_type_name
