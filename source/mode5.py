import pandas as pd
import numpy as np

from .dates_conversion.instruct_and_date_conversion import *
from .mode2 import *


class Mode5(Mode):
    def __init__(self, csv_handler):
        super().__init__(csv_handler)
        self.file_path = csv_handler.file_path

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
        else:
            class_type = list(class_type_set)[0]

        return class_type, subject

    def __delete_rows_corresponding_with_event(self, class_type, subject):
        df = pd.read_csv(
            r"%s" % self.file_path,
            delimiter=",",
        )

        df.drop(
            df[(df["Tytuł"] == subject) & ((df["Typ"] == class_type) | (pd.isna(df["Typ"])))].index,
            axis="index",
            inplace=True,
        )
        df.reset_index(drop=True, inplace=True)

        df.to_csv(r"%s" % self.file_path, index=False)

    def __confirm_delete(self, class_type, subject):
        if pd.isna(class_type):
            confirmation_str =  f"\nTwoje wydarzenie:\
                \n{subject}"
        else:
            confirmation_str =  f"\nTwoje wydarzenie:\
              \n{class_type}, {subject}"
            
        print(confirmation_str)

        confirm_input = input(
            "Czy jesteś pewien, że chcesz usunąć to wydarzenie? (y/n) "
        )

        return confirm_input

    def run_mode(self):
        type_and_subject = self.__get_class_type_and_subject_name()
        (class_type, subject) = type_and_subject

        confirm_choice = self.__confirm_delete(class_type, subject)

        if confirm_choice == "y":
            self.__delete_rows_corresponding_with_event(class_type, subject)
            print("\nWydarzenie zostało usunięte.\n\n")
        else:
            print("\nWydarzenie nie zostało usunięte.\n\n")
