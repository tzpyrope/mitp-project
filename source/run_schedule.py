from .option_1 import *
from option_2 import *
from option_3 import *
from option_4 import *
from option_6 import *
from option_7 import *
import sys

def get_user_choice_input():
    choice = input()

    return choice

def check_if_wrong_choice_input(choice: str):
    while True:
        if choice in list(get_main_part_instructions().keys()):
            break
        else:
            print("\nWybierz jedną z podanych opcji.\n")
            choice = input()

    return choice

def main():
    while True:
        print_main_part_instructions()
        user_choice = get_user_choice_input()

        user_choice = check_if_wrong_choice_input(user_choice)

        if user_choice == "1":
            user_chose_option_1()
        elif user_choice == "2": 
            user_chose_option_2()
        elif user_choice == "3":
            user_chose_option_3()
        elif user_choice == "4":
            user_chose_option_4()
        elif user_choice == "6": 
            user_chose_option_6()
        elif user_choice == "7":
            user_chose_option_7()
        elif user_choice == "exit":
            exit()

main()