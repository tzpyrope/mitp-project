from .dates_conversion.instruct_and_date_conversion import *
from .mode_functions import *
from .mode_schema import Mode


class Mode2(Mode):
    def __init__(self, csv_handler):
        super().__init__(csv_handler)

    def __get_class_type_and_subject_name(self):
        class_type_set = set()
        class_type_dict = {}
        subject = search_for_subject_corresponding_to_user_choice(self.subject_list)

        list_to_set_specified(
            self.class_type_list, class_type_set, self.subject_list, subject
        )
        type_choice = search_for_number_of_different_class_types(class_type_set)

        if type_choice == 1:
            create_class_type_dict_for_classes_with_more_than_one_type(
                class_type_set, class_type_dict
            )
            class_type = search_for_class_type_corresponding_to_user_choice(
                class_type_dict
            )
            class_type_str = f", {class_type}"
        else:
            class_type = list(class_type_set)[0]
            class_type_str = ""

        return class_type, subject, class_type_str

    def __check_if_closest_date_exists(self, dates: list):
        if len(dates) != 0:
            ordered_dates_after = sorted(dates)
            closest_date = datetime.strftime(ordered_dates_after[0], "%d/%m/%Y %H:%M")
        else:
            closest_date = None

        return closest_date

    def __search_for_closest_class_for_given_subject(
        self, subject: str, class_type: str
    ):
        # szukanie najbliższej przyszłej daty podczas której zaczyna się dany przedmiot w danej formie
        dates_after = []

        for i in range(len(self.subject_list)):
            if (self.subject_list[i] == subject) and (
                self.class_type_list[i] or "" == class_type
            ):
                for j in range(len(self.full_start[i])):
                    if self.full_start[i][j] > current_time:
                        dates_after.append(self.full_start[i][j])

        return self.__check_if_closest_date_exists(dates_after)

    def run_mode(self):
        class_type_and_subject = self.__get_class_type_and_subject_name()
        (class_type, subject, class_type_str) = class_type_and_subject

        date = self.__search_for_closest_class_for_given_subject(subject, class_type)

        if date is not None:
            print(
                f'\nNajbliższe zajęcia "{subject}{class_type_str}" odbędą się dnia {date}.\n\n'
            )
        else:
            print("\nPo podanej dacie nie masz już takich zajęć.\n\n")
