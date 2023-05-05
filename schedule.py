from option_1 import *
from option_2 import *
from option_3 import *
from option_4 import *
from option_6 import *
from option_7 import *

main_part_instructions()

while True:
    user_choice = input()

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
    elif user_choice == "help":
        print("\n")
        main_part_instructions()
    elif user_choice == "exit":
        exit()

    else: # użytkownik wpisuje coś innego niż 1, 2, 3 etc.
        print("oopsie")