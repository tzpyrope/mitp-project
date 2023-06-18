from abc import ABC, abstractmethod


class Mode(ABC):
    def __init__(self, csv_handler):
        self.full_start = csv_handler.get_class_start_times()
        self.full_end = csv_handler.get_class_end_times()
        self.class_type_list = csv_handler.class_type_list
        self.subject_list = csv_handler.subject_list
        self.start_days = csv_handler.start_days
        self.end_days = csv_handler.end_days
        self.start_time = csv_handler.start_time
        self.end_time = csv_handler.end_time
        self.location = csv_handler.location

    @abstractmethod
    def run_mode(self):
        pass
