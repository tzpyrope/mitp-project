from source import *


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
    csv_handler = CsvConversion("events.csv")

    m1 = Mode1(csv_handler)
    m2 = Mode2(csv_handler)
    m3 = Mode3(csv_handler)
    m4 = Mode4(csv_handler)
    m5 = Mode5(csv_handler)
    m6 = Mode6(csv_handler)
    m7 = Mode7(csv_handler)

    instructions = make_main_part_instructions_str()
    print(instructions)

    while True:
        user_choice = get_user_choice_input()
        user_choice = check_if_wrong_choice_input(user_choice)

        if user_choice == "1":
            m1.run_mode()
        elif user_choice == "2":
            m2.run_mode()
        elif user_choice == "3":
            m3.run_mode()
        elif user_choice == "4":
            m4.run_mode()
        elif user_choice == "5":
            m5.run_mode()
        elif user_choice == "6":
            m6.run_mode()
        elif user_choice == "7":
            m7.run_mode()
        elif user_choice == "help":
            print(instructions)
        elif user_choice == "exit":
            break


if __name__ == "__main__":
    main()
