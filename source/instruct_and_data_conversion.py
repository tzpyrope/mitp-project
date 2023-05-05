from datetime import datetime, timedelta
from tabulate import tabulate
from operator import itemgetter
import numpy as np
import csv
from vardata import *

def get_main_part_instructions():
    instructions = {"1": "podaje jakie masz zajęcia w podanym dniu o danej godzinie\
        \njeśli nie masz wtedy zajęć, podaje kiedy masz następne zajęcia tego samego dnia",
        "2": "podaje kiedy masz najbliższe zajęcia z danego przedmiotu (w oparciu o obecną datę lub sprecyzowaną)",
        "3": "podaje twój plan zajęć na dany dzień",
        "4": "dodaje wydarzenie",
        "5": "usuwa wydarzenie",
        "6": "wyszukaj wolne sloty w podanym terminie",
        "7": "podaje ile w danym okresie czasowym masz zaplanowanych wydarzeń",
        "help": "pokazuje ponownie listę opcji",
        "exit": "zakończ program"}
    
    return instructions
    
def print_main_part_instructions():
    instructions = get_main_part_instructions()
    
    print("\nWybierz jedną z poniższych opcji:")
    for key, value in instructions.items():
        print(f"{key} - {value}")
    print("\n")

def append_hour(date_list: list, hour_list: list, ending_list: list):
    for i in range(len(date_list)):
        list_object = date_list[i] + " " + hour_list[i]
        ending_list.append(list_object)

def datetime_list_conversion(beginning_list: list):
    for i in range(len(beginning_list)):
        list_object_datetime =  datetime.strptime(beginning_list[i], "%d.%m.%Y %H:%M")
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

def list_to_set_specified(list_from_set: list, new_set: set, specified_list: list, specified_variable):
    for i in range(len(specified_list)):
        if specified_list[i] == specified_variable:
            new_set.add(list_from_set[i])

def account_for_single_day_events(start_time_end_day: list, end_time_end_day: list, weeks: list):
    start_time_end_day.append("N/A")
    end_time_end_day.append("N/A")
    weeks.append(0)

def make_multidimensional_list_for_end_days(start_time_end_day: list, end_time_end_day: list, weeks: list, i: int):
    end_day = datetime.strptime(end_days[i], "%d.%m.%Y")
    start_day = datetime.strptime(start_days[i], "%d.%m.%Y")
    week_count = (abs(end_day - start_day).days) // 7
    weeks.append(week_count)
    
    start_time_end_day.append([])
    end_time_end_day.append([])

    for number in range(0, (week_count + 1)):
        date = start_day + timedelta(weeks=number)
        date = datetime.strftime(date, "%d.%m.%Y")
        date_begin = date + " " + start_time[i]
        date_end = date + " " + end_time[i]
        date_begin = datetime.strptime(date_begin, "%d.%m.%Y %H:%M")
        date_end = datetime.strptime(date_end, "%d.%m.%Y %H:%M")
        start_time_end_day[i].append(date_begin)
        end_time_end_day[i].append(date_end)

def end_days_datetime_list_conversion(return_start: bool):
    # utworzenie dwuwymiarowej listy dla kolumny end_days
    # + co jeśli end_days == missing value albo jest takie samo jak start_days
    start_time_end_days = []
    end_time_end_days = []

    weeks = []

    for i in range(len(end_days)):
        if pd.isna(end_days[i]) or end_days[i] == start_days[i]:
            account_for_single_day_events(start_time_end_days, end_time_end_days, weeks)
        # wzięcie start_days[i] i end_days[i], policzenie ile jest między nimi tygodni (start_days wliczone, więc nie trzeba potem robić insert)
        # musi być w datetime
        else:
            make_multidimensional_list_for_end_days(start_time_end_days, end_time_end_days, weeks, i)

    if return_start:
        return start_time_end_days
    else:
        return end_time_end_days

def start_days_datetime_list_conversion(return_start: bool):
    # data zajęć w kolumnie "pierwszy dzień" + godzina rozpoczęcia/zakończenia
    start_time_start_days = []
    end_time_start_days = []

    # godziny rozpoczęcia, zakończenia zajęć dodane do start_days
    append_hour(start_days, start_time, start_time_start_days)
    append_hour(start_days, end_time, end_time_start_days)

    # str na datetime dla start_days zajęć + godziny rozpoczęcia, zakończenia zajęć
    datetime_list_conversion(start_time_start_days)
    datetime_list_conversion(end_time_start_days)

    if return_start:
        return start_time_start_days
    else:
        return end_time_start_days
    
def final_end_days_list_conversion():
    full_end = []

    end_time_start_days_list = start_days_datetime_list_conversion(False)
    end_time_end_days_list = end_days_datetime_list_conversion(False)

    for i in range(len(end_time_start_days_list)):
        if end_time_end_days_list[i] == "N/A":
            full_end.append([end_time_start_days_list[i]])
        else:
            full_end.append(end_time_end_days_list[i])

    return full_end

def final_start_days_list_conversion():
    # łączenie dni początkowych i końcowych w dwie dwuwymiarowe listy, jedna z godzinami rozpoczęcia i druga zakończenia
    full_start = []

    start_time_start_days_list = start_days_datetime_list_conversion(True)
    start_time_end_days_list = end_days_datetime_list_conversion(True)

    for i in range(len(start_time_start_days_list)):
        if start_time_end_days_list[i] == "N/A":
            full_start.append([start_time_start_days_list[i]])
        else:        
            full_start.append(start_time_end_days_list[i])

    return full_start

full_start = final_start_days_list_conversion()
full_end = final_end_days_list_conversion()