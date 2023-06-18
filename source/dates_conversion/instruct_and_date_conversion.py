from .variables import *


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
